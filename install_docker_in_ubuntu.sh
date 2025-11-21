#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                                                                    ║"
echo "║         🐳 ติดตั้ง Docker ใน Ubuntu อัตโนมัติ 🐳                   ║"
echo "║                                                                    ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""

# สี
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[1/8] Update package list"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sudo apt update
echo -e "${GREEN}✅ Update สำเร็จ${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[2/8] ติดตั้ง dependencies"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sudo apt install -y ca-certificates curl gnupg lsb-release
echo -e "${GREEN}✅ ติดตั้ง dependencies สำเร็จ${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[3/8] สร้างโฟลเดอร์สำหรับ keyrings"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sudo mkdir -p /etc/apt/keyrings
echo -e "${GREEN}✅ สร้างโฟลเดอร์สำเร็จ${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[4/8] เพิ่ม Docker GPG key"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo -e "${GREEN}✅ เพิ่ม GPG key สำเร็จ${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[5/8] เพิ่ม Docker repository"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
echo -e "${GREEN}✅ เพิ่ม repository สำเร็จ${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[6/8] Update package list อีกครั้ง"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sudo apt update
echo -e "${GREEN}✅ Update สำเร็จ${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[7/8] ติดตั้ง Docker (ใช้เวลา 5-10 นาที)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
echo -e "${GREEN}✅ ติดตั้ง Docker สำเร็จ!${NC}"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "[8/8] เริ่ม Docker service และตั้งค่า permissions"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
sudo service docker start
sudo usermod -aG docker $USER
echo -e "${GREEN}✅ เริ่ม Docker service สำเร็จ${NC}"
echo ""

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ ติดตั้ง Docker สำเร็จ! ✅                     ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "📌 ทดสอบ Docker:"
echo ""

docker --version
docker-compose version

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 เสร็จสมบูรณ์!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "ขั้นตอนถัดไป:"
echo ""
echo "1. ปิด Ubuntu terminal นี้"
echo "2. เปิด Ubuntu ใหม่"
echo "3. รันคำสั่ง:"
echo ""
echo -e "   ${BLUE}cd /mnt/g/เทสทวิต${NC}"
echo -e "   ${BLUE}docker-compose up -d${NC}"
echo ""
echo "4. เปิดเบราว์เซอร์:"
echo -e "   ${BLUE}http://localhost:5678${NC}"
echo ""
echo "   Username: admin"
echo "   Password: admin123"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
