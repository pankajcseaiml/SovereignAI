@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — Google Drive Backup Pipeline
echo ========================================================
python scripts\backup_to_drive.py %*
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Backup to Google Drive failed.
    exit /b 1
)
echo [SUCCESS] Backup completed.
