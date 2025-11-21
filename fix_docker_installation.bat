@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║        🔧 แก้ปัญหา Docker Installation Failed 🔧                   ║
║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  ข้อผิดพลาด: Virtual Machine Platform ติดตั้งไม่สำเร็จ
echo.
echo กำลังแก้ไขปัญหาโดยอัตโนมัติ...
echo.

REM ตรวจสอบสิทธิ์ Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ สคริปต์นี้ต้องรันแบบ Administrator!
    echo.
    echo กรุณา:
    echo 1. คลิกขวาที่ไฟล์นี้
    echo 2. เลือก "Run as administrator"
    echo.
    pause
    exit /b 1
)

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [1/5] เปิดใช้งาน Virtual Machine Platform
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

if %errorlevel% equ 0 (
    echo ✅ เปิดใช้งาน Virtual Machine Platform สำเร็จ
) else (
    echo ⚠️  มีปัญหากับ Virtual Machine Platform
)
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [2/5] เปิดใช้งาน Windows Subsystem for Linux (WSL)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

if %errorlevel% equ 0 (
    echo ✅ เปิดใช้งาน WSL สำเร็จ
) else (
    echo ⚠️  มีปัญหากับ WSL
)
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [3/5] ตรวจสอบ Hyper-V (ถ้ามี)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

dism.exe /online /enable-feature /featurename:Microsoft-Hyper-V-All /all /norestart >nul 2>&1

if %errorlevel% equ 0 (
    echo ✅ เปิดใช้งาน Hyper-V สำเร็จ
) else (
    echo ℹ️  ไม่สามารถเปิด Hyper-V ได้ (จะใช้ WSL 2 แทน - ไม่เป็นไร)
)
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [4/5] เปิดใช้งาน Containers
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

dism.exe /online /enable-feature /featurename:Containers /all /norestart >nul 2>&1

if %errorlevel% equ 0 (
    echo ✅ เปิดใช้งาน Containers สำเร็จ
) else (
    echo ℹ️  Containers feature (ไม่จำเป็นสำหรับ Docker Desktop)
)
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [5/5] แสดงสถานะทั้งหมด
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo Windows Features ที่เปิดใช้งาน:
echo.
dism.exe /online /get-features /format:table | findstr /i "VirtualMachinePlatform Microsoft-Windows-Subsystem-Linux"

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                    ✅ การแก้ไขเสร็จสมบูรณ์! ✅                      ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📌 ขั้นตอนถัดไป:
echo.
echo 1️⃣  RESTART WINDOWS ทันที! (สำคัญมาก!)
echo    Windows features ที่เปิดใช้งานต้องการ restart
echo.
echo 2️⃣  หลัง restart:
echo    - ลองติดตั้ง Docker Desktop อีกครั้ง
echo    - หรือถ้าติดตั้งแล้ว ให้เปิด Docker Desktop
echo.
echo 3️⃣  ถ้ายังมีปัญหา:
echo    - อ่าน DOCKER_INSTALLATION.md
echo    - ลองติดตั้ง WSL 2 update: https://aka.ms/wsl2kernel
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

choice /c YN /m "ต้องการ Restart Windows เดี๋ยวนี้หรือไม่? (Y/N)"

if errorlevel 2 (
    echo.
    echo ⚠️  อย่าลืม Restart Windows ด้วยตนเอง!
    echo.
    pause
    exit /b 0
)

if errorlevel 1 (
    echo.
    echo กำลัง Restart Windows ใน 10 วินาที...
    echo กด Ctrl+C เพื่อยกเลิก
    echo.
    shutdown /r /t 10
)

exit /b 0
