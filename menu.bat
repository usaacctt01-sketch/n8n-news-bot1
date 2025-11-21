@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║           📖 QUICK START - เริ่มต้นอย่างรวดเร็ว 📖            ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

:MENU
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          🎯 เมนูหลัก - Auto News Posting System 🎯             ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo   [1] 🔍 ตรวจสอบระบบ (Check System)
echo   [2] 🚀 เริ่มต้นระบบ (Start System)
echo   [3] 📊 ดูสถานะ (View Status)
echo   [4] 📝 ดู Logs
echo   [5] 🔄 Restart ระบบ
echo   [6] ⏹️  หยุดระบบ (Stop System)
echo   [7] 🗑️  ลบข้อมูลทั้งหมด (Clean All Data)
echo   [8] 📖 เปิดคู่มือ (Open Guide)
echo   [9] 🌐 เปิด n8n
echo   [0] ❌ ออก (Exit)
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

choice /c 1234567890 /n /m "เลือกคำสั่ง (0-9): "

if errorlevel 10 goto EXIT
if errorlevel 9 goto OPEN_N8N
if errorlevel 8 goto OPEN_GUIDE
if errorlevel 7 goto CLEAN
if errorlevel 6 goto STOP
if errorlevel 5 goto RESTART
if errorlevel 4 goto LOGS
if errorlevel 3 goto STATUS
if errorlevel 2 goto START
if errorlevel 1 goto CHECK

:CHECK
cls
echo กำลังตรวจสอบระบบ...
call check_system.bat
goto MENU

:START
cls
echo กำลังเริ่มต้นระบบ...
call start.bat
goto MENU

:STATUS
cls
call status.bat
goto MENU

:LOGS
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                        📝 Logs Menu                            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo   [1] ดู n8n logs
echo   [2] ดู YouTube API logs
echo   [3] ดู logs ทั้งหมด
echo   [4] กลับเมนูหลัก
echo.
choice /c 1234 /n /m "เลือก (1-4): "
if errorlevel 4 goto MENU
if errorlevel 3 docker-compose logs -f
if errorlevel 2 docker-compose logs -f youtube-downloader-api
if errorlevel 1 docker-compose logs -f n8n
goto MENU

:RESTART
cls
echo.
echo กำลัง Restart ระบบ...
docker-compose restart
echo.
echo ✅ Restart เสร็จสิ้น!
timeout /t 3
goto MENU

:STOP
cls
echo.
echo ⚠️  คุณแน่ใจหรือไม่ที่จะหยุดระบบ?
choice /m "หยุดระบบ"
if errorlevel 2 goto MENU
echo.
echo กำลังหยุดระบบ...
docker-compose down
echo.
echo ✅ หยุดระบบเรียบร้อย!
timeout /t 3
goto MENU

:CLEAN
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                   ⚠️  คำเตือน! WARNING! ⚠️                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo การลบข้อมูลทั้งหมดจะ:
echo   ❌ ลบ Docker volumes (ข้อมูล n8n ทั้งหมด)
echo   ❌ ลบไฟล์ดาวน์โหลดทั้งหมด
echo   ❌ ไม่สามารถกู้คืนได้!
echo.
echo ⚠️  กรุณาแน่ใจก่อนดำเนินการ!
echo.
choice /m "ลบข้อมูลทั้งหมด"
if errorlevel 2 goto MENU
echo.
echo กำลังลบข้อมูล...
docker-compose down -v
if exist "downloads\" rmdir /s /q downloads
mkdir downloads
echo.
echo ✅ ลบข้อมูลเรียบร้อย!
timeout /t 3
goto MENU

:OPEN_GUIDE
cls
echo.
echo กำลังเปิดคู่มือการใช้งาน...
start INSTALLATION_GUIDE.md
timeout /t 2
goto MENU

:OPEN_N8N
cls
echo.
echo กำลังเปิด n8n...
start http://localhost:5678
timeout /t 2
goto MENU

:EXIT
cls
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║              👋 ขอบคุณที่ใช้งาน! Goodbye! 👋                   ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
timeout /t 2
exit /b 0
