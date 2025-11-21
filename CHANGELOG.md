# Changelog

All notable changes to Twitter Auto Post Bot will be documented in this file.

## [3.0.0] - 2025-11-21

### Added
- 🚀 **3 Login Methods**: 
  - Normal browser (manual login - recommended)
  - Profile-based (uses existing session)
  - Credentials-based (auto-login with email/password)
- 🔐 **2FA/OTP Support**: Popup dialog for entering OTP codes
- 🎭 **Anti-Detection System**: 
  - Hides automation flags from browser
  - Custom User-Agent
  - CDP commands to modify navigator properties
  - Disabled automation features
- 🔄 **Multiple Selector Support**: Tries multiple CSS/XPath selectors for better reliability
- 📊 **Better Error Logging**: Detailed error messages and debugging info

### Improved
- ⏱️ **Increased Wait Times**: Longer waits for media upload (3s → 7s) and posting (5s → 6s)
- 🎯 **Smart Element Finding**: Tries multiple selectors for file input, text box, and post button
- 🐛 **Enhanced Error Handling**: Better error messages with URL checking and login status detection
- 🔧 **Profile Unlocking**: Added options to use Chrome profile even when browser is running

### Changed
- GUI height increased from 750px to 900px for new login options
- Improved log messages with emoji indicators (✓, ❌, ⚠️)
- Updated README with all 3 login methods

### Technical
- Added `--remote-debugging-port` for Chrome/Edge
- Added `--disable-features=LockProfileCookieDatabase` for profile reuse
- Improved `post_tweet()` function with failover selectors
- Added XPath selector support alongside CSS selectors

## [2.1.0] - 2024-11-20

### Fixed
- 🐛 **Login Selectors**: แก้ไขปัญหาหาปุ่มไม่เจอในภาษาไทย ("ถัดไป", "เข้าสู่ระบบ")
- 🔧 **Reliability**: เปลี่ยนไปใช้ `data-testid` เพื่อความแม่นยำในการค้นหาปุ่ม
- 🛡️ **Error Handling**: เพิ่มการตรวจสอบ Error Message จาก Twitter (เช่น รหัสผ่านผิด)
- 🔐 **OTP/Verification**: อัพเดทข้อความ Popup ให้รองรับกรณีที่ Twitter ถามหา Username

## [2.0.0] - 2024-11-20

### Added
- 🎉 **Multi-Browser Support**: ตอนนี้รองรับ Chrome, Edge และ Firefox
- Dropdown menu สำหรับเลือกบราวเซอร์ในหน้า GUI
- Dynamic help text ที่เปลี่ยนตามบราวเซอร์ที่เลือก
- Support สำหรับ Edge และ Firefox driver initialization
- Browser-specific profile path examples

### Changed
- เปลี่ยนชื่อ variable จาก `chrome_profile` เป็น `browser_profile`
- เปลี่ยน UI label จาก "Chrome Profile Path" เป็น "Browser Profile Path"
- อัพเดท validation messages ให้แสดงชื่อบราวเซอร์ที่เลือก
- อัพเดท log messages ให้แสดงชื่อบราวเซอร์ที่กำลังใช้งาน
- เพิ่มขนาดหน้าต่างเป็น 800x750 (จากเดิม 800x700)

### Fixed
- แก้ไข duplicate imports
- แก้ไข unused variable warnings
- ลบ unused Service imports ที่ไม่จำเป็น

## [1.0.0] - 2024-11

### Added
- ✨ Initial release
- Chrome browser support
- Auto posting with media (images/videos)
- Hashtag support
- Random media selection
- Configurable post intervals
- Config file save/load
- Real-time logging
- GUI interface with Tkinter
- Batch file for easy launching

### Features
- รองรับการอัพโหลดรูปภาพ (JPG, PNG, GIF)
- รองรับการอัพโหลดวิดีโอ (MP4, MOV, AVI)
- สุ่มเลือกไฟล์จากรายการ
- ตั้งจำนวนโพสและเวลาระหว่างโพส
- ใช้ Chrome Profile ที่ล็อกอินไว้แล้ว
- บันทึกการตั้งค่าอัตโนมัติ

---

## Version History Summary

- **v2.0.0**: Multi-browser support (Chrome + Edge + Firefox)
- **v1.0.0**: Initial release (Chrome only)

