@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — Stopping Application Containers
echo   (Persistent volumes and databases are safely preserved)
echo ========================================================
docker compose down
echo [SUCCESS] Containers stopped cleanly.
