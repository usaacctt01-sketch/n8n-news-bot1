# 🤖 ระบบโพสต์ข่าวอัตโนมัติ (Auto News Posting System)

> ระบบอัตโนมัติที่ดาวน์โหลดวิดีโอจาก YouTube, วิเคราะห์เนื้อหาด้วย AI, และโพสต์ไปยัง Facebook อัตโนมัติ

[![n8n](https://img.shields.io/badge/n8n-Workflow-FF6D5A?style=flat&logo=n8n)](https://n8n.io/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![AI Powered](https://img.shields.io/badge/AI-Gemini%20%7C%20GPT--4-4285F4?style=flat&logo=google)](https://openrouter.ai/)

---

## ✨ Features

- 🎬 **ดาวน์โหลดวิดีโอ** จาก YouTube อัตโนมัติ
- 🤖 **วิเคราะห์ด้วย AI** (Gemini 2.5 Flash / GPT-4o)
- 📝 **สร้างแคปชั่นภาษาไทย** พร้อมแฮชแท็กอัตโนมัติ
- 📱 **โพสต์ไปยัง Facebook Page** อัตโนมัติ
- 📊 **จัดการคิวงาน** ผ่าน Google Sheets
- 🗑️ **ลบไฟล์อัตโนมัติ** หลังโพสต์เสร็จ
- ⏰ **รันอัตโนมัติทุก 2 นาที** (ปรับได้)

---

## 🚀 Quick Start (3 Steps)

### 1️⃣ ติดตั้ง Docker Desktop

```powershell
# ดาวน์โหลด Docker Desktop
https://www.docker.com/products/docker-desktop/

# ติดตั้ง → Restart Windows → เปิด Docker Desktop
```

### 2️⃣ เริ่มระบบ

```powershell
# วิธีที่ 1: Double-click
menu.bat

# หรือ วิธีที่ 2: PowerShell
cd "g:\เทสทวิต"
docker-compose up -d
```

### 3️⃣ เข้าใช้งาน n8n

```
🌐 เปิดเว็บเบราว์เซอร์: http://localhost:5678
👤 Username: admin
🔑 Password: admin123
```

📖 **คู่มือฉบับเต็ม:** [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## 🎯 การใช้งาน

### เพิ่มงานใหม่ใน Google Sheets

| video_id | video_url | status | created_at |
|----------|-----------|--------|------------|
| - | https://youtube.com/watch?v=xxx | pending | 2024-11-21 |

### ระบบจะทำอัตโนมัติ:

```
📊 ตรวจสอบงาน "pending" ทุก 2 นาที
    ↓
📥 ดาวน์โหลดวิดีโอจาก YouTube
    ↓
🤖 วิเคราะห์ด้วย AI → สร้างแคปชั่นและแฮชแท็ก
    ↓
📱 โพสต์ไปยัง Facebook Page
    ↓
✅ อัพเดท status → "done"
    ↓
🗑️ ลบไฟล์วิดีโอ
```

---

## 📁 โครงสร้างโปรเจค

```
เทสทวิต/
├── 🎬 เริ่มต้นที่นี่
│   ├── menu.bat                    ← เมนูหลัก (แนะนำ!)
│   ├── start.bat                   ← เริ่มระบบ
│   └── check_system.bat            ← ตรวจสอบก่อนรัน
│
├── 📖 เอกสาร
│   ├── INSTALLATION_GUIDE.md       ← คู่มือติดตั้งฉบับเต็ม
│   ├── PROJECT_SUMMARY.md          ← สรุปโปรเจค
│   └── README.md                   ← ไฟล์นี้
│
├── 🔧 การตั้งค่า
│   ├── docker-compose.yml          ← Docker configuration
│   ├── Flow 2 โพสต์ข่าว.json       ← n8n workflow
│   └── .env.example                ← Environment variables
│
├── 🐳 Services
│   ├── youtube-downloader-api/     ← FastAPI service
│   └── scripts/                    ← Python scripts
│
└── 📦 Downloads (auto-created)
    └── downloads/                   ← วิดีโอชั่วคราว
```

---

## ⚙️ การตั้งค่า Credentials

### ต้องตั้งค่า 3 อย่าง:

1. **🟢 Google Sheets**
   - สร้าง spreadsheet ใน Google Sheets
   - เชื่อมต่อผ่าน OAuth2 ใน n8n

2. **🟣 OpenRouter (AI)**
   - สมัครที่: https://openrouter.ai/
   - รับ API Key
   - เติมเงินขั้นต่ำ $5

3. **🔵 Facebook Graph API**
   - สร้าง App ที่: https://developers.facebook.com/
   - รับ Access Token และขยายอายุ
   - ใส่ Page ID

📖 **คู่มือละเอียด:** อ่านใน [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## 🛠️ คำสั่งที่ใช้บ่อย

### การจัดการระบบ

```powershell
# เริ่มระบบ
docker-compose up -d

# ดูสถานะ
docker-compose ps

# ดู logs
docker-compose logs -f

# Restart
docker-compose restart

# หยุดระบบ
docker-compose down
```

### หรือใช้ Batch Files (ง่ายกว่า)

```powershell
menu.bat         # เมนูหลัก
start.bat        # เริ่มระบบ
status.bat       # ดูสถานะ
check_system.bat # ตรวจสอบ
```

---

## 🌐 URLs สำคัญ

| Service | URL | Credentials |
|---------|-----|-------------|
| 🎨 n8n GUI | http://localhost:5678 | admin / admin123 |
| 🔧 YouTube API | http://localhost:8000 | - |
| 📚 API Docs | http://localhost:8000/docs | - |

---

## 🏗️ สถาปัตยกรรม

```
┌─────────────────────────────────────────────────────────┐
│                        n8n Workflow                     │
│  ┌───────────┐  ┌──────────┐  ┌──────────────────┐    │
│  │  Trigger  │→│  Google  │→│  Download Video  │    │
│  │  (Cron)   │  │  Sheets  │  │    (FastAPI)     │    │
│  └───────────┘  └──────────┘  └──────────────────┘    │
│                                         ↓               │
│  ┌───────────┐  ┌──────────┐  ┌──────────────────┐    │
│  │  Cleanup  │←│ Facebook │←│   AI Analysis    │    │
│  │   Files   │  │   Post   │  │ (Gemini/GPT-4)   │    │
│  └───────────┘  └──────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────┘
                          ↕
        ┌────────────────────────────────┐
        │   YouTube Downloader API        │
        │   (FastAPI + yt-dlp + ffmpeg)   │
        └────────────────────────────────┘
```

---

## 💰 ค่าใช้จ่าย

| Service | ราคา | หมายเหตุ |
|---------|------|----------|
| Docker | ฟรี | - |
| n8n | ฟรี | Self-hosted |
| Google Sheets | ฟรี | - |
| Facebook API | ฟรี | - |
| **OpenRouter (AI)** | **~$5-75/เดือน** | ขึ้นกับการใช้งาน |

**ประมาณการ AI:**
- 1 โพสต์ ≈ $0.01-0.05
- 50 โพสต์/วัน ≈ $15-75/เดือน

---

## 🐛 Troubleshooting

### ❌ Docker ไม่รัน
```powershell
# แก้ไข: เปิด Docker Desktop และรอจนไฟเป็นสีเขียว
```

### ❌ n8n เข้าไม่ได้
```powershell
# แก้ไข
docker-compose restart n8n

# ดู logs
docker-compose logs -f n8n
```

### ❌ วิดีโอดาวน์โหลดไม่ได้
```powershell
# ตรวจสอบ API
curl http://localhost:8000/health

# Restart API
docker-compose restart youtube-downloader-api
```

### ❌ Facebook โพสต์ไม่ได้
- ตรวจสอบ Access Token หมดอายุหรือไม่
- ตรวจสอบ Page ID ถูกต้อง
- ตรวจสอบ Permissions

📖 **Troubleshooting เพิ่มเติม:** [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

## 📚 เอกสารทั้งหมด

| ไฟล์ | คำอธิบาย |
|------|----------|
| [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md) | 📕 คู่มือติดตั้งฉบับเต็ม (เริ่มต้นที่นี่!) |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | 📘 สรุปโปรเจคและโครงสร้าง |
| [README.md](README.md) | 📗 ภาพรวมโปรเจค (ไฟล์นี้) |

---

## 🎓 เทคโนโลยีที่ใช้

- **[n8n](https://n8n.io/)** - Workflow Automation Platform
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python Web Framework
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - YouTube Video Downloader
- **[OpenRouter](https://openrouter.ai/)** - AI Gateway (Gemini, GPT-4)
- **[Docker](https://www.docker.com/)** - Containerization Platform
- **[Google Sheets API](https://developers.google.com/sheets/api)** - Job Queue Management
- **[Facebook Graph API](https://developers.facebook.com/docs/graph-api)** - Social Media Posting

---

## 📊 ข้อมูลเทคนิค

### AI Models รองรับ
- ✅ Google Gemini 2.5 Flash Lite
- ✅ OpenAI GPT-4o Latest
- ✅ Any OpenRouter compatible model

### วิดีโอฟอร์แมตรองรับ
- ✅ MP4
- ✅ YouTube URLs
- ✅ YouTube Shorts
- ⚠️ ต้องเป็น public video

### แพลตฟอร์มรองรับ
- ✅ Facebook Page
- 🔜 Twitter/X (ขยายได้)
- 🔜 Instagram (ขยายได้)
- 🔜 TikTok (ขยายได้)

---

## 🔐 ความปลอดภัย

### ⚠️ สิ่งสำคัญ:

1. **เปลี่ยนรหัสผ่าน n8n** จาก `admin123`
2. **อย่าแชร์** API Keys และ Tokens
3. **Backup workflows** เป็นประจำ
4. **ใช้ HTTPS** ในการ deploy production

---

## 🎯 Use Cases

### 1. ข่าวประจำวัน
- เพิ่ม URL ข่าวใน Google Sheets
- ระบบวิเคราะห์และโพสต์อัตโนมัติ

### 2. Content Curation
- รวบรวมวิดีโอจากหลายแหล่ง
- AI สรุปและสร้างแคปชั่น

### 3. Social Media Management
- กำหนดคิวงาน
- โพสต์แบบกระจายเวลา

---

## 🚦 สถานะโปรเจค

- ✅ Core Features: **เสร็จสมบูรณ์**
- ✅ Documentation: **เสร็จสมบูรณ์**
- ✅ Docker Setup: **เสร็จสมบูรณ์**
- ⚠️ Production Ready: **ต้องตั้งค่า SSL/HTTPS**

---

## 📞 ติดต่อ/ช่วยเหลือ

หากมีปัญหา:
1. 📖 อ่าน [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
2. 🐛 ตรวจสอบ Troubleshooting section
3. 📝 ดู logs: `docker-compose logs -f`
4. 🔍 ตรวจสอบ Executions ใน n8n

---

## 📜 License

This project is for educational and personal use.

---

## 🌟 Credits

Powered by:
- n8n Workflow Automation
- OpenRouter AI Gateway
- Google Cloud Services
- Meta (Facebook) Developer Platform

---

**Version:** 1.0.0  
**Created:** 2024-11-21  
**Last Updated:** 2024-11-21

---

<div align="center">

### 🎉 พร้อมใช้งานแล้ว! เริ่มต้นด้วย `menu.bat` 🎉

**[📖 อ่านคู่มือการติดตั้ง](INSTALLATION_GUIDE.md)** | **[📊 ดูสรุปโปรเจค](PROJECT_SUMMARY.md)**

Made with ❤️ using n8n, FastAPI, and AI

</div>
