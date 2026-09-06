# SovereignAI — Google Drive Backup Architecture

## 1. Remote Structure

Backups are synchronized to Google Drive under the remote prefix:
`gdrive:Projects/SovereignAI/`

```text
Projects/SovereignAI/
├── database/
│   ├── sovereignai_db_20260906_120000.sql.enc
│   ├── sovereignai_db_20260906_120000.sql.enc.meta.json
│   └── ...
├── storage/
│   ├── sovereignai_storage_20260906_120000.tar.gz.enc
│   ├── sovereignai_storage_20260906_120000.tar.gz.enc.meta.json
│   └── ...
└── checksums/
    └── checksums_ledger.json
```

---

## 2. Backup Pipeline Workflow

```text
PostgreSQL Dump / Storage Folder
              ↓
   gzip Level 9 Compression
              ↓
  AES-256-GCM AEAD Encryption
              ↓
 SHA-256 Checksum Calculation
              ↓
   rclone Upload to Google Drive
              ↓
Remote File Existence Verification
```

---

## 3. Automation Scripts

| Script | Purpose | Command |
|---|---|---|
| `backup_to_drive.bat` | Performs complete dump, encrypt, and upload | `scripts\backup_to_drive.bat` |
| `restore_from_drive.bat` | Downloads and decrypts latest cloud backup | `scripts\restore_from_drive.bat` |
| `verify_backup.bat` | Validates local and remote SHA-256 checksums | `scripts\verify_backup.bat` |
| `encrypt_backup.py` | Standalone file encryption tool | `python scripts\encrypt_backup.py <file>` |
| `decrypt_backup.py` | Standalone file decryption tool | `python scripts\decrypt_backup.py <file.enc>` |

---

## 4. Multi-Version Retention Policy

- Backups are timestamped (`YYYYMMDD_HHMMSS`).
- Historical backups are never automatically deleted by sync scripts.
- To audit existing cloud backups, run `rclone lsf gdrive:Projects/SovereignAI/database/`.
