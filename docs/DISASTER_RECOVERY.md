# SovereignAI — Enterprise Disaster Recovery Runbook

This document defines the exact, deterministic procedure for rebuilding the entire SovereignAI application on a completely new machine, assuming the original machine was lost or wiped.

---

## 1. Disaster Scenario & Operating Assumptions

- **Scenario**: Original workstation is destroyed, formatted, or unreachable.
- **Available Assets**:
  1. Private GitHub Repository: `https://github.com/pankajcseaiml/SovereignAI`
  2. KeePassXC master password (memorized by administrator).
  3. Google Drive remote storage (`gdrive:Projects/SovereignAI/`).
- **Target Machine**: Clean computer with Windows 11 or Linux.

---

## 2. Step-by-Step Cold-Machine Rebuild Procedure

### Phase 1: Machine Provisioning & Prerequisites
Install base dependencies on the new computer:
1. **Git**: `winget install Git.Git` or `apt install git`
2. **Docker Desktop**: `winget install Docker.DockerDesktop`
3. **Python 3.11+**: `winget install Python.Python.3.11`
4. **KeePassXC**: `winget install KeePassXCTeam.KeePassXC`
5. **rclone**: `winget install Rclone.Rclone`

---

### Phase 2: Clone Clean Repository
```bash
git clone https://github.com/pankajcseaiml/SovereignAI.git
cd SovereignAI
```

---

### Phase 3: Secret Recovery via KeePassXC
1. Copy your secure `.kdbx` vault file to:
   `%USERPROFILE%\Documents\SovereignAI_Secrets.kdbx`
2. Run the automated environment generator:
   ```bash
   scripts\generate_env.bat
   ```
   You will be prompted for your KeePassXC master password. The `.env` file will be generated locally without printing any secrets to the screen.

---

### Phase 4: Download & Decrypt Backups from Google Drive
1. Authenticate `rclone`:
   ```bash
   rclone config
   # Select Google Drive remote named 'gdrive'
   ```
2. Execute automated restoration:
   ```bash
   scripts\restore_from_drive.bat
   ```
   This script:
   - Downloads the latest encrypted database backup (`sovereignai_db_*.sql.enc`).
   - Downloads the latest encrypted storage archive (`sovereignai_storage_*.tar.gz.enc`).
   - Verifies SHA-256 integrity hashes against Google Drive ledgers.
   - Decrypts both payloads using the `BACKUP_ENCRYPTION_KEY` from KeePassXC.
   - Extracts storage files into `storage/`.

---

### Phase 5: Container Build & Startup
1. Start Docker containers:
   ```bash
   scripts\start.bat
   ```
2. Verify all 8 services become healthy:
   ```bash
   scripts\status.bat
   ```

---

### Phase 6: Model Download
Pull the open-weight LLM weights into the Ollama container:
```bash
python scripts\download_models.py --model qwen2.5:0.5b
```

---

### Phase 7: Verification & Sign-Off
Run the automated verification suite:
```bash
scripts\verify.bat
```
Confirm:
- [x] Zero secret leaks detected.
- [x] Database tables and seed records verified.
- [x] Backend `/health` endpoint returns 200 OK.
- [x] Web frontend loads on `http://localhost:3000`.
- [x] LangGraph ReAct agent responds to industrial queries.

---

## 3. Disaster Recovery Verification Guarantee

This procedure has been validated via an isolated clean-clone sandbox test. No hidden files, credentials, or caches from the development machine are required for complete recovery.
