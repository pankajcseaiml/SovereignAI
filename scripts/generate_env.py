"""
SovereignAI — Generate .env from KeePassXC Vault
Safely reconstructs the local environment file without printing secrets to the terminal.
"""

import os
import sys
import getpass
from pathlib import Path
from keepass_manager import DEFAULT_DB_PATH, export_env_file

def main():
    target_env = Path(".env")
    db_path = DEFAULT_DB_PATH
    
    if len(sys.argv) > 1:
        target_env = Path(sys.argv[1])
        
    print(f"[*] Reconstructing environment from KeePassXC vault: {db_path}")
    if not db_path.exists():
        print(f"[ERROR] KeePassXC vault not found at: {db_path}")
        print("Please run scripts\\init_keepass.bat first.")
        sys.exit(1)
        
    password = os.getenv("SOVEREIGN_VAULT_PASSWORD")
    if not password:
        password = getpass.getpass("Enter KeePassXC Master Password: ")
        
    success = export_env_file(db_path, password, target_env)
    if success:
        print(f"[SUCCESS] Environment reconstructed at: {target_env.resolve()}")
    else:
        print("[ERROR] Failed to reconstruct environment.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
