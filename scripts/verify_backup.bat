@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — Backup Integrity Verification
echo ========================================================
python scripts\verify_backup.py %*
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Backup verification reported issues.
    exit /b 1
)
echo [SUCCESS] Backup verification completed successfully.
