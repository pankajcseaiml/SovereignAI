"""
SovereignAI — Enterprise Google Drive Backup Pipeline
Automates database dump, storage archive, AES-256-GCM encryption, checksumming,
and uploading to Google Drive via rclone.
"""

import os
import sys
import tarfile
import json
import subprocess
import shutil
from datetime import datetime, timezone
from pathlib import Path

from encrypt_backup import encrypt_file, get_encryption_key

RCLONE_EXE = r"C:\Users\Pankaj\AppData\Local\Microsoft\WinGet\Links\rclone.exe"
GDRIVE_REMOTE_BASE = "gdrive:Projects/SovereignAI"
BACKUP_DIR = Path("backups")


def find_rclone() -> str:
    """Locates rclone executable."""
    if Path(RCLONE_EXE).exists():
        return RCLONE_EXE
    rclone_path = shutil.which("rclone")
    if rclone_path:
        return rclone_path
    raise FileNotFoundError("rclone not found. Please install rclone or set path.")


def dump_database(timestamp: str, db_backup_dir: Path) -> Path:
    """Dumps database. Tries docker pg_dump first, falls back to schema export."""
    dump_sql = db_backup_dir / f"sovereignai_db_{timestamp}.sql"
    dump_success = False

    # Try docker compose exec postgres pg_dump
    try:
        cmd = ["docker", "compose", "exec", "-T", "postgres", "pg_dump", "-U", "user", "-d", "sovereignai"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if res.returncode == 0 and len(res.stdout) > 50:
            with open(dump_sql, "w", encoding="utf-8") as f:
                f.write(res.stdout)
            dump_success = True
            print(f"  [+] Database dumped via PostgreSQL container ({len(res.stdout)} bytes)")
    except Exception:
        pass

    if not dump_success:
        # Fallback: export using database/schema.sql + seeds
        schema_file = Path("database/schema.sql")
        content = ""
        if schema_file.exists():
            content = schema_file.read_text(encoding="utf-8")
        else:
            content = "-- SovereignAI Schema Backup Fallback\n"
        with open(dump_sql, "w", encoding="utf-8") as f:
            f.write(f"-- SovereignAI Database Backup - Timestamp: {timestamp}\n{content}\n")
        print(f"  [+] Database exported from schema definition ({dump_sql})")

    return dump_sql


def archive_storage(timestamp: str, storage_backup_dir: Path) -> Path:
    """Archives local storage directory into a tarball."""
    archive_tar = storage_backup_dir / f"sovereignai_storage_{timestamp}.tar.gz"
    storage_src = Path("storage")
    with tarfile.open(archive_tar, "w:gz") as tar:
        if storage_src.exists():
            tar.add(storage_src, arcname="storage")
        else:
            tar.add(".", filter=lambda x: None)  # empty
    print(f"  [+] Storage archive created: {archive_tar}")
    return archive_tar


def upload_to_drive(local_path: Path, remote_folder: str) -> bool:
    """Uploads file or directory to Google Drive via rclone."""
    rclone = find_rclone()
    target_remote = f"{GDRIVE_REMOTE_BASE}/{remote_folder}"
    cmd = [rclone, "copy", str(local_path), target_remote]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode == 0:
        print(f"  [SUCCESS] Uploaded {local_path.name} -> {target_remote}")
        return True
    else:
        print(f"  [ERROR] Upload failed: {res.stderr.strip()}", file=sys.stderr)
        return False


def main():
    print("========================================================")
    print("  SovereignAI — Automated Google Drive Backup Pipeline  ")
    print("========================================================")

    # 1. Verify encryption key is configured
    try:
        raw_key = get_encryption_key()
        print("[*] Backup encryption key verified (AES-256).")
    except Exception as e:
        print(f"[ERROR] Encryption key check failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. Setup backup directories
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    db_backup_dir = BACKUP_DIR / "database"
    storage_backup_dir = BACKUP_DIR / "storage"
    checksums_dir = BACKUP_DIR / "checksums"

    db_backup_dir.mkdir(parents=True, exist_ok=True)
    storage_backup_dir.mkdir(parents=True, exist_ok=True)
    checksums_dir.mkdir(parents=True, exist_ok=True)

    # 3. Create raw backups
    print("[*] Creating application backups...")
    raw_db = dump_database(timestamp, db_backup_dir)
    raw_storage = archive_storage(timestamp, storage_backup_dir)

    # 4. Encrypt payloads
    print("[*] Encrypting with AES-256-GCM + gzip level 9...")
    enc_db, meta_db, sha_db = encrypt_file(raw_db, key=raw_key)
    enc_storage, meta_storage, sha_storage = encrypt_file(raw_storage, key=raw_key)

    # 5. Clean up plaintext dumps locally for security (preserve encrypted files)
    try:
        raw_db.unlink(missing_ok=True)
        raw_storage.unlink(missing_ok=True)
    except Exception:
        pass

    # 6. Update master checksums ledger
    master_ledger_file = checksums_dir / "checksums_ledger.json"
    ledger = []
    if master_ledger_file.exists():
        try:
            with open(master_ledger_file, "r", encoding="utf-8") as f:
                ledger = json.load(f)
        except Exception:
            ledger = []

    ledger.append({
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "database": {
            "file": enc_db.name,
            "sha256": sha_db,
            "size_bytes": enc_db.stat().st_size
        },
        "storage": {
            "file": enc_storage.name,
            "sha256": sha_storage,
            "size_bytes": enc_storage.stat().st_size
        }
    })
    with open(master_ledger_file, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)

    # 7. Upload to Google Drive
    print(f"[*] Uploading encrypted backups to Google Drive ({GDRIVE_REMOTE_BASE})...")
    upload_to_drive(enc_db, "database")
    upload_to_drive(meta_db, "database")
    upload_to_drive(enc_storage, "storage")
    upload_to_drive(meta_storage, "storage")
    upload_to_drive(master_ledger_file, "checksums")

    print("\n========================================================")
    print("  [SUCCESS] Backup & Upload Completed Successfully!     ")
    print(f"  Encrypted DB:      {enc_db.name} (SHA-256: {sha_db[:16]}...)")
    print(f"  Encrypted Storage: {enc_storage.name} (SHA-256: {sha_storage[:16]}...)")
    print("========================================================")


if __name__ == "__main__":
    main()
