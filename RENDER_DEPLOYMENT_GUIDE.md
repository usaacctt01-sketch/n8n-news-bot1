# 🚀 คู่มือ Deploy บน Render.com

## ✅ สิ่งที่ต้องเตรียม

1. **GitHub Account** - https://github.com/signup
2. **Render Account** - https://render.com/register
3. **Code บน GitHub** (push แล้ว)

---

## 📋 ขั้นตอนการ Deploy

### **ขั้นตอนที่ 1: สร้าง Render Account**

1. ไปที่: https://render.com/register
2. เลือก **"Sign up with GitHub"**
3. Authorize Render เข้าถึง GitHub

---

### **ขั้นตอนที่ 2: Deploy YouTube Downloader API**

1. **คลิก "New +"** ที่มุมบนขวา
2. เลือก **"Web Service"**
3. **Connect Repository:**
   - คลิก "Connect account" (ถ้ายังไม่ได้เชื่อม)
   - เลือก repository: `n8n-news-bot`
4. **กรอกข้อมูล:**
   - **Name:** `youtube-downloader-api`
   - **Region:** Singapore (ใกล้ไทยที่สุด)
   - **Branch:** `main`
   - **Root Directory:** `youtube-downloader-api`
   - **Environment:** `Docker`
   - **Dockerfile Path:** `./Dockerfile`
5. **เลือก Free Plan:**
   - Instance Type: **Free**
6. **Environment Variables:**
   - `DOWNLOAD_DIR` = `/downloads`
   - `TZ` = `Asia/Bangkok`
7. **คลิก "Create Web Service"**
8. **รอ 5-10 นาที** ให้ deploy เสร็จ
9. **คัดลอก URL** ที่ได้ (เช่น `https://youtube-downloader-api.onrender.com`)

---

### **ขั้นตอนที่ 3: Deploy n8n**

1. **คลิก "New +" อีกครั้ง**
2. เลือก **"Web Service"**
3. **Connect Repository:**
   - เลือก repository: `n8n-news-bot`
4. **กรอกข้อมูล:**
   - **Name:** `n8n-automation`
   - **Region:** Singapore
   - **Branch:** `main`
   - **Root Directory:** (เว้นว่าง - ใช้ root)
   - **Environment:** `Docker`
   - **Dockerfile Path:** `./Dockerfile.n8n`
5. **เลือก Free Plan:**
   - Instance Type: **Free**
6. **Environment Variables:**
   ```
   N8N_BASIC_AUTH_ACTIVE=true
   N8N_BASIC_AUTH_USER=admin
   N8N_BASIC_AUTH_PASSWORD=admin123
   N8N_HOST=0.0.0.0
   N8N_PORT=5678
   N8N_PROTOCOL=https
   WEBHOOK_URL=https://n8n-automation.onrender.com
   NODE_ENV=production
   EXECUTIONS_PROCESS=main
   GENERIC_TIMEZONE=Asia/Bangkok
   TZ=Asia/Bangkok
   YOUTUBE_API_URL=https://youtube-downloader-api.onrender.com
   ```
   
   ⚠️ **แทน `https://youtube-downloader-api.onrender.com` ด้วย URL จริงจากขั้นตอนที่ 2**

7. **เพิ่ม Disk (สำคัญ!):**
   - คลิก "Add Disk"
   - **Name:** `n8n-data`
   - **Mount Path:** `/home/node/.n8n`
   - **Size:** 1 GB

8. **คลิก "Create Web Service"**
9. **รอ 5-10 นาที**

---

### **ขั้นตอนที่ 4: เข้าใช้งาน n8n**

1. **เมื่อ deploy เสร็จ** จะได้ URL เช่น:
   ```
   https://n8n-automation.onrender.com
   ```

2. **เปิดเบราว์เซอร์** ไปที่ URL นั้น

3. **Login:**
   ```
   Username: admin
   Password: admin123
   ```

4. **Import Workflow:**
   - คลิก menu (≡) บนซ้าย
   - เลือก "Import from File"
   - เลือกไฟล์: `Flow 2 โพสต์ข่าว.json`

5. **ตั้งค่า Credentials:**
   - Google Sheets OAuth2
   - OpenRouter API
   - Facebook Graph API

6. **Activate Workflow:**
   - คลิกสวิตช์ "Active" ให้เป็นสีเขียว

---

## ⚠️ ข้อจำกัดของ Free Plan

**Render Free Plan:**
- ✅ ฟรีตลอดไป
- ⚠️ **Spin down หลัง 15 นาทีที่ไม่มีการใช้งาน**
- ⚠️ **Cold start 30-60 วินาที** เมื่อมีคนเข้า
- ✅ 750 ชั่วโมง/เดือน
- ✅ Disk 1GB

**วิธีแก้ปัญหา Spin down:**

**Option 1: Ping ทุก 10 นาที (ฟรี)**

ใช้ **UptimeRobot** (https://uptimerobot.com):
1. สมัครฟรี
2. เพิ่ม Monitor
3. URL: `https://n8n-automation.onrender.com`
4. Monitoring Interval: 5 นาที

**Option 2: Upgrade เป็น Paid Plan** ($7/เดือน)
- ไม่มี spin down
- รัน 24/7

---

## 🔧 การอัพเดท Code

เมื่อคุณแก้ไข code:

```bash
cd "g:\เทสทวิต"
git add .
git commit -m "Update code"
git push
```

Render จะ **auto-deploy** ใหม่อัตโนมัติ!

---

## 📊 ดู Logs

1. เข้าไปที่ Render Dashboard
2. เลือก Service (n8n-automation หรือ youtube-downloader-api)
3. คลิก tab "Logs"
4. เห็น real-time logs

---

## 🆘 แก้ปัญหา

### **ปัญหา: Deploy failed**

1. ดู Logs ว่า error อะไร
2. ตรวจสอบ Dockerfile
3. ตรวจสอบ Environment Variables

### **ปัญหา: n8n เข้าไม่ได้**

1. ตรวจสอบว่า service status = "Live" (สีเขียว)
2. ตรวจสอบ URL ถูกต้องหรือไม่
3. ดู Logs

### **ปัญหา: Workflow ไม่ทำงาน**

1. ตรวจสอบ Credentials
2. ตรวจสอบ `YOUTUBE_API_URL` ตั้งค่าถูกต้อง
3. ตรวจสอบ Google Sheets มีข้อมูล "pending"

---

## 💰 ค่าใช้จ่าย

**Free Plan: $0/เดือน**
- ✅ พอใช้งานเบื้องต้นได้
- ⚠️ มี spin down

**Paid Plan: $7/เดือน**
- ✅ ไม่มี spin down
- ✅ รัน 24/7
- ✅ เร็วกว่า

---

## ✅ Checklist

- [ ] สร้าง GitHub account
- [ ] Push code ขึ้น GitHub
- [ ] สร้าง Render account
- [ ] Deploy youtube-downloader-api
- [ ] คัดลอก URL
- [ ] Deploy n8n
- [ ] ตั้งค่า YOUTUBE_API_URL
- [ ] เข้า n8n dashboard
- [ ] Import workflow
- [ ] ตั้งค่า credentials
- [ ] Activate workflow
- [ ] ทดสอบ

---

**เสร็จแล้ว! คุณมี Auto News Posting Bot ที่รันบน Cloud แล้ว! 🎉**
