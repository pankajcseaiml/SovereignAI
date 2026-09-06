@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — KeePassXC Secret Vault Initializer
echo ========================================================
echo This script initializes an encrypted KeePassXC vault at:
echo   %%USERPROFILE%%\Documents\SovereignAI_Secrets.kdbx
echo and imports all variables from the current .env file.
echo.
python scripts\keepass_manager.py import-env --env .env
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] KeePassXC initialization failed.
    exit /b 1
)
echo.
echo [SUCCESS] Vault initialized and all secrets safely imported!
