#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "========================================================"
echo "  SovereignAI — Enterprise Setup & Environment Init     "
echo "========================================================"

# 1. Check Python
if ! command -v python3 &>/dev/null && ! command -v python &>/dev/null; then
    echo "[ERROR] Python is not installed."
    exit 1
fi
echo "[OK] Python detected."

# 2. Check Git
if ! command -v git &>/dev/null; then
    echo "[ERROR] Git is not installed."
    exit 1
fi
echo "[OK] Git detected."

# 3. Check Docker
if command -v docker &>/dev/null; then
    echo "[OK] Docker detected."
else
    echo "[WARNING] Docker is not installed."
fi

# 4. Storage & backup directories
mkdir -p storage/{uploads,processed,generated,temporary,quarantine}
mkdir -p backups/{database,storage,checksums}

# 5. Check .env
if [ ! -f ".env" ]; then
    echo "[*] Creating .env from .env.example..."
    cp .env.example .env
fi

echo "[SUCCESS] SovereignAI Setup Completed!"
