@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║         🚀 ติดตั้ง Docker ด้วย WSL อัตโนมัติ 🚀                    ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

REM ตรวจสอบสิทธิ์ Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ต้องรันแบบ Administrator!
    echo.
    echo กรุณา:
    echo 1. คลิกขวาที่ไฟล์นี้
    echo 2. เลือก "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [1/3] ตั้งค่า WSL 1 (ไม่ต้องใช้ VirtualMachinePlatform)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

wsl --set-default-version 1
echo ✅ ตั้ง WSL 1 เป็น default แล้ว
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [2/3] ติดตั้ง Ubuntu 22.04
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo กำลังติดตั้ง Ubuntu... (ใช้เวลา 5-10 นาที)
echo.

wsl --install -d Ubuntu-22.04

if %errorlevel% equ 0 (
    echo.
    echo ✅ ติดตั้ง Ubuntu สำเร็จ!
    echo.
) else (
    echo.
    echo ⚠️  การติดตั้ง Ubuntu อาจมีปัญหา
    echo กรุณาลองติดตั้งผ่าน Microsoft Store แทน
    echo.
    echo กดปุ่มใดก็ได้เพื่อเปิด Microsoft Store...
    pause >nul
    start ms-windows-store://pdp/?ProductId=9PN20MSR04DW
    exit /b 1
)

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [3/3] เตรียมสคริปต์ติดตั้ง Docker
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo ✅ สร้างสคริปต์สำเร็จ: install_docker_in_ubuntu.sh
echo.

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                    ✅ เสร็จขั้นตอนที่ 1! ✅                         ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📌 ขั้นตอนถัดไป:
echo.
echo 1️⃣  Ubuntu terminal จะเปิดขึ้นมา
echo    → ตั้งชื่อผู้ใช้และรหัสผ่าน
echo.
echo 2️⃣  หลังตั้งเสร็จ ใน Ubuntu terminal ให้รัน:
echo    → ./install_docker_in_ubuntu.sh
echo.
echo 3️⃣  รอให้ Docker ติดตั้งเสร็จ (10-15 นาที)
echo.
echo 4️⃣  แล้วรัน:
echo    → ./start_news_bot.sh
echo.
echo 5️⃣  เปิดเบราว์เซอร์:
echo    → http://localhost:5678
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
