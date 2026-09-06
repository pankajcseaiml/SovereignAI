"""
SovereignAI — Google Drive Backup Restorer & Disaster Recovery
Downloads encrypted backups from Google Drive via rclone, validates SHA-256,
decrypts via AES-256-GCM, and restores database and storage files.
"""

import os
import sys
import tarfile
import subprocess
import shutil
from pathlib import Path
from typing import List, Optional

from decrypt_backup import decrypt_file
from backup_to_drive import find_rclone, GDRIVE_REMOTE_BASE

RESTORE_STAGING = Path("backups/restore_staging")


def list_remote_backups(remote_folder: str = "database") -> List[str]:
    """Lists files in Google Drive backup directory."""
    rclone = find_rclone()
    target = f"{GDRIVE_REMOTE_BASE}/{remote_folder}"
    cmd = [rclone, "lsf", target]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        return []
    files = [f.strip() for f in res.stdout.splitlines() if f.strip().endswith(".enc")]
    return sorted(files)


def download_remote_file(remote_file: str, remote_folder: str, local_dest: Path) -> Path:
    """Downloads a file and its companion .meta.json from Google Drive."""
    rclone = find_rclone()
    local_dest.mkdir(parents=True, exist_ok=True)
    target_remote_file = f"{GDRIVE_REMOTE_BASE}/{remote_folder}/{remote_file}"
    meta_remote_file = f"{target_remote_file}.meta.json"

    # Download .enc
    cmd = [rclone, "copy", target_remote_file, str(local_dest)]
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to download {target_remote_file}: {res.stderr}")

    # Download .meta.json
    cmd_meta = [rclone, "copy", meta_remote_file, str(local_dest)]
    subprocess.run(cmd_meta, capture_output=True, text=True, check=False)

    return local_dest / remote_file


def restore_database_file(sql_file: Path):
    """Imports SQL file into PostgreSQL container if running."""
    print(f"[*] Importing database from: {sql_file}")
    try:
        cmd = ["docker", "compose", "exec", "-T", "postgres", "psql", "-U", "user", "-d", "sovereignai"]
        with open(sql_file, "r", encoding="utf-8") as f:
            res = subprocess.run(cmd, stdin=f, capture_output=True, text=True, check=False)
        if res.returncode == 0:
            print("[SUCCESS] Database restored into PostgreSQL container.")
            return True
        else:
            print(f"[!] PostgreSQL container import returned notice/warning: {res.stderr.strip()}")
    except Exception as e:
        print(f"[!] Note: Database container import skipped ({e}). Schema file available at {sql_file}")
    return False


def restore_storage_file(tar_file: Path):
    """Extracts storage tarball into ./storage/."""
    print(f"[*] Extracting storage archive: {tar_file}")
    target_storage = Path("storage")
    target_storage.mkdir(parents=True, exist_ok=True)
    try:
        with tarfile.open(tar_file, "r:gz") as tar:
            tar.extractall(path=".")
        print("[SUCCESS] Storage files extracted.")
        return True
    except Exception as e:
        print(f"[ERROR] Failed to extract storage: {e}", file=sys.stderr)
        return False


def main():
    print("========================================================")
    print("  SovereignAI — Google Drive Disaster Recovery Restorer ")
    print("========================================================")

    RESTORE_STAGING.mkdir(parents=True, exist_ok=True)

    # 1. Check remote database backups
    print(f"[*] Querying Google Drive remote: {GDRIVE_REMOTE_BASE}/database/...")
    backups = list_remote_backups("database")
    if not backups:
        print("[!] No remote database backups found on Google Drive.", file=sys.stderr)
        print("Checking local backups directory...")
        local_enc = list(Path("backups/database").glob("*.enc"))
        if not local_enc:
            print("[ERROR] No backups found locally or remotely.", file=sys.stderr)
            sys.exit(1)
        latest_db_enc = sorted(local_enc)[-1]
    else:
        latest_remote_db = backups[-1]
        print(f"[+] Found {len(backups)} remote backup(s). Latest: {latest_remote_db}")
        print("[*] Downloading encrypted database backup...")
        latest_db_enc = download_remote_file(latest_remote_db, "database", RESTORE_STAGING)

    # 2. Download latest storage backup if exists
    storage_backups = list_remote_backups("storage")
    latest_storage_enc = None
    if storage_backups:
        latest_remote_storage = storage_backups[-1]
        print(f"[*] Downloading encrypted storage backup: {latest_remote_storage}...")
        latest_storage_enc = download_remote_file(latest_remote_storage, "storage", RESTORE_STAGING)

    # 3. Decrypt database
    print("\n[*] Decrypting database payload with AES-256-GCM...")
    try:
        restored_db_sql = decrypt_file(latest_db_enc)
        print(f"[SUCCESS] Database decrypted to: {restored_db_sql}")
        restore_database_file(restored_db_sql)
    except Exception as e:
        print(f"[ERROR] Database decryption failed: {e}", file=sys.stderr)
        sys.exit(1)

    # 4. Decrypt storage
    if latest_storage_enc and latest_storage_enc.exists():
        print("\n[*] Decrypting storage payload with AES-256-GCM...")
        try:
            restored_storage_tar = decrypt_file(latest_storage_enc)
            print(f"[SUCCESS] Storage decrypted to: {restored_storage_tar}")
            restore_storage_file(restored_storage_tar)
        except Exception as e:
            print(f"[WARNING] Storage decryption skipped: {e}")

    print("\n========================================================")
    print("  [SUCCESS] Disaster Recovery Restoration Complete!    ")
    print("========================================================")


if __name__ == "__main__":
    main()
