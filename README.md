# SovereignAI

**Sovereign On-Premise Agentic AI Workbench using Open-Weight Multimodal LLMs for Confidential Industrial Work.**

SovereignAI provides an enterprise-ready, self-hosted AI operating environment designed for air-gapped or high-security facilities. It features a Next.js 16 operator workspace, FastAPI async backend, Celery task execution, LangGraph agent workflows, Qdrant vector retrieval, Redis state synchronization, and local Ollama model inference.

---

## 1. Target Enterprise Architecture

The project adheres to a strict separation of concerns across five pillars:

```text
┌─────────────────────────────────────────────────────────────┐
│               SOVEREIGN-AI TARGET ARCHITECTURE              │
└─────────────────────────────────────────────────────────────┘
                               │
       ┌───────────────────────┼────────────────────────┐
       ▼                       ▼                        ▼
┌───────────────┐      ┌───────────────┐       ┌─────────────────┐
│ PRIVATE GITHUB│      │   KEEPASSXC   │       │  GOOGLE DRIVE   │
│               │      │               │       │                 │
│ Source Code   │      │ DB Password   │       │ AES-256-GCM     │
│ Tests & Docs  │      │ JWT Secret    │       │ Encrypted DB    │
│ Migrations    │      │ Redis URL     │       │ Backups &       │
│ Dockerfiles   │      │ AES-256 Key   │       │ SHA-256         │
│ Compose specs │      │ (.kdbx file   │       │ Integrity       │
│ Scripts       │      │ outside repo) │       │ Manifests       │
└───────────────┘      └───────────────┘       └─────────────────┘
       │                                                │
       ▼                                                ▼
┌───────────────┐                              ┌─────────────────┐
│ DOCKER ENGINE │                              │ DISASTER RECOV. │
│ Reproducible  │                              │ Cold-machine    │
│ containers &  │                              │ clean-clone     │
│ volumes       │                              │ 100% verified   │
└───────────────┘                              └─────────────────┘
```

---

## 2. Directory Structure

```text
SovereignAI/
├── backend/                  # FastAPI async backend service
│   ├── app/                  # Application core, models, schemas, AI tools
│   ├── Dockerfile            # Hardened Python 3.11 container with health check
│   └── requirements.txt      # Pinned Python dependencies
├── frontend/                 # Next.js 16 + React 19 UI
│   ├── src/                  # App router, workspace UI, components, hooks
│   └── Dockerfile            # Node 20 container definition
├── ai-engine/                # Multimodal agents & RAG workers
│   └── Dockerfile            # Python AI microservice container
├── database/                 # Database DDL schema and initial seeds
│   └── schema.sql            # PostgreSQL 16 schema & industrial demo records
├── storage/                  # Local uploads, processed files, quarantine
├── scripts/                  # Automated lifecycle, backup, and secret scripts
│   ├── setup.bat / .sh       # One-click environment bootstrap
│   ├── start.bat / .sh       # Start Docker Compose services
│   ├── stop.bat / .sh        # Graceful shutdown (preserves data)
│   ├── status.bat / .sh      # Check container and volume health
│   ├── verify.bat / .sh      # Run end-to-end verification audit
│   ├── keepass_manager.py    # KeePassXC secret management CLI
│   ├── generate_env.bat      # Reconstruct .env from KeePassXC vault
│   ├── backup_to_drive.bat   # Dump -> Compress -> Encrypt -> Upload
│   ├── restore_from_drive.bat# Download -> Decrypt -> Restore
│   ├── verify_backup.bat     # Validate SHA-256 checksums & AES keys
│   └── scan_secrets.py       # Pre-commit secret scanning gate
├── docs/                     # Comprehensive enterprise documentation
│   ├── DISASTER_RECOVERY.md  # Cold-machine rebuild runbook
│   ├── SECURITY.md           # Zero-secret exposure policy
│   ├── GOOGLE_DRIVE_BACKUP.md# rclone & encryption specifications
│   └── DOCKER_GUIDE.md       # Container networking & volumes
├── .env.example              # Safe environment variable template
├── .gitignore                # Hardened git exclusion rules
├── .dockerignore             # Image build exclusion rules
└── docker-compose.yml        # Multi-container orchestration
```

---

## 3. Prerequisites

- **Docker Desktop** (with WSL2 Linux engine on Windows or native Docker on Linux)
- **Git** (version 2.30+)
- **Python 3.11+** (for management scripts and CLI tools)
- **KeePassXC** (v2.7+) for secure secret storage
- **rclone** (v1.60+) for encrypted Google Drive cloud backups

---

## 4. Quickstart

### Option A: Dockerized Deployment (Recommended)

1. Clone repository and initialize environment:
   ```bash
   git clone https://github.com/pankajcseaiml/SovereignAI.git
   cd SovereignAI
   scripts\setup.bat
   ```
2. Start all services:
   ```bash
   scripts\start.bat
   ```
3. Verify running services:
   ```bash
   scripts\status.bat
   ```
4. Access endpoints:
   - **Frontend UI**: [http://localhost:3000](http://localhost:3000)
   - **Backend API Docs**: [http://localhost:8001/api/v1/openapi.json](http://localhost:8001/api/v1/openapi.json)
   - **API Health**: [http://localhost:8001/health](http://localhost:8001/health)
   - **Qdrant Dashboard**: [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

### Option B: Local Development

```bash
# Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Setup frontend
cd ../frontend
npm install
npm run dev
```

---

## 5. Secret Management (KeePassXC)

SovereignAI strictly prohibits checking secrets into Git. Real credentials reside in an encrypted local KeePassXC vault:
`%USERPROFILE%\Documents\SovereignAI_Secrets.kdbx`

To initialize the vault and import existing credentials:
```bash
scripts\init_keepass.bat
```

To regenerate `.env` on-demand without printing secret values:
```bash
scripts\generate_env.bat
```

---

## 6. Encrypted Google Drive Backups

Backups are compressed with gzip (level 9), encrypted with **AES-256-GCM**, verified with **SHA-256**, and synced to Google Drive (`gdrive:Projects/SovereignAI/`):

- **Create and upload backup**:
  ```bash
  scripts\backup_to_drive.bat
  ```
- **Verify backup integrity & decryption keys**:
  ```bash
  scripts\verify_backup.bat
  ```
- **Restore from Google Drive**:
  ```bash
  scripts\restore_from_drive.bat
  ```

---

## 7. Testing & Verification

Run the automated verification suite to audit secrets, run unit tests, and verify backup integrity:
```bash
scripts\verify.bat
```

Or run pytest directly:
```bash
python -m pytest tests/backend -v
```

---

## 8. Disaster Recovery

If the host machine is completely destroyed, SovereignAI can be reconstructed on a fresh computer using only:
1. Private GitHub Repository
2. KeePassXC master password
3. Google Drive encrypted backups

See [docs/DISASTER_RECOVERY.md](file:///c:/Users/Pankaj/Documents/SovereignAI/docs/DISASTER_RECOVERY.md) for the complete runbook.
