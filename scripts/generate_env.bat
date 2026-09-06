@echo off
setlocal
cd /d "%~dp0\.."
echo ========================================================
echo   SovereignAI — Local Environment Reconstruction
echo ========================================================
python scripts\generate_env.py %*
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to generate .env
    exit /b 1
)
echo [OK] .env generated successfully.
