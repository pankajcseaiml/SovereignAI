#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
echo "========================================================"
echo "  SovereignAI — Stopping Application Containers         "
echo "  (Persistent volumes and databases are safely preserved)"
echo "========================================================"
docker compose down
echo "[SUCCESS] Containers stopped cleanly."
