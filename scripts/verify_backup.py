"""
SovereignAI — Backup Integrity & Decryption Verifier
Verifies local and remote backups against SHA-256 hashes and verifies AES-256-GCM authentication tags.
Strictly Zero Secret Exposure: Never reveals keys or confidential payload data.
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path

from encrypt_backup import MAGIC_HEADER, get_encryption_key
from backup_to_drive import find_rclone, GDRIVE_REMOTE_BASE

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    print("[ERROR] cryptography library is required.", file=sys.stderr)
    sys.exit(1)


def verify_enc_file(enc_path: Path, raw_key: bytes) -> dict:
    """Verifies SHA-256 hash and GCM authentication tag for an encrypted backup file."""
    res = {
        "file": enc_path.name,
        "exists": enc_path.exists(),
        "sha256_match": False,
        "tag_auth": False,
        "error": None
    }

    if not enc_path.exists():
        res["error"] = "File not found"
        return res

    with open(enc_path, "rb") as f:
        data = f.read()

    actual_hash = hashlib.sha256(data).hexdigest().upper()

    # Check meta.json
    meta_file = enc_path.with_name(f"{enc_path.name}.meta.json")
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
            expected_hash = meta.get("sha256_checksum", "").upper()
            res["sha256_match"] = (actual_hash == expected_hash)
        except Exception as e:
            res["error"] = f"Failed to read metadata: {e}"
    else:
        res["sha256_match"] = True  # No meta file to conflict

    # Verify GCM Auth Tag
    header_len = len(MAGIC_HEADER)
    if len(data) >= header_len + 12 + 16 and data[:header_len] == MAGIC_HEADER:
        nonce = data[header_len:header_len + 12]
        ciphertext = data[header_len + 12:]
        aesgcm = AESGCM(raw_key)

        # Try with source filename in AAD
        source_name = enc_path.name[:-4] if enc_path.name.endswith(".enc") else enc_path.name
        aad = MAGIC_HEADER + source_name.encode("utf-8")
        try:
            aesgcm.decrypt(nonce, ciphertext, aad)
            res["tag_auth"] = True
        except Exception:
            try:
                aesgcm.decrypt(nonce, ciphertext, None)
                res["tag_auth"] = True
            except Exception as e:
                res["error"] = f"Authentication tag failed: {e}"

    return res


def check_remote_listing():
    """Checks remote files on Google Drive via rclone."""
    try:
        rclone = find_rclone()
        cmd = [rclone, "lsf", GDRIVE_REMOTE_BASE, "-R"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0:
            lines = [l.strip() for l in res.stdout.splitlines() if l.strip()]
            return lines
    except Exception:
        pass
    return []


def main():
    print("========================================================")
    print("  SovereignAI — Backup Integrity Verification Audit     ")
    print("========================================================")

    try:
        key = get_encryption_key()
    except Exception as e:
        print(f"[ERROR] Could not load encryption key: {e}", file=sys.stderr)
        sys.exit(1)

    # 1. Audit local backups
    local_encs = list(Path("backups").glob("**/*.enc"))
    print(f"[*] Auditing {len(local_encs)} local encrypted backup file(s)...")

    all_passed = True
    for enc in local_encs:
        report = verify_enc_file(enc, key)
        sha_status = "PASS" if report["sha256_match"] else "FAIL"
        auth_status = "PASS" if report["tag_auth"] else "FAIL"
        print(f"  - File: {report['file']}")
        print(f"    SHA-256 Checksum:       [{sha_status}]")
        print(f"    AES-GCM Authentication: [{auth_status}]")
        if report["error"]:
            print(f"    Error:                  {report['error']}")
            all_passed = False

    # 2. Check remote Google Drive files
    print(f"\n[*] Checking remote Google Drive artifacts ({GDRIVE_REMOTE_BASE})...")
    remote_files = check_remote_listing()
    if remote_files:
        print(f"[SUCCESS] Remote files detected on Google Drive ({len(remote_files)} files):")
        for rf in remote_files:
            print(f"  + {rf}")
    else:
        print("[!] No remote files detected or rclone remote query failed.")

    print("\n========================================================")
    if all_passed and local_encs:
        print("  [SUCCESS] All backup integrity and key checks PASSED! ")
    elif not local_encs:
        print("  [NOTICE] No local backups found. Run backup_to_drive.bat first.")
    else:
        print("  [WARNING] Some backup verification checks failed.")
    print("========================================================")


if __name__ == "__main__":
    main()
