@echo off
chcp 65001 >nul
cls

echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                                                                    ║
echo ║         🚀 Setup และ Deploy ไปยัง Render.com 🚀                   ║
echo ║                                                                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo 📋 Checklist - สิ่งที่ต้องเตรียม
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 1. GitHub Account - https://github.com/signup
echo 2. Git for Windows - https://git-scm.com/download/win
echo 3. Render Account - https://render.com/register
echo.

set /p github_ready="มี GitHub account แล้วหรือยัง? (y/n): "
if /i "%github_ready%" neq "y" (
    echo.
    echo ❌ กรุณาสร้าง GitHub account ก่อน:
    echo    1. เปิด: https://github.com/signup
    echo    2. กรอกข้อมูล และ verify email
    echo    3. กลับมารันไฟล์นี้อีกครั้ง
    echo.
    start https://github.com/signup
    pause
    exit /b 1
)

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [1/5] ตรวจสอบ Git
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ยังไม่ได้ติดตั้ง Git
    echo.
    echo กำลังเปิดหน้าดาวน์โหลด Git...
    start https://git-scm.com/download/win
    echo.
    echo 📌 ขั้นตอน:
    echo    1. ดาวน์โหลด Git for Windows
    echo    2. ติดตั้งแบบ default ทุกอย่าง
    echo    3. Restart terminal
    echo    4. กลับมารันไฟล์นี้อีกครั้ง
    echo.
    pause
    exit /b 1
)

echo ✅ Git ติดตั้งแล้ว
git --version
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [2/5] ตั้งค่า Git
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

set /p git_name="ชื่อของคุณ (สำหรับ Git): "
set /p git_email="Email ของคุณ (ที่ใช้กับ GitHub): "

git config --global user.name "%git_name%"
git config --global user.email "%git_email%"

echo ✅ ตั้งค่า Git แล้ว
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [3/5] สร้าง GitHub Repository
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo กรุณาทำตามขั้นตอน:
echo.
echo 1. เปิดเบราว์เซอร์ไปที่: https://github.com/new
echo 2. Repository name: n8n-news-bot
echo 3. เลือก: Private (ถ้าไม่อยากให้คนอื่นเห็น)
echo 4. ❌ ห้ามติ๊ก "Add README file"
echo 5. คลิก "Create repository"
echo 6. คัดลอก URL ที่ได้ (เช่น https://github.com/yourname/n8n-news-bot.git)
echo.

start https://github.com/new

set /p repo_url="วาง GitHub repository URL ที่นี่: "

if "%repo_url%"=="" (
    echo ❌ ต้องใส่ repository URL
    pause
    exit /b 1
)

echo.
echo ✅ Repository URL: %repo_url%
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [4/5] Push Code ขึ้น GitHub
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM สร้าง .gitignore
echo node_modules/ > .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo .env >> .gitignore
echo .DS_Store >> .gitignore
echo downloads/* >> .gitignore
echo !downloads/.gitkeep >> .gitignore
echo *.log >> .gitignore

REM สร้าง .gitkeep สำหรับ downloads
type nul > downloads\.gitkeep

REM Initialize Git
git init
git add .
git commit -m "Initial commit - Auto News Posting Bot"
git branch -M main
git remote add origin %repo_url%

echo.
echo กำลัง push code ขึ้น GitHub...
echo (จะถาม username และ password/token)
echo.
echo 📌 ถ้าใช้ password:
echo    - Password ธรรมดาใช้ไม่ได้แล้ว!
echo    - ต้องสร้าง Personal Access Token
echo    - ไปที่: https://github.com/settings/tokens
echo    - Generate new token (classic)
echo    - เลือก scope: repo
echo    - คัดลอก token มาใส่แทน password
echo.

git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Push ไม่สำเร็จ
    echo.
    echo วิธีแก้:
    echo 1. ตรวจสอบ username/password ถูกต้อง
    echo 2. ใช้ Personal Access Token แทน password
    echo 3. ไปสร้างที่: https://github.com/settings/tokens
    echo.
    start https://github.com/settings/tokens
    pause
    exit /b 1
)

echo.
echo ✅ Push code ขึ้น GitHub สำเร็จ!
echo.

echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo [5/5] Deploy บน Render.com
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

echo 📌 ขั้นตอนถัดไป:
echo.
echo 1. สร้าง Render account:
echo    → https://render.com/register
echo    → เลือก "Sign up with GitHub"
echo.
echo 2. อ่านคู่มือ: RENDER_DEPLOYMENT_GUIDE.md
echo    → มีคำแนะนำทีละขั้นตอนละเอียด
echo.
echo 3. Deploy Services:
echo    → Deploy youtube-downloader-api ก่อน
echo    → คัดลอก URL ที่ได้
echo    → Deploy n8n
echo    → ตั้งค่า YOUTUBE_API_URL
echo.
echo 4. เข้าใช้งาน:
echo    → https://n8n-automation.onrender.com
echo    → Username: admin
echo    → Password: admin123
echo.

echo.
echo กำลังเปิดหน้า Render...
echo.

start https://render.com/register
start https://dashboard.render.com

echo.
echo ╔════════════════════════════════════════════════════════════════════╗
echo ║                    ✅ เสร็จขั้นตอนเตรียมการ! ✅                    ║
echo ╚════════════════════════════════════════════════════════════════════╝
echo.
echo 📂 Code อยู่บน GitHub แล้ว!
echo 📖 เปิดไฟล์: RENDER_DEPLOYMENT_GUIDE.md
echo 🌐 ไปที่: https://dashboard.render.com
echo.
echo ขั้นต่อไป: ทำตามคู่มือใน RENDER_DEPLOYMENT_GUIDE.md
echo.
pause
