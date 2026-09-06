@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — Application & Container Status
echo ========================================================
docker compose ps
echo.
echo Persistent Volumes:
docker volume ls --filter name=sovereign
