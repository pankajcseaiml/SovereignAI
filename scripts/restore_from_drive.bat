@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — Restore from Google Drive
echo ========================================================
python scripts\restore_from_drive.py %*
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Restore from Google Drive failed.
    exit /b 1
)
echo [SUCCESS] Restore completed.
