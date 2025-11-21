@echo off
chcp 65001 >nul
cls
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║        🚀 ระบบโพสต์ข่าวอัตโนมัติ - ตรวจสอบระบบ 🚀             ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo กำลังตรวจสอบระบบ...
echo.

REM ตรวจสอบ Docker
echo [1/4] ตรวจสอบ Docker...
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker พบแล้ว
    docker --version
) else (
    echo ❌ ไม่พบ Docker!
    echo.
    echo 📥 กรุณาติดตั้ง Docker Desktop ก่อน:
    echo    👉 https://www.docker.com/products/docker-desktop/
    echo.
    echo 📖 อ่านคู่มือการติดตั้งที่: INSTALLATION_GUIDE.md
    echo.
    pause
    exit /b 1
)
echo.

REM ตรวจสอบ Docker Compose
echo [2/4] ตรวจสอบ Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker Compose พบแล้ว
    docker-compose --version
) else (
    echo ❌ ไม่พบ Docker Compose!
    pause
    exit /b 1
)
echo.

REM ตรวจสอบ Docker Engine ทำงานหรือไม่
echo [3/4] ตรวจสอบ Docker Engine...
docker info >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Docker Engine ทำงานปกติ
) else (
    echo ❌ Docker Engine ไม่ทำงาน!
    echo.
    echo กรุณา:
    echo 1. เปิด Docker Desktop
    echo 2. รอจนไฟเป็นสีเขียว
    echo 3. รันโปรแกรมนี้อีกครั้ง
    echo.
    pause
    exit /b 1
)
echo.

REM ตรวจสอบไฟล์ที่จำเป็น
echo [4/4] ตรวจสอบไฟล์...
set FILES_OK=1

if not exist "docker-compose.yml" (
    echo ❌ ไม่พบไฟล์: docker-compose.yml
    set FILES_OK=0
)

if not exist "Flow 2 โพสต์ข่าว.json" (
    echo ❌ ไม่พบไฟล์: Flow 2 โพสต์ข่าว.json
    set FILES_OK=0
)

if not exist "youtube-downloader-api\Dockerfile" (
    echo ❌ ไม่พบไฟล์: youtube-downloader-api\Dockerfile
    set FILES_OK=0
)

if not exist "youtube-downloader-api\main.py" (
    echo ❌ ไม่พบไฟล์: youtube-downloader-api\main.py
    set FILES_OK=0
)

if %FILES_OK% equ 1 (
    echo ✅ ไฟล์ทั้งหมดพร้อมแล้ว
) else (
    echo ❌ ไฟล์บางไฟล์หายไป!
    pause
    exit /b 1
)
echo.

echo ╔════════════════════════════════════════════════════════════════╗
echo ║                  ✅ ระบบพร้อมใช้งาน! ✅                         ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo คุณสามารถเริ่มใช้งานได้โดย:
echo.
echo 1️⃣  Double-click ไฟล์ "start.bat"
echo 2️⃣  หรือรันคำสั่ง: docker-compose up -d
echo.
echo 📖 อ่านคู่มือเพิ่มเติมที่: INSTALLATION_GUIDE.md
echo.
pause
