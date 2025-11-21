@echo off
chcp 65001 > nul
echo ===================================================
echo       TikTok Auto Post Bot (Fixed Version)
echo ===================================================
echo.

python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b
)

if not exist "requirements.txt" (
    echo [INFO] requirements.txt not found. Skipping dependency check.
) else (
    echo [INFO] Checking dependencies...
    pip install -r requirements.txt > nul 2>&1
)

echo [INFO] Starting TikTok Bot...
echo.
python tiktok_bot_fixed.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The bot crashed or closed with an error.
    pause
)
