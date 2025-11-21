@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║         🔧 แก้ปัญหา Registry Corruption (Error 0x800703F1) 🔧      ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo ⚠️  ปัญหา: Registry Database Corrupt
echo 💡 วิธีแก้: ซ่อมแซม Windows และ Registry
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
echo [1/6] ตรวจสอบและซ่อมแซมไฟล์ระบบ (SFC)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo กำลังตรวจสอบไฟล์ระบบ... (อาจใช้เวลา 5-10 นาที)
echo.

sfc /scannow

if %errorlevel% equ 0 (
    echo ✅ ตรวจสอบและซ่อมแซมไฟล์ระบบเสร็จสิ้น
) else (
    echo ⚠️  พบปัญหากับไฟล์ระบบ
)
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [2/6] ตรวจสอบ Windows Image (DISM - CheckHealth)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

DISM /Online /Cleanup-Image /CheckHealth

echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [3/6] สแกนความเสียหาย (DISM - ScanHealth)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo กำลังสแกน... (อาจใช้เวลา 10-20 นาที)
echo.

DISM /Online /Cleanup-Image /ScanHealth

echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [4/6] ซ่อมแซม Windows Image (DISM - RestoreHealth)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo กำลังซ่อมแซม... (อาจใช้เวลา 15-30 นาที)
echo.

DISM /Online /Cleanup-Image /RestoreHealth

if %errorlevel% equ 0 (
    echo ✅ ซ่อมแซม Windows Image สำเร็จ
) else (
    echo ⚠️  มีปัญหากับการซ่อมแซม
)
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [5/6] รัน SFC อีกครั้ง (หลังซ่อม DISM)
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

sfc /scannow

echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [6/6] ลองเปิด Virtual Machine Platform อีกครั้ง
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

if %errorlevel% equ 0 (
    echo ✅ เปิดใช้งาน Virtual Machine Platform สำเร็จ!
) else (
    echo ⚠️  ยังมีปัญหากับ Virtual Machine Platform
    echo.
    echo จะลองวิธีอื่น...
)
echo.

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                    ✅ การซ่อมแซมเสร็จสิ้น! ✅                       ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📌 ขั้นตอนถัดไป:
echo.
echo 1️⃣  RESTART WINDOWS ทันที! (สำคัญมาก!)
echo.
echo 2️⃣  หลัง restart:
echo    - รัน fix_docker_installation.bat อีกครั้ง
echo    - หรือลองติดตั้ง Docker Desktop โดยตรง
echo.
echo 3️⃣  ถ้ายังไม่ได้:
echo    - ใช้วิธีติดตั้ง Docker แบบ WSL 2 เท่านั้น
echo    - อ่าน ALTERNATIVE_DOCKER_SETUP.md
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
    echo กำลัง Restart Windows ใน 15 วินาที...
    echo กด Ctrl+C เพื่อยกเลิก
    echo.
    shutdown /r /t 15
)

exit /b 0
