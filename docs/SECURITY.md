# SovereignAI — Enterprise Security & Secret Management Policy

## 1. Zero Secret Exposure Mandate (Rule 2)

Under no circumstances may credentials, tokens, or encryption keys be:
- Printed to terminal standard output (stdout) or standard error (stderr).
- Committed or tracked in Git history or git branches.
- Uploaded in plaintext to cloud storage.
- Baked into Docker images, layers, or build arguments.

---

## 2. Secret Separation Architecture

Secrets are strictly partitioned across three domains:

1. **GitHub Repository**: Contains source code, Docker configs, documentation, and safe templates (`.env.example`). NEVER contains real secrets.
2. **KeePassXC Vault (`SovereignAI_Secrets.kdbx`)**: Encrypted using Argon2d key derivation and AES-256 cipher. Stores all runtime passwords, database credentials, and backup keys. Located strictly outside the repository scope.
3. **Local Runtime `.env`**: Generated on-demand on the local host by `scripts/generate_env.bat` and consumed by Docker at runtime. Git-ignored.

---

## 3. Cryptographic Standards

- **Backup Encryption**: AES-256 in Galois/Counter Mode (AES-GCM), providing authenticated encryption with associated data (AEAD).
- **Integrity**: SHA-256 cryptographic hashes accompany every encrypted payload.
- **Tamper Resistance**: Modifying any byte in an encrypted file invalidates the GCM authentication tag, causing immediate rejection of the backup.
- **Password Hashing**: Bcrypt with minimum work factor 12 for stored application users.
- **JWT Signing**: HMAC-SHA256 with 256-bit cryptographically random key.

---

## 4. Pre-Commit Security Gate (Rule 37)

Before any commit or push, the automated scanner `scripts/scan_secrets.py` must execute cleanly:
```bash
python scripts\scan_secrets.py
```
If any pattern matching private keys, API keys, or embedded database URLs is detected, the operation is blocked.
