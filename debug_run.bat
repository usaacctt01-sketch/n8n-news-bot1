@echo off
chcp 65001 > nul
echo ==========================================
echo       DIAGNOSTIC MODE (โหมดตรวจสอบ)
echo ==========================================
echo.

echo [1/3] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python.
    pause
    exit /b
)

echo.
echo [2/3] Testing Minimal GUI...
python minimal.py
if %errorlevel% neq 0 (
    echo [ERROR] Minimal GUI failed!
) else (
    echo [SUCCESS] Minimal GUI works.
)

echo.
echo [3/3] Running Main Bot (Fixed Version)...
python tiktok_bot_fixed.py

echo.
echo ==========================================
echo    PROGRAM FINISHED / CRASHED
echo    READ THE ERROR MESSAGE ABOVE
echo ==========================================
pause
