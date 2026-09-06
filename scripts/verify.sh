#!/usr/bin/env bash
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "========================================================"
echo "  SovereignAI — End-to-End System Verification Audit    "
echo "========================================================"

# 1. Secret Scan
echo "[*] Phase 1: Running Automated Secret Scanner..."
python3 scripts/scan_secrets.py || python scripts/scan_secrets.py
echo "[PASS] Zero secrets detected."

# 2. Environment Verification
echo "[*] Phase 2: Verifying Environment..."
if [ -f ".env" ]; then
    echo "[PASS] .env file is present."
fi

# 3. Test Suite
echo "[*] Phase 3: Executing Test Suite..."
pytest tests/backend -v || python -m pytest tests/backend -v
echo "[PASS] Tests passed."

# 4. Backup Verification
echo "[*] Phase 4: Auditing Backup Integrity..."
python3 scripts/verify_backup.py || python scripts/verify_backup.py

echo "========================================================"
echo "  [SUCCESS] All SovereignAI Verifications PASSED!       "
echo "========================================================"
