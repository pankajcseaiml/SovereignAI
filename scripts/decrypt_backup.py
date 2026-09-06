"""
SovereignAI — Authenticated Backup Decryptor
Validates SHA-256 checksum, authenticates AES-256-GCM tag, decrypts, and decompresses.
"""

import os
import sys
import gzip
import json
import hashlib
from pathlib import Path
from typing import Optional

from encrypt_backup import MAGIC_HEADER, get_encryption_key

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.exceptions import InvalidTag
except ImportError:
    print("[ERROR] cryptography library is required. Install via 'pip install cryptography'", file=sys.stderr)
    sys.exit(1)


def decrypt_file(
    encrypted_path: Path,
    output_path: Optional[Path] = None,
    key: Optional[bytes] = None,
    verify_meta: bool = True
) -> Path:
    """
    Decrypts an authenticated AES-256-GCM encrypted backup file.
    Validates integrity and restores original data.
    """
    if not encrypted_path.exists():
        raise FileNotFoundError(f"Encrypted file not found: {encrypted_path}")

    raw_key = key or get_encryption_key()

    # 1. Read encrypted file
    with open(encrypted_path, "rb") as f:
        data = f.read()

    # 2. Check SHA-256 if metadata file exists
    meta_path = encrypted_path.with_name(f"{encrypted_path.name}.meta.json")
    if verify_meta and meta_path.exists():
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        actual_hash = hashlib.sha256(data).hexdigest().upper()
        expected_hash = meta.get("sha256_checksum", "").upper()
        if expected_hash and actual_hash != expected_hash:
            raise ValueError(f"Checksum mismatch! Expected {expected_hash}, got {actual_hash}. File may be corrupted.")

    # 3. Verify magic header
    header_len = len(MAGIC_HEADER)
    if len(data) < header_len + 12 + 16:  # header + nonce (12) + tag (16)
        raise ValueError("Invalid encrypted file: payload is too short.")

    if data[:header_len] != MAGIC_HEADER:
        raise ValueError(f"Invalid magic header. Expected '{MAGIC_HEADER.decode()}', got '{data[:header_len]}'")

    # 4. Extract nonce and ciphertext
    nonce = data[header_len:header_len + 12]
    ciphertext = data[header_len + 12:]

    # 5. Determine source filename for AAD
    source_filename = None
    if meta_path.exists():
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                source_filename = json.load(f).get("source_file")
        except Exception:
            pass

    if not source_filename:
        # Infer source filename: remove .enc
        base_name = encrypted_path.name
        if base_name.endswith(".enc"):
            source_filename = base_name[:-4]
        else:
            source_filename = base_name + ".restored"

    # 6. Authenticate and decrypt with AES-GCM
    aesgcm = AESGCM(raw_key)
    aad = MAGIC_HEADER + source_filename.encode("utf-8")
    try:
        compressed_data = aesgcm.decrypt(nonce, ciphertext, aad)
    except InvalidTag:
        # Fallback with empty AAD in case AAD was not bound
        try:
            compressed_data = aesgcm.decrypt(nonce, ciphertext, None)
        except InvalidTag:
            raise ValueError("Decryption failed! Authentication tag verification failed. Invalid key or corrupted data.")

    # 7. Gzip decompress
    try:
        decompressed_data = gzip.decompress(compressed_data)
    except Exception as e:
        raise ValueError(f"Gzip decompression failed: {e}")

    # 8. Determine destination path
    if output_path is None:
        if encrypted_path.name.endswith(".enc"):
            output_path = encrypted_path.with_name(encrypted_path.name[:-4])
        else:
            output_path = encrypted_path.with_name(f"{encrypted_path.name}.decrypted")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(decompressed_data)

    return output_path


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SovereignAI Authenticated Backup Decryptor")
    parser.add_argument("input", help="Encrypted .enc file to decrypt")
    parser.add_argument("--output", "-o", help="Restored output file path")
    parser.add_argument("--key", "-k", help="Hexadecimal AES-256 key (optional)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    try:
        restored = decrypt_file(input_path, output_path, None)
        print(f"[SUCCESS] File decrypted and restored successfully:")
        print(f"  Restored file: {restored}")
    except Exception as e:
        print(f"[ERROR] Decryption failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
