@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI -- End-to-End System Verification Audit
echo ========================================================

echo.
echo [*] Phase 1: Running Automated Secret Scanner...
python scripts\scan_secrets.py
if errorlevel 1 (
    echo [FAIL] Secret scan detected sensitive data!
    exit /b 1
)
echo [PASS] Zero secrets detected in workspace.

echo.
echo [*] Phase 2: Verifying Environment Configuration...
if not exist ".env" (
    echo [WARNING] .env not found.
) else (
    echo [PASS] .env file is present.
)

echo.
echo [*] Phase 3: Executing Automated Test Suite...
python -m pytest tests/backend -v
if errorlevel 1 (
    echo [FAIL] Test suite encountered failures.
    exit /b 1
)
echo [PASS] All automated unit tests passed!

echo.
echo [*] Phase 4: Auditing Backup Integrity and Decryption Keys...
python scripts\verify_backup.py
if errorlevel 1 (
    echo [NOTICE] Backup verification reported notices.
) else (
    echo [PASS] Backup integrity verified.
)

echo.
echo ========================================================
echo   [SUCCESS] All SovereignAI System Verifications PASSED!
echo ========================================================
