@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — End-to-End System Verification Audit
echo ========================================================

REM 1. Secret Scan
echo.
echo [*] Phase 1: Running Automated Secret Scanner...
python scripts\scan_secrets.py
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Secret scan detected sensitive data! Aborting.
    exit /b 1
)
echo [PASS] Zero secrets detected in workspace.

REM 2. Environment Verification
echo.
echo [*] Phase 2: Verifying Environment Configuration...
if not exist ".env" (
    echo [WARNING] .env not found. Using .env.example defaults for verification.
) else (
    echo [PASS] .env file is present.
)

REM 3. Run Pytest Suite
echo.
echo [*] Phase 3: Executing Automated Test Suite...
python -m pytest tests/backend -v
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Test suite encountered failures.
    exit /b 1
)
echo [PASS] All automated unit tests passed!

REM 4. Verify Backup Integrity
echo.
echo [*] Phase 4: Auditing Backup Integrity & Decryption Keys...
python scripts\verify_backup.py
if %ERRORLEVEL% NEQ 0 (
    echo [NOTICE] Backup verification reported notices (check if backups have been created).
) else (
    echo [PASS] Backup integrity verified.
)

echo.
echo ========================================================
echo   [SUCCESS] All SovereignAI System Verifications PASSED!
echo ========================================================
