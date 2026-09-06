#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
echo "========================================================"
echo "  SovereignAI — Starting Application Containers         "
echo "========================================================"
docker compose up -d "$@"
echo "[SUCCESS] Containers started! Check status with scripts/status.sh"
