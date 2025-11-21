@echo off
chcp 65001 >nul
echo ====================================
echo   Twitter Auto Post Bot
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ไม่พบ Python กรุณาติดตั้ง Python ก่อน
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if requirements are installed
echo กำลังตรวจสอบ Dependencies...
pip show selenium >nul 2>&1
if errorlevel 1 (
    echo กำลังติดตั้ง Dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ ติดตั้ง Dependencies ไม่สำเร็จ
        pause
        exit /b 1
    )
)

echo ✓ Dependencies พร้อมใช้งาน
echo.
echo กำลังเปิดโปรแกรม...
echo.
echo ⚠️  อย่าลืม: ปิด Chrome ทั้งหมดก่อนใช้งาน!
echo.

REM Run the bot
python twitter_bot.py

if errorlevel 1 (
    echo.
    echo ❌ เกิดข้อผิดพลาด
    pause
)
