"""
SovereignAI — KeePassXC Enterprise Secret Manager
Integrates with keepassxc-cli to manage application credentials securely.
Strictly adheres to Zero Secret Exposure: Secret values are never printed to console.
"""

import os
import sys
import getpass
import secrets
import argparse
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

DEFAULT_KEEPASS_CLI = r"C:\Program Files\KeePassXC\keepassxc-cli.exe"
DEFAULT_DB_PATH = Path.home() / "Documents" / "SovereignAI_Secrets.kdbx"
GROUP_NAME = "SovereignAI"

REQUIRED_VARS = [
    "APP_ENV",
    "DATABASE_URL",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "POSTGRES_DB",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "QDRANT_HOST",
    "QDRANT_PORT",
    "REDIS_URL",
    "AI_ENGINE_URL",
    "MODEL_SERVER_URL",
    "STORAGE_PATH",
    "JWT_SECRET",
    "LOG_LEVEL",
    "BACKUP_ENCRYPTION_KEY",
]


def find_keepass_cli() -> str:
    """Locates the keepassxc-cli executable."""
    env_cli = os.getenv("KEEPASSXC_CLI")
    if env_cli and Path(env_cli).exists():
        return env_cli
    if Path(DEFAULT_KEEPASS_CLI).exists():
        return DEFAULT_KEEPASS_CLI
    import shutil
    cli_on_path = shutil.which("keepassxc-cli")
    if cli_on_path:
        return cli_on_path
    raise FileNotFoundError(
        f"keepassxc-cli not found. Expected at '{DEFAULT_KEEPASS_CLI}' or in PATH."
    )


def run_cli(args: List[str], stdin_data: Optional[str] = None):
    """Runs keepassxc-cli without echoing sensitive data."""
    cli = find_keepass_cli()
    cmd = [cli] + args
    res = subprocess.run(cmd, input=stdin_data, capture_output=True, text=True, check=False)
    return res.returncode, res.stdout, res.stderr


def init_database(db_path: Path, password: str) -> bool:
    """Initializes KeePassXC database and populates with current secrets from .env."""
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # 1. Create DB if not exists
    if not db_path.exists():
        print(f"[*] Creating new KeePassXC database at: {db_path}")
        rc, out, err = run_cli(["db-create", "-p", str(db_path)], stdin_data=f"{password}\n{password}\n")
        if rc != 0:
            print(f"[ERROR] Failed to create KeePassXC database: {err}", file=sys.stderr)
            return False
        print("[SUCCESS] KeePassXC database initialized.")
    else:
        print(f"[*] KeePassXC database exists at: {db_path}")

    # 2. Create Group
    run_cli(["mkdir", str(db_path), GROUP_NAME], stdin_data=f"{password}\n")

    # 3. Read .env if present
    env_vars = {}
    if Path(".env").exists():
        with open(".env", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    env_vars[k.strip()] = v.strip()

    # Ensure BACKUP_ENCRYPTION_KEY exists
    if not env_vars.get("BACKUP_ENCRYPTION_KEY"):
        gen_key = secrets.token_hex(32)
        env_vars["BACKUP_ENCRYPTION_KEY"] = gen_key
        with open(".env", "a", encoding="utf-8") as f:
            f.write(f"\nBACKUP_ENCRYPTION_KEY={gen_key}\n")
        print("  [+] Generated new AES-256 BACKUP_ENCRYPTION_KEY and saved to .env")

    # 4. Insert each secret
    stored_count = 0
    for k in REQUIRED_VARS:
        val = env_vars.get(k, "")
        if not val:
            continue
        entry_path = f"{GROUP_NAME}/{k}"
        # Remove existing
        run_cli(["rm", str(db_path), entry_path], stdin_data=f"{password}\n")
        # Add new entry (prompts for db password then entry password twice)
        rc, out, err = run_cli(
            ["add", "-u", "Admin", "-p", str(db_path), entry_path],
            stdin_data=f"{password}\n{val}\n{val}\n"
        )
        if rc == 0:
            print(f"  [STORED] {k} -> {entry_path}")
            stored_count += 1
        else:
            print(f"  [WARNING] Could not store {k}: {err.strip()}")

    print(f"\n[SUCCESS] Stored {stored_count} secrets safely in {db_path}")
    return True


def get_secret(db_path: Path, password: str, key: str) -> Optional[str]:
    """Retrieves secret value silently from the database."""
    entry_path = f"{GROUP_NAME}/{key}"
    rc, out, err = run_cli(
        ["show", "-s", "-a", "password", str(db_path), entry_path],
        stdin_data=f"{password}\n"
    )
    if rc == 0:
        return out.strip()
    return None


def export_env_file(db_path: Path, password: str, target_file: Path) -> bool:
    """Regenerates .env locally from KeePassXC without printing secrets."""
    print(f"[*] Reading secrets from KeePassXC vault: {db_path}")
    lines = [
        "# =============================================================================",
        "# SovereignAI Environment Configuration",
        "# AUTO-GENERATED FROM SECURE KEEPASSXC DATABASE",
        "# NEVER COMMIT THIS FILE TO GIT",
        "# =============================================================================",
        ""
    ]
    retrieved = 0
    for k in REQUIRED_VARS:
        val = get_secret(db_path, password, k)
        if val is not None:
            lines.append(f"{k}={val}")
            print(f"  [RETRIEVED] {k}")
            retrieved += 1
        else:
            print(f"  [MISSING] {k} not found in vault")

    with open(target_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[SUCCESS] Wrote {retrieved} configuration variables to: {target_file}")
    return retrieved > 0


def verify_keepass(db_path: Path, password: str) -> bool:
    """Verifies entries in KeePassXC vault."""
    rc, out, err = run_cli(["ls", "-R", str(db_path), GROUP_NAME], stdin_data=f"{password}\n")
    if rc != 0:
        print(f"[ERROR] Cannot open KeePassXC database: {err}")
        return False
    print(f"[SUCCESS] Group '{GROUP_NAME}' verified. Entries in vault:")
    for line in out.splitlines():
        line = line.strip()
        if line:
            print(f"  - {line}")
    return True


def main():
    parser = argparse.ArgumentParser(description="SovereignAI KeePassXC Secret Manager")
    parser.add_argument("command", choices=["init", "import-env", "export-env", "list", "verify"],
                        help="Action to perform")
    parser.add_argument("--db", default=str(DEFAULT_DB_PATH), help="Path to .kdbx file")
    parser.add_argument("--env", default=".env", help="Path to .env file")
    parser.add_argument("--password", help="Master password (optional)")
    args = parser.parse_args()

    db_path = Path(args.db)

    password = args.password or os.getenv("SOVEREIGN_VAULT_PASSWORD") or os.getenv("KEEPASS_MASTER_PASSWORD")
    if not password:
        password = getpass.getpass("Enter KeePassXC Master Password: ")

    if args.command in ["init", "import-env"]:
        init_database(db_path, password)
    elif args.command == "export-env":
        export_env_file(db_path, password, Path(args.env))
    elif args.command in ["list", "verify"]:
        verify_keepass(db_path, password)


if __name__ == "__main__":
    main()
