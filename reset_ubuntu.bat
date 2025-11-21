@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║         🔄 รีเซ็ต Ubuntu และลงใหม่ 🔄                              ║
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

echo ⚠️  คำเตือน: จะลบ Ubuntu และ Docker ที่ติดตั้งไว้
echo.
echo กดปุ่มใดก็ได้เพื่อดำเนินการต่อ หรือปิดหน้าต่างนี้เพื่อยกเลิก...
pause >nul

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [1/3] ลบ Ubuntu 22.04
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

wsl --unregister Ubuntu-22.04

echo.
echo ✅ ลบ Ubuntu 22.04 แล้ว
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [2/3] ตั้งค่า WSL 1
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

wsl --set-default-version 1

echo.
echo ✅ ตั้งค่า WSL 1 แล้ว
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [3/3] ติดตั้ง Ubuntu 22.04 ใหม่
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo กำลังติดตั้ง Ubuntu... (ใช้เวลา 5-10 นาที)
echo.

wsl --install -d Ubuntu-22.04

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                    ✅ รีเซ็ตสำเร็จ! ✅                              ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📌 ขั้นตอนถัดไป:
echo.
echo 1️⃣  Ubuntu terminal จะเปิดขึ้นมา
echo    → ตั้งชื่อผู้ใช้และรหัสผ่าน (ครั้งนี้ห้ามลืม!)
echo.
echo 2️⃣  ใน Ubuntu terminal ให้รัน:
echo    cd /mnt/g/เทสทวิต
echo    chmod +x install_docker_in_ubuntu.sh
echo    ./install_docker_in_ubuntu.sh
echo.
echo 3️⃣  หลังติดตั้ง Docker เสร็จ ปิดและเปิด Ubuntu ใหม่
echo.
echo 4️⃣  รัน:
echo    cd /mnt/g/เทสทวิต
echo    sudo docker compose up -d
echo.
echo 5️⃣  เปิดเบราว์เซอร์:
echo    http://localhost:5678
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
pause
