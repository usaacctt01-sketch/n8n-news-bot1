import os
import time
import json
import pickle
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import threading

import logging

# Setup logging
logging.basicConfig(
    filename='tiktok_bot_v2.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class TikTokBot:
    def __init__(self):
        self.driver = None
        self.posted_links = []
        self.session_file = "tiktok_session.pkl"
        logging.info("TikTokBot V2 initialized")
        
    def init_driver(self, load_session=True):
        """Initialize Chrome driver with session support"""
        try:
            logging.info("Initializing Chrome Driver (Desktop Mode)...")
            options = ChromeOptions()
            
            # Use Chrome user data directory for persistent session
            user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
            if not os.path.exists(user_data_dir):
                os.makedirs(user_data_dir)
            
            options.add_argument(f"user-data-dir={user_data_dir}")
            options.add_argument("--profile-directory=TikTokBot")
            
            # Anti-detection options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
            options.add_argument("--start-maximized")
            options.add_argument("--disable-infobars")
            
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            })
            
            logging.info("Starting WebDriver...")
            self.driver = webdriver.Chrome(options=options)
            logging.info("WebDriver started successfully")
            
            # Execute CDP commands to hide automation
            try:
                self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => undefined
                        });
                    """
                })
            except:
                pass
                
            return True
            
        except Exception as e:
            logging.error(f"Failed to init driver: {e}")
            raise e
    
    def check_login_status(self, log_callback=None):
        """Check if already logged in"""
        try:
            self.driver.get("https://www.tiktok.com")
            time.sleep(3)
            
            # Check for user profile icon or button
            try:
                # Look for profile/avatar element (means logged in)
                profile_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-e2e='profile-icon'], span[data-e2e='nav-upload']")
                if profile_elements and len(profile_elements) > 0:
                    if log_callback:
                        log_callback("✅ ตรวจพบ Session ล็อกอินอยู่แล้ว!")
                    return True
            except:
                pass
            
            if log_callback:
                log_callback("❌ ยังไม่ได้ล็อกอิน หรือ Session หมดอายุ")
            return False
            
        except Exception as e:
            logging.error(f"Failed to check login status: {e}")
            return False
    
    def qr_login(self, log_callback=None):
        """Login via QR Code (Manual)"""
        try:
            if log_callback:
                log_callback("📱 เปิดหน้า QR Code Login...")
            
            self.driver.get("https://www.tiktok.com/login/qrcode")
            time.sleep(3)
            
            if log_callback:
                log_callback("⏳ กรุณาสแกน QR Code ด้วยแอป TikTok บนมือถือ...")
            
            # Wait for successful login (check URL change or profile element appears)
            max_wait = 300  # 5 minutes
            start_time = time.sleep
            
            for _ in range(max_wait):
                try:
                    current_url = self.driver.current_url
                    # If redirected from login page
                    if "login" not in current_url.lower():
                        # Double check by looking for profile icon
                        profile_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[data-e2e='profile-icon']")
                        if profile_elements:
                            if log_callback:
                                log_callback("✅ ล็อกอินสำเร็จ!")
                            return True
                except:
                    pass
                time.sleep(1)
            
            raise Exception("QR Code Login Timeout (5 นาที)")
            
        except Exception as e:
            if log_callback:
                log_callback(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            return False
    
    def upload_video(self, video_path, caption, log_callback=None):
        """Upload video to TikTok (Desktop Upload Page)"""
        try:
            if log_callback:
                log_callback(f"📤 กำลังอัพโหลดวิดีโอ: {os.path.basename(video_path)}")
            
            # Go to upload page (Desktop)
            self.driver.get("https://www.tiktok.com/creator-center/upload")
            time.sleep(5)
            
            # Alternative: direct upload URL
            if "upload" not in self.driver.current_url.lower():
                self.driver.get("https://www.tiktok.com/upload")
                time.sleep(5)
            
            # Find file input
            if log_callback:
                log_callback("🔍 กำลังค้นหาปุ่มอัพโหลด...")
            
            file_selectors = [
                "input[type='file']",
                "input[accept*='video']",
                "input[accept*='mp4']"
            ]
            
            file_input = None
            for selector in file_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for elem in elements:
                        # Check if element accepts video files
                        accept_attr = elem.get_attribute("accept")
                        if accept_attr and "video" in accept_attr:
                            file_input = elem
                            break
                    if file_input:
                        break
                except:
                    continue
            
            if not file_input:
                raise Exception("ไม่พบปุ่มอัพโหลดวิดีโอ - อาจยังไม่ได้ล็อกอิน หรือ TikTok เปลี่ยน Layout")
            
            # Upload file
            if log_callback:
                log_callback("⏫ กำลังอัพโหลดไฟล์...")
            
            abs_path = str(Path(video_path).absolute())
            file_input.send_keys(abs_path)
            time.sleep(10)  # Wait for upload to start
            
            #Wait for video processing
            if log_callback:
                log_callback("⏳ รอการประมวลผลวิดีโอ...")
            
            # Wait for processing (look for upload progress or completion)
            max_wait_upload = 120  # 2 minutes for upload
            uploaded = False
            for _ in range(max_wait_upload):
                try:
                    # Check if caption box appears (means upload done)
                    caption_elements = self.driver.find_elements(By.CSS_SELECTOR, "div[contenteditable='true'], div[data-text='true']")
                    if caption_elements:
                        uploaded = True
                        break
                except:
                    pass
                time.sleep(1)
            
            if not uploaded:
                raise Exception("อัพโหลดวิดีโอไม่สำเร็จ - Timeout")
            
            # Add caption
            if caption:
                if log_callback:
                    log_callback("✏️ กำลังใส่ Caption...")
                
                caption_selectors = [
                    "div[contenteditable='true']",
                    "div[data-text='true']",
                    "div[class*='DraftEditor']"
                ]
                
                caption_box = None
                for selector in caption_selectors:
                    try:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        for elem in elements:
                            if elem.is_displayed() and elem.is_enabled():
                                caption_box = elem
                                break
                        if caption_box:
                            break
                    except:
                        continue
                
                if caption_box:
                    try:
                        caption_box.click()
                        time.sleep(1)
                        caption_box.send_keys(caption)
                        time.sleep(2)
                    except:
                        if log_callback:
                            log_callback("⚠️ ใส่ Caption ไม่สำเร็จ (กรอกทีหลังได้)")
            
            # Click post button
            if log_callback:
                log_callback("🚀 กำลังโพสวิดีโอ...")
            
            post_button_selectors = [
                "button[data-e2e='upload-button']",
                "button[class*='upload-btn']",
                "//button[contains(text(), 'Post')]",
                "//button[contains(text(), 'โพสต์')]",
                "//div[contains(text(), 'Post')]",
                "//div[contains(@class, 'Button') and contains(., 'Post')]"
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    if selector.startswith("//"):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for elem in elements:
                        if elem.is_displayed() and elem.is_enabled():
                            post_button = elem
                            break
                    if post_button:
                        break
                except:
                    continue
            
            if not post_button:
                raise Exception("ไม่พบปุ่ม Post - เช็คหน้าจอ Chrome ว่ามีปุ่ม Post ไหม")
            
            post_button.click()
            
            # Wait for posting to complete
            if log_callback:
                log_callback("⏳ รอการโพสเสร็จสิ้น (อาจใช้เวลา 30-60 วินาที)...")
            
            time.sleep(15)
            
            # Try to get posted video link
            video_link = None
            try:
                # Wait for success page or redirect
                time.sleep(10)
                current_url = self.driver.current_url
                
                # Check if redirected to profile or video page
                if "tiktok.com/@" in current_url or "/video/" in current_url:
                    video_link = current_url
                else:
                    # Try to find the link in the page
                    link_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
                    if link_elements:
                        video_link = link_elements[0].get_attribute("href")
            except:
                pass
            
            if log_callback:
                log_callback("✅ โพสวิดีโอสำเร็จ!")
            
            if video_link:
                return video_link
            else:
                return "Posted successfully (link not found)"
            
        except Exception as e:
            if log_callback:
                log_callback(f"❌ เกิดข้อผิดพลาดในการอัพโหลด: {str(e)}")
            logging.error(f"Upload error: {e}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


class TikTokBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 TikTok Auto Post Bot V2")
        self.root.geometry("900x800")
        self.root.resizable(False, False)
        
        # Variables
        self.video_files = []
        self.caption = tk.StringVar()
        self.is_running = False
        self.is_logged_in = False
        self.bot = None
        self.posted_links = []
        
        # Setup UI
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#FE2C55", height=70)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🎵 TikTok Auto Post Bot V2",
            font=("Arial", 22, "bold"),
            bg="#FE2C55",
            fg="white"
        )
        title_label.pack(pady=18)
        
        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Login Section
        login_frame = tk.LabelFrame(main_frame, text="🔐 Step 1: QR Code Login", padx=15, pady=15, font=("Arial", 11, "bold"))
        login_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_label = tk.Label(
            login_frame,
            text="✅ ใช้ QR Code เท่านั้น - ปลอดภัย รวดเร็ว ไม่โดนบล็อก\n💡 Browser จะจำ Session - ไม่ต้องสแกน QR ทุกครั้ง",
            font=("Arial", 10),
            fg="#333",
            justify=tk.LEFT
        )
        info_label.pack(anchor=tk.W, pady=(0, 12))
        
        # Login button and status
        login_btn_frame = tk.Frame(login_frame)
        login_btn_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.qr_login_btn = tk.Button(
            login_btn_frame,
            text="📱 QR Code Login",
            command=self.qr_login,
            bg="#25F4EE",
            fg="black",
            font=("Arial", 12, "bold"),
            width=20,
            height=2
        )
        self.qr_login_btn.pack(side=tk.LEFT, padx=(0, 15))
        
        self.login_status = tk.Label(
            login_btn_frame,
            text="❌ ยังไม่ได้ล็อกอิน",
            font=("Arial", 11, "bold"),
            fg="#FF6B6B"
        )
        self.login_status.pack(side=tk.LEFT)
        
        # Video Files Section
        video_frame = tk.LabelFrame(main_frame, text="🎬 Step 2: Video Files", padx=15, pady=15, font=("Arial", 11, "bold"))
        video_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Listbox
        listbox_frame = tk.Frame(video_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.video_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, height=8, font=("Arial", 10))
        self.video_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.video_listbox.yview)
        
        # Buttons
        btn_frame = tk.Frame(video_frame)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Button(btn_frame, text="➕ Add Videos", command=self.add_videos, bg="#25F4EE", fg="black", font=("Arial", 10, "bold"), height=1).pack(side=tk.LEFT, padx=(0, 8))
        tk.Button(btn_frame, text="🗑️ Clear All", command=self.clear_videos, bg="#E8E8E8", font=("Arial", 10)).pack(side=tk.LEFT)
        
        # Caption Section
        caption_frame = tk.LabelFrame(main_frame, text="✏️ Step 3: Caption (คำบรรยาย)", padx=15, pady=15, font=("Arial", 11, "bold"))
        caption_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Entry(caption_frame, textvariable=self.caption, width=80, font=("Arial", 10)).pack()
        tk.Label(caption_frame, text="ตัวอย่าง: Amazing video! #fyp #viral #trending", font=("Arial", 9), fg="gray").pack(anchor=tk.W, pady=(5, 0))
        
        # Control Buttons
        control_label = tk.Label(main_frame, text="🚀 Step 4: เริ่มโพสวิดีโอ", font=("Arial", 12, "bold"), fg="#FE2C55")
        control_label.pack(anchor=tk.W, pady=(0, 10))
        
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.start_btn = tk.Button(
            control_frame,
            text="🚀 Start Posting",
            command=self.start_posting,
            bg="#FE2C55",
            fg="white",
            font=("Arial", 14, "bold"),
            height=2,
            state=tk.DISABLED
        )
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))
        
        self.stop_btn = tk.Button(
            control_frame,
            text="⏹ Stop",
            command=self.stop_posting,
            bg="#FF6B6B",
            fg="white",
            font=("Arial", 14, "bold"),
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Log Section
        log_frame = tk.LabelFrame(main_frame, text="📋 Log", padx=15, pady=15, font=("Arial", 11, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, state=tk.DISABLED, font=("Consolas", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def add_videos(self):
        """Add video files"""
        files = filedialog.askopenfilenames(
            title="Select Video Files",
            filetypes=[
                ("Video Files", "*.mp4 *.mov *.avi *.mkv *.webm"),
                ("All Files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.video_files:
                self.video_files.append(file)
                self.video_listbox.insert(tk.END, os.path.basename(file))
    
    def clear_videos(self):
        """Clear all videos"""
        self.video_files.clear()
        self.video_listbox.delete(0, tk.END)
    
    def log(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def qr_login(self):
        """QR Code login"""
        self.qr_login_btn.config(state=tk.DISABLED, text="กำลังเปิด...")
        self.login_status.config(text="🔄 กำลังเปิด Chrome...", fg="#FFA500")
        
        thread = threading.Thread(target=self.qr_login_thread, daemon=True)
        thread.start()
    
    def qr_login_thread(self):
        """Thread for QR login"""
        try:
            self.log("🚀 เริ่มต้นระบบ...")
            
            # Initialize bot
            if not self.bot:
                self.bot = TikTokBot()
                self.bot.init_driver()
                self.log("✅ เปิด Chrome สำเร็จ")
            
            # Check if already logged in
            if self.bot.check_login_status(self.log):
                self.is_logged_in = True
                self.login_status.config(text="✅ ล็อกอินสำเร็จ! (จาก Session)", fg="#00C853")
                self.qr_login_btn.config(state=tk.DISABLED, text="✅ ล็อกอินแล้ว")
                self.start_btn.config(state=tk.NORMAL)
                self.log("✅ ใช้ Session ที่บันทึกไว้ - สามารถเริ่มโพสวิดีโอได้แล้ว!")
                return
            
            # Perform QR Login
            success = self.bot.qr_login(self.log)
            
            if success:
                self.is_logged_in = True
                self.login_status.config(text="✅ ล็อกอินสำเร็จ!", fg="#00C853")
                self.qr_login_btn.config(state=tk.DISABLED, text="✅ ล็อกอินแล้ว")
                self.start_btn.config(state=tk.NORMAL)
                self.log("✅ ล็อกอินสำเร็จ! สามารถเริ่มโพสวิดีโอได้แล้ว")
                self.root.after(0, lambda: messagebox.showinfo("สำเร็จ", "ล็อกอิน TikTok สำเร็จ!\nSession จะถูกบันทึกไว้ ครั้งหน้าไม่ต้องสแกน QR อีก 🎉"))
            else:
                self.login_status.config(text="❌ ล็อกอินไม่สำเร็จ", fg="#FF6B6B")
                self.qr_login_btn.config(state=tk.NORMAL, text="📱 QR Code Login")
                
        except Exception as e:
            self.log(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            self.login_status.config(text="❌ Error", fg="#FF6B6B")
            self.qr_login_btn.config(state=tk.NORMAL, text="📱 QR Code Login")
    
    def start_posting(self):
        """Start posting"""
        # Validate
        if not self.video_files:
            messagebox.showerror("Error", "กรุณาเลือกวิดีโอที่ต้องการโพส")
            return
        
        if not self.is_logged_in:
            messagebox.showerror("Error", "กรุณาล็อกอินก่อน")
            return
        
        # Disable buttons
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.qr_login_btn.config(state=tk.DISABLED)
        self.is_running = True
        
        # Clear log
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        
        # Start posting thread
        thread = threading.Thread(target=self.posting_thread, daemon=True)
        thread.start()
    
    def stop_posting(self):
        """Stop posting"""
        self.is_running = False
        self.log("⏹ กำลังหยุดการทำงาน...")
        self.stop_btn.config(state=tk.DISABLED)
    
    def posting_thread(self):
        """Thread for posting"""
        try:
            self.log("🚀 เริ่มต้นการโพสวิดีโอ...")
            
            # Post videos
            for i, video_path in enumerate(self.video_files):
                if not self.is_running:
                    break
                
                self.log(f"\n--- วิดีโอที่ {i+1}/{len(self.video_files)} ---")
                
                video_link = self.bot.upload_video(
                    video_path,
                    self.caption.get(),
                    log_callback=self.log
                )
                
                if video_link:
                    self.posted_links.append(video_link)
                    self.log(f"✅ โพสสำเร็จ: {video_link}")
                else:
                    self.log(f"❌ โพสไม่สำเร็จ")
                
                # Wait before next post
                if i < len(self.video_files) - 1 and self.is_running:
                    self.log("⏳ รอ 60 วินาทีก่อนโพสต่อไป (เพื่อหลบการตรวจจับสแปม)...")
                    time.sleep(60)
            
            self.log("\n🎉 เสร็จสิ้นการโพสทั้งหมด!")
            
            # Show summary
            if self.posted_links:
                self.log("\n📌 สรุปลิงก์ที่โพสแล้ว:")
                for idx, link in enumerate(self.posted_links, 1):
                    self.log(f"  {idx}. {link}")
            
        except Exception as e:
            self.log(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด:\n{str(e)}")
        
        finally:
            self.log("✨ การทำงานเสร็จสิ้น")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.qr_login_btn.config(state=tk.NORMAL if not self.is_logged_in else tk.DISABLED)
            self.is_running = False


def main():
    root = tk.Tk()
    app = TikTokBotGUI(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
