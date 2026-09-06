import os
import sys
import pytest
from pathlib import Path

scripts_dir = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(scripts_dir) not in sys.path:
    sys.path.insert(0, str(scripts_dir))

from encrypt_backup import encrypt_file, generate_aes256_key
from decrypt_backup import decrypt_file


def test_encryption_decryption_roundtrip(tmp_path: Path):
    """Verify that a file can be encrypted and restored with 100% byte-exact fidelity."""
    test_key_hex = generate_aes256_key()
    raw_key = bytes.fromhex(test_key_hex)

    # Create dummy source file
    sample_data = b"SovereignAI Confidential Industrial Telemetry Dump - Valve 450 PSI Nominal" * 50
    source_file = tmp_path / "sample_telemetry.sql"
    source_file.write_bytes(sample_data)

    # Encrypt
    enc_file, meta_file, sha256_hash = encrypt_file(source_file, key=raw_key)
    assert enc_file.exists()
    assert meta_file.exists()
    assert len(sha256_hash) == 64

    # Decrypt
    restored_file = tmp_path / "sample_telemetry_restored.sql"
    decrypted_path = decrypt_file(enc_file, output_path=restored_file, key=raw_key)

    assert decrypted_path.exists()
    assert decrypted_path.read_bytes() == sample_data


def test_tampered_ciphertext_detection(tmp_path: Path):
    """Verify that any modification to encrypted payload causes AES-GCM authentication failure."""
    raw_key = bytes.fromhex(generate_aes256_key())

    source_file = tmp_path / "original.txt"
    source_file.write_bytes(b"Top secret industrial model weights and configurations")

    enc_file, _, _ = encrypt_file(source_file, key=raw_key)

    # Tamper with a byte in ciphertext
    corrupted_data = bytearray(enc_file.read_bytes())
    # Flip the last byte (part of authentication tag or ciphertext)
    corrupted_data[-1] ^= 0xFF
    corrupted_file = tmp_path / "corrupted.txt.enc"
    corrupted_file.write_bytes(corrupted_data)

    # Decryption must raise ValueError due to authentication failure
    with pytest.raises(ValueError, match="Decryption failed|Checksum mismatch"):
        decrypt_file(corrupted_file, key=raw_key, verify_meta=False)


def test_wrong_key_rejection(tmp_path: Path):
    """Verify that attempting decryption with an incorrect key fails securely."""
    key_correct = bytes.fromhex(generate_aes256_key())
    key_wrong = bytes.fromhex(generate_aes256_key())

    source_file = tmp_path / "secret.txt"
    source_file.write_bytes(b"Mission critical data")

    enc_file, _, _ = encrypt_file(source_file, key=key_correct)

    with pytest.raises(ValueError, match="Decryption failed"):
        decrypt_file(enc_file, key=key_wrong, verify_meta=False)
