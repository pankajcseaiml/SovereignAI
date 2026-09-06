"""
SovereignAI — Authenticated Backup Encryptor
Pure Python: gzip level 9 compression + AES-256-GCM authenticated encryption + SHA-256 hash.
Magic Header: SOVA_ENC_V1
"""

import os
import sys
import gzip
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Tuple

MAGIC_HEADER = b"SOVA_ENC_V1"  # 11 bytes

import secrets

def generate_aes256_key() -> str:
    """Generates a cryptographically secure 256-bit (32-byte hex) key."""
    return secrets.token_hex(32)

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except ImportError:
    print("[ERROR] cryptography library is required. Install via 'pip install cryptography'", file=sys.stderr)
    sys.exit(1)


def get_encryption_key(cli_key: Optional[str] = None) -> bytes:
    """Retrieves 32-byte (256-bit) encryption key from CLI, environment, or .env file."""
    key_hex = cli_key or os.getenv("BACKUP_ENCRYPTION_KEY")
    if not key_hex and Path(".env").exists():
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("BACKUP_ENCRYPTION_KEY="):
                    key_hex = line.split("=", 1)[1].strip()
                    break

    if not key_hex:
        raise ValueError(
            "Missing BACKUP_ENCRYPTION_KEY. Set in environment, pass --key, or configure in .env / KeePassXC."
        )

    # Normalize key (strip quotes if present)
    key_hex = key_hex.strip("\"' ")
    try:
        raw_key = bytes.fromhex(key_hex)
    except ValueError:
        raise ValueError("BACKUP_ENCRYPTION_KEY must be a valid 64-character hexadecimal string (32 bytes).")

    if len(raw_key) != 32:
        raise ValueError(f"BACKUP_ENCRYPTION_KEY must be exactly 32 bytes (64 hex chars). Got {len(raw_key)} bytes.")

    return raw_key


def encrypt_file(
    input_path: Path,
    output_path: Optional[Path] = None,
    key: Optional[bytes] = None
) -> Tuple[Path, Path, str]:
    """
    Compresses with gzip (level 9), encrypts with AES-256-GCM, and computes SHA-256.
    Returns: (encrypted_file_path, metadata_file_path, sha256_hex)
    """
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    raw_key = key or get_encryption_key()

    if output_path is None:
        output_path = input_path.with_name(f"{input_path.name}.enc")

    # 1. Read input data
    with open(input_path, "rb") as f:
        plaintext = f.read()
    orig_size = len(plaintext)

    # 2. Gzip compress
    compressed_data = gzip.compress(plaintext, compresslevel=9)

    # 3. Generate 12-byte random nonce for AES-GCM
    nonce = os.urandom(12)

    # 4. Encrypt with AESGCM (appends 16-byte authentication tag automatically)
    aesgcm = AESGCM(raw_key)
    # Additional authenticated data (AAD) binds the header and filename to ciphertext
    aad = MAGIC_HEADER + input_path.name.encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, compressed_data, aad)

    # 5. Pack: MAGIC_HEADER (11 bytes) + NONCE (12 bytes) + CIPHERTEXT+TAG
    encrypted_payload = MAGIC_HEADER + nonce + ciphertext

    # 6. Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(encrypted_payload)
    enc_size = len(encrypted_payload)

    # 7. Compute SHA-256
    sha256_hash = hashlib.sha256(encrypted_payload).hexdigest().upper()

    # 8. Write metadata ledger
    meta_path = output_path.with_name(f"{output_path.name}.meta.json")
    metadata = {
        "source_file": input_path.name,
        "encrypted_file": output_path.name,
        "original_size_bytes": orig_size,
        "encrypted_size_bytes": enc_size,
        "compression_ratio": round((1 - (enc_size / orig_size)) * 100, 2) if orig_size > 0 else 0,
        "sha256_checksum": sha256_hash,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "algorithm": "AES-256-GCM",
        "compression": "gzip-9",
        "magic_header": MAGIC_HEADER.decode("utf-8"),
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    return output_path, meta_path, sha256_hash


def main():
    import argparse
    parser = argparse.ArgumentParser(description="SovereignAI Authenticated Backup Encryptor")
    parser.add_argument("input", help="File to encrypt")
    parser.add_argument("--output", "-o", help="Output .enc file path")
    parser.add_argument("--key", "-k", help="Hexadecimal AES-256 key (optional)")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None

    try:
        enc_file, meta_file, sha256 = encrypt_file(input_path, output_path, None)
        print(f"[SUCCESS] Encrypted payload created:")
        print(f"  File:     {enc_file}")
        print(f"  Metadata: {meta_file}")
        print(f"  SHA-256:  {sha256}")
    except Exception as e:
        print(f"[ERROR] Encryption failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
