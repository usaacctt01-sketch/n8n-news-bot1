@echo off
chcp 65001 >nul
echo ================================================
echo 🚀 เริ่มระบบโพสต์ข่าวอัตโนมัติ
echo ================================================
echo.

echo [1/3] ตรวจสอบ Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ไม่พบ Docker! กรุณาติดตั้ง Docker Desktop ก่อน
    echo    ดาวน์โหลดได้ที่: https://www.docker.com/products/docker-desktop/
    pause
    exit /b 1
)
echo ✅ Docker พร้อมใช้งาน
echo.

echo [2/3] สร้างโฟลเดอร์ที่จำเป็น...
if not exist "downloads" mkdir downloads
if not exist "scripts" mkdir scripts
echo ✅ โฟลเดอร์พร้อมแล้ว
echo.

echo [3/3] เริ่มต้น Docker Containers...
docker-compose up -d
echo.

if %errorlevel% equ 0 (
    echo ================================================
    echo ✅ เริ่มต้นสำเร็จ!
    echo ================================================
    echo.
    echo 🌐 เข้าใช้งาน n8n ได้ที่:
    echo    http://localhost:5678
    echo.
    echo 🔑 Login:
    echo    Username: admin
    echo    Password: admin123
    echo.
    echo 🛠️ FastAPI (YouTube Downloader):
    echo    http://localhost:8000
    echo.
    echo ================================================
    echo.
    echo กด Ctrl+C เพื่อหยุดการทำงาน หรือปิดหน้าต่างนี้
    echo.
    echo ดูสถานะ: docker-compose ps
    echo ดู logs:   docker-compose logs -f
    echo หยุดระบบ:  docker-compose down
    echo ================================================
    
    REM Open browser
    timeout /t 3 >nul
    start http://localhost:5678
    
) else (
    echo ❌ เกิดข้อผิดพลาดในการเริ่มต้น
    echo กรุณาตรวจสอบ Docker Desktop ว่าเปิดอยู่หรือไม่
)

pause
