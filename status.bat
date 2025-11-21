@echo off
chcp 65001 >nul
cls
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              🔍 ตรวจสอบสถานะระบบ 🔍                            ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM ตรวจสอบว่า Docker Engine ทำงานหรือไม่
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Engine ไม่ทำงาน!
    echo กรุณาเปิด Docker Desktop ก่อน
    echo.
    pause
    exit /b 1
)

echo กำลังตรวจสอบ...
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📦 Docker Containers
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
docker-compose ps
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🌐 Services
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

echo.
echo [n8n Automation]
curl -s http://localhost:5678 >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ สถานะ: ทำงาน
    echo   🔗 URL: http://localhost:5678
    echo   👤 Username: admin
    echo   🔑 Password: admin123
) else (
    echo   ❌ สถานะ: ไม่ตอบสนอง
    echo   💡 ลองรัน: docker-compose restart n8n
)

echo.
echo [YouTube Downloader API]
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✅ สถานะ: ทำงาน
    echo   🔗 URL: http://localhost:8000
    echo   📄 Docs: http://localhost:8000/docs
) else (
    echo   ❌ สถานะ: ไม่ตอบสนอง
    echo   💡 ลองรัน: docker-compose restart youtube-downloader-api
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📊 Resources
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REM นับจำนวนไฟล์ใน downloads
if exist "downloads" (
    dir /b "downloads" 2>nul | find /c /v "" > temp_count.txt
    set /p FILE_COUNT=<temp_count.txt
    del temp_count.txt
    echo   📁 ไฟล์ใน downloads: !FILE_COUNT! ไฟล์
) else (
    echo   📁 ไฟล์ใน downloads: โฟลเดอร์ยังไม่สร้าง
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 🛠️  Actions
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo [1] ดู logs n8n              → docker-compose logs -f n8n
echo [2] ดู logs API              → docker-compose logs -f youtube-downloader-api
echo [3] Restart ทั้งหมด         → docker-compose restart
echo [4] หยุดระบบ                → docker-compose down
echo [5] เปิดเว็บ n8n             → http://localhost:5678
echo [6] เปิดเว็บ API Docs        → http://localhost:8000/docs
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

choice /c 123456X /n /m "เลือกคำสั่ง (1-6) หรือ X เพื่อออก: "

if errorlevel 7 exit /b 0
if errorlevel 6 start http://localhost:8000/docs
if errorlevel 5 start http://localhost:5678
if errorlevel 4 docker-compose down
if errorlevel 3 docker-compose restart
if errorlevel 2 docker-compose logs -f youtube-downloader-api
if errorlevel 1 docker-compose logs -f n8n

pause
