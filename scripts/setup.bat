@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — Enterprise Setup & Environment Init
echo ========================================================

REM 1. Check Python
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH.
    exit /b 1
)
echo [OK] Python detected.

REM 2. Check Git
git --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Git is not installed or not in PATH.
    exit /b 1
)
echo [OK] Git detected.

REM 3. Check Docker
docker --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Docker is not installed or not in PATH.
) else (
    echo [OK] Docker detected.
)

REM 4. Ensure directories exist
if not exist "storage\uploads" mkdir "storage\uploads"
if not exist "storage\processed" mkdir "storage\processed"
if not exist "storage\generated" mkdir "storage\generated"
if not exist "storage\temporary" mkdir "storage\temporary"
if not exist "storage\quarantine" mkdir "storage\quarantine"
if not exist "backups\database" mkdir "backups\database"
if not exist "backups\storage" mkdir "backups\storage"
if not exist "backups\checksums" mkdir "backups\checksums"

REM 5. Check .env file
if not exist ".env" (
    echo [*] .env not found. Checking KeePassXC vault...
    if exist "%USERPROFILE%\Documents\SovereignAI_Secrets.kdbx" (
        echo [*] KeePassXC vault detected. Reconstructing .env...
        call scripts\generate_env.bat
    ) else (
        echo [*] Creating .env from .env.example template...
        copy .env.example .env >nul
        echo [NOTICE] Please review and customize .env before starting services.
    )
) else (
    echo [OK] .env configuration file exists.
)

echo.
echo ========================================================
echo   [SUCCESS] SovereignAI Setup Completed!
echo   Run scripts\start.bat to launch Docker containers.
echo ========================================================
