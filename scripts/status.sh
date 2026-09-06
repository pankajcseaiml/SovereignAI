#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"
echo "========================================================"
echo "  SovereignAI — Application & Container Status          "
echo "========================================================"
docker compose ps
echo ""
echo "Persistent Volumes:"
docker volume ls --filter name=sovereign
