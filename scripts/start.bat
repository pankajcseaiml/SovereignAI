@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — Starting Application Containers
echo ========================================================
docker compose up -d %*
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Docker compose up failed. Ensure Docker Desktop is running.
    exit /b 1
)
echo.
echo [SUCCESS] Containers started! Check status with scripts\status.bat
