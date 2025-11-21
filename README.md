# n8n Auto News Posting Bot

ระบบโพสต์ข่าวอัตโนมัติไปยัง Facebook โดยใช้ n8n workflow automation

## 🚀 คุณสมบัติ

- ✅ ตรวจสอบงานจาก Google Sheets ทุก 2 นาที
- ✅ ดาวน์โหลดวิดีโอจาก YouTube อัตโนมัติ
- ✅ สร้างคำบรรยายและแฮชแท็กภาษาไทยด้วย AI
- ✅ โพสต์ไปยัง Facebook Page อัตโนมัติ
- ✅ อัพเดทสถานะกลับไปยัง Google Sheets
- ✅ ลบไฟล์ชั่วคราวเมื่อโพสต์เสร็จ

## 🛠️ เทคโนโลยีที่ใช้

- **n8n** - Workflow Automation
- **FastAPI** - YouTube Downloader Service
- **Python** - Backend Scripts
- **Docker** - Containerization
- **OpenRouter AI** - Caption Generation
- **Facebook Graph API** - Social Media Posting

## 📋 ข้อกำหนดเบื้องต้น

- GitHub Account
- Render.com Account (Free tier)
- Google Sheets API Credentials
- OpenRouter API Key
- Facebook Page Access Token

## 🚀 Quick Start

### วิธีที่ 1: Deploy บน Render.com (แนะนำ)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/n8n-news-bot.git

# 2. ทำตามคู่มือ
เปิดไฟล์: RENDER_DEPLOYMENT_GUIDE.md
```

หรือรัน automated script:

```bash
# Windows
deploy_to_render.bat
```

### วิธีที่ 2: รัน Local (ต้องมี Docker)

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/n8n-news-bot.git
cd n8n-news-bot

# 2. Start services
docker-compose up -d

# 3. เข้าใช้งาน
เปิด: http://localhost:5678
Username: admin
Password: admin123
```

## 📂 โครงสร้างโปรเจค

```
n8n-news-bot/
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile.n8n              # Dockerfile for n8n
├── render.yaml                 # Render.com configuration
├── Flow 2 โพสต์ข่าว.json       # n8n workflow
├── youtube-downloader-api/     # YouTube Downloader Service
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
├── scripts/                    # Python scripts
│   ├── fetch_youtube_shorts.py
│   └── process_video.py
└── RENDER_DEPLOYMENT_GUIDE.md  # คู่มือ Deploy
```

## 🔧 การตั้งค่า

### 1. Google Sheets API

1. ไปที่: https://console.cloud.google.com/
2. สร้าง Project ใหม่
3. Enable Google Sheets API
4. สร้าง OAuth 2.0 Credentials
5. ใส่ใน n8n Credentials

### 2. OpenRouter API

1. สมัครที่: https://openrouter.ai/
2. Generate API Key
3. ใส่ใน n8n Credentials

### 3. Facebook Graph API

1. สร้าง Facebook App: https://developers.facebook.com/
2. ขอ Page Access Token
3. ใส่ใน n8n Credentials

## 📊 การใช้งาน

1. **เตรียม Google Sheets:**
   - สร้าง Sheet ตามโครงสร้างที่กำหนด
   - Columns: video_url, caption, status, post_id, posted_at

2. **Import Workflow:**
   - เข้า n8n Dashboard
   - Import from File: `Flow 2 โพสต์ข่าว.json`

3. **ตั้งค่า Credentials:**
   - Google Sheets OAuth2
   - OpenRouter API Key
   - Facebook Graph API Token

4. **Activate Workflow:**
   - คลิกสวิตช์ "Active"

5. **เพิ่มงานใน Google Sheets:**
   - วาง YouTube URL
   - ตั้ง status = "pending"
   - รอ 2 นาที

## 🆘 การแก้ปัญหา

### Workflow ไม่ทำงาน

- ตรวจสอบ Credentials ถูกต้อง
- ตรวจสอบ Google Sheets มีข้อมูล "pending"
- ดู Execution logs ใน n8n

### YouTube Download ล้มเหลว

- ตรวจสอบ YouTube URL ถูกต้อง
- ตรวจสอบ API service ทำงาน
- ดู logs: `docker-compose logs youtube-downloader-api`

### Facebook Post ล้มเหลว

- ตรวจสอบ Access Token ยังไม่หมดอายุ
- ตรวจสอบสิทธิ์ของ Token
- ตรวจสอบ Page ID ถูกต้อง

## 💰 ค่าใช้จ่าย

### Render.com Free Tier
- ✅ ฟรีตลอดไป
- ⚠️ Spin down หลัง 15 นาที idle
- ✅ 750 ชั่วโมง/เดือน

### Render.com Paid Plan
- 💲 $7/เดือน
- ✅ ไม่มี spin down
- ✅ รัน 24/7

## 📝 License

MIT License - ใช้ฟรีได้ตามต้องการ

## 🤝 Contributing

Pull requests are welcome!

## 📧 ติดต่อ

มีปัญหาหรือคำถาม? เปิด Issue บน GitHub

---

**สร้างด้วย ❤️ สำหรับการทำงานอัตโนมัติ**
