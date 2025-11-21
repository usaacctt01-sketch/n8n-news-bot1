import os
import time
import json
from pathlib import Path
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import random
from selenium.common.exceptions import NoSuchElementException


import logging

# Setup logging
logging.basicConfig(
    filename='bot_debug.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

class TikTokBot:
    def __init__(self):
        self.driver = None
        self.posted_links = []
        logging.info("TikTokBot initialized")
        
    def init_driver(self):
        """Initialize Chrome driver with random mobile emulation"""
        try:
            logging.info("Initializing Chrome Driver (Mobile Mode)...")
            options = ChromeOptions()
            
            # Random Mobile Devices List
            mobile_devices = [
                {
                    "name": "iPhone 14 Pro Max",
                    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
                    "width": 430, "height": 932, "pixelRatio": 3.0
                },
                {
                    "name": "iPhone 13",
                    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
                    "width": 390, "height": 844, "pixelRatio": 3.0
                },
                {
                    "name": "Samsung Galaxy S23 Ultra",
                    "userAgent": "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
                    "width": 412, "height": 915, "pixelRatio": 3.5
                },
                {
                    "name": "Google Pixel 7 Pro",
                    "userAgent": "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
                    "width": 412, "height": 892, "pixelRatio": 3.5
                },
                {
                    "name": "Samsung Galaxy Z Fold 4",
                    "userAgent": "Mozilla/5.0 (Linux; Android 12; SM-F936B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Mobile Safari/537.36",
                    "width": 360, "height": 800, "pixelRatio": 3.0
                }
            ]
            
            # Randomly select a device
            device = random.choice(mobile_devices)
            logging.info(f"📱 Emulating: {device['name']}")
            
            # Configure Mobile Emulation
            mobile_emulation = {
                "deviceMetrics": { "width": device["width"], "height": device["height"], "pixelRatio": device["pixelRatio"] },
                "userAgent": device["userAgent"]
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
            
            # Anti-detection options
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-extensions")
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
        except Exception as e:
            logging.error(f"Failed to init driver: {e}")
            raise e
    
    def type_like_human(self, element, text):
        """Type text like a human with random delays"""
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.1, 0.3))  # Random delay per keystroke
    
    def login(self, username, password, otp_callback=None, log_callback=None):
        """Login to TikTok (Mobile Flow with Human Behavior)"""
        try:
            if log_callback:
                log_callback("🔓 กำลังเข้าสู่หน้าล็อกอิน (Mobile Mode)...")
            
            # Go to main login page first (more natural)
            self.driver.get("https://www.tiktok.com/login")
            time.sleep(random.uniform(3, 5))
            
            # Click "Use phone / email / username" if present
            try:
                use_phone_btn = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'phone-or-email')] | //div[contains(text(), 'Use phone')]"))
                )
                use_phone_btn.click()
                time.sleep(random.uniform(2, 3))
            except:
                pass

            # Click "Log in with email or username" link if present
            try:
                email_link = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Log in with email')] | //p[contains(text(), 'Log in with email')]"))
                )
                email_link.click()
                time.sleep(random.uniform(1, 2))
            except:
                pass
            
            # Wait for login form
            if log_callback:
                log_callback("📝 กำลังกรอก Username/Email (พิมพ์แบบคน)...")
            
            # Try to find username input
            username_selectors = [
                "input[name='username']",
                "input[type='text']",
                "input[placeholder*='Email']",
                "input[placeholder*='username']"
            ]
            
            username_input = None
            for selector in username_selectors:
                try:
                    username_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if username_input.is_displayed():
                        break
                except:
                    continue
            
            if not username_input:
                # Fallback: Try direct URL if navigation failed
                self.driver.get("https://www.tiktok.com/login/phone-or-email/email")
                time.sleep(3)
                username_input = self.driver.find_element(By.CSS_SELECTOR, "input[name='username']")

            if not username_input:
                raise Exception("ไม่พบช่องใส่ Username/Email")
            
            username_input.click()
            time.sleep(1)
            username_input.clear()
            self.type_like_human(username_input, username)
            time.sleep(random.uniform(1, 2))
            
            # Find password input
            if log_callback:
                log_callback("🔑 กำลังกรอก Password...")
            
            password_selectors = [
                "input[type='password']",
                "input[name='password']"
            ]
            
            password_input = None
            for selector in password_selectors:
                try:
                    password_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if password_input.is_displayed():
                        break
                except:
                    continue
            
            if not password_input:
                raise Exception("ไม่พบช่องใส่ Password")
            
            password_input.click()
            time.sleep(1)
            password_input.clear()
            self.type_like_human(password_input, password)
            time.sleep(random.uniform(1, 2))
            
            # Click login button
            if log_callback:
                log_callback("🚀 กำลังกดปุ่มล็อกอิน...")
            
            login_button_selectors = [
                "button[type='submit']",
                "button[data-e2e='login-button']",
                "//button[contains(text(), 'Log in')]",
                "//div[contains(text(), 'Log in')]"
            ]
            
            login_button = None
            for selector in login_button_selectors:
                try:
                    if selector.startswith("//"):
                        login_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        login_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except:
                    continue
            
            if not login_button:
                raise Exception("ไม่พบปุ่มล็อกอิน")
            
            time.sleep(random.uniform(0.5, 1.5))
            login_button.click()
            time.sleep(5)
            
            # Monitor for OTP or Success
            max_retries = 10  # Increased wait time
            for _ in range(max_retries):
                current_url = self.driver.current_url
                page_source = self.driver.page_source.lower()
                
                # Case 1: OTP Required
                if "verify" in current_url.lower() or "code" in page_source or "otp" in page_source:
                    if log_callback:
                        log_callback("⚠️ ตรวจพบการขอ OTP!")
                    
                    if otp_callback:
                        otp_code = otp_callback() # Popup will show here
                        
                        if otp_code:
                            if log_callback:
                                log_callback(f"📱 กำลังใส่ OTP: {otp_code}")
                            
                            # Find OTP inputs
                            try:
                                otp_inputs = self.driver.find_elements(By.CSS_SELECTOR, "input[type='text'], input[type='tel']")
                                if otp_inputs:
                                    if len(otp_inputs) == 1:
                                        self.type_like_human(otp_inputs[0], otp_code)
                                    else:
                                        for i, char in enumerate(otp_code):
                                            if i < len(otp_inputs):
                                                otp_inputs[i].send_keys(char)
                            except:
                                pass
                            
                            time.sleep(2)
                            # Try to click verify button if exists
                            try:
                                verify_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Verify') or contains(text(), 'Confirm')]")
                                verify_btn.click()
                            except:
                                pass
                            
                            time.sleep(5)
                            continue
                
                # Case 2: Success
                if "login" not in current_url.lower() and ("tiktok.com" in current_url):
                    if log_callback:
                        log_callback("✅ ล็อกอินสำเร็จ!")
                    return True
                
                # Case 3: Error Message
                try:
                    error_el = self.driver.find_element(By.CSS_SELECTOR, "div[class*='Error'], span[class*='Error']")
                    error_msg = error_el.text
                    if "maximum number of attempts" in error_msg.lower():
                        raise Exception("โดนบล็อกชั่วคราว (Maximum attempts) - กรุณารอ 15-30 นาที หรือเปลี่ยน IP")
                except NoSuchElementException:
                    pass
                except Exception as e:
                    if "Maximum attempts" in str(e):
                        raise e
                
                time.sleep(2)
            
            # Final check
            if "login" not in self.driver.current_url.lower():
                return True
            else:
                raise Exception("Login Timeout")
                
        except Exception as e:
            if log_callback:
                log_callback(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            return False
    
    def upload_video(self, video_path, caption, log_callback=None):
        """Upload video to TikTok"""
        try:
            if log_callback:
                log_callback(f"📤 กำลังอัพโหลดวิดีโอ: {os.path.basename(video_path)}")
            
            # Go to upload page
            self.driver.get("https://www.tiktok.com/upload")
            time.sleep(3)
            
            # Find file input
            if log_callback:
                log_callback("🔍 กำลังค้นหาปุ่มอัพโหลด...")
            
            file_selectors = [
                "input[type='file']",
                "input[accept*='video']"
            ]
            
            file_input = None
            for selector in file_selectors:
                try:
                    file_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    break
                except:
                    continue
            
            if not file_input:
                raise Exception("ไม่พบปุ่มอัพโหลดวิดีโอ")
            
            # Upload file
            if log_callback:
                log_callback("⏫ กำลังอัพโหลดไฟล์...")
            
            file_input.send_keys(str(Path(video_path).absolute()))
            time.sleep(5)
            
            # Wait for upload to complete
            if log_callback:
                log_callback("⏳ รอการอัพโหลดเสร็จสิ้น...")
            
            # Wait longer for video processing
            time.sleep(10)
            
            # Add caption
            if caption:
                if log_callback:
                    log_callback("✏️ กำลังใส่ Caption...")
                
                caption_selectors = [
                    "div[contenteditable='true']",
                    "textarea",
                    "div[data-text='true']"
                ]
                
                caption_box = None
                for selector in caption_selectors:
                    try:
                        caption_box = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        break
                    except:
                        continue
                
                if caption_box:
                    caption_box.click()
                    time.sleep(1)
                    caption_box.send_keys(caption)
                    time.sleep(2)
            
            # Click post button
            if log_callback:
                log_callback("🚀 กำลังโพสวิดีโอ...")
            
            post_button_selectors = [
                "button[data-e2e='upload-button']",
                "//button[contains(text(), 'Post')]",
                "//button[contains(text(), 'โพสต์')]",
                "//div[contains(text(), 'Post')]/..",
                "//div[contains(text(), 'โพสต์')]/.."
            ]
            
            post_button = None
            for selector in post_button_selectors:
                try:
                    if selector.startswith("//"):
                        post_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        post_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    break
                except:
                    continue
            
            if not post_button:
                raise Exception("ไม่พบปุ่มโพส")
            
            post_button.click()
            
            # Wait for posting to complete
            if log_callback:
                log_callback("⏳ รอการโพสเสร็จสิ้น...")
            
            time.sleep(10)
            
            # Try to get posted video link
            video_link = None
            try:
                # Look for success message or video link
                time.sleep(5)
                current_url = self.driver.current_url
                
                # Check if redirected to profile or video page
                if "tiktok.com/@" in current_url or "/video/" in current_url:
                    video_link = current_url
                    if log_callback:
                        log_callback(f"🔗 ลิงก์วิดีโอ: {video_link}")
                else:
                    # Try to find the link in the page
                    link_elements = self.driver.find_elements(By.CSS_SELECTOR, "a[href*='/video/']")
                    if link_elements:
                        video_link = link_elements[0].get_attribute("href")
                        if log_callback:
                            log_callback(f"🔗 ลิงก์วิดีโอ: {video_link}")
            except:
                pass
            
            if log_callback:
                log_callback("✅ โพสวิดีโอสำเร็จ!")
            
            return video_link if video_link else "Posted successfully (link not available)"
            
        except Exception as e:
            if log_callback:
                log_callback(f"❌ เกิดข้อผิดพลาดในการอัพโหลด: {str(e)}")
            return None
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()


class TikTokBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 TikTok Auto Post Bot")
        self.root.geometry("900x800")
        self.root.resizable(False, False)
        
        # Variables
        self.video_files = []
        self.username = tk.StringVar()
        self.password = tk.StringVar()
        self.caption = tk.StringVar()
        self.is_running = False
        self.is_logged_in = False  # Track login status
        self.bot = None
        self.posted_links = []
        
        # Load config
        self.load_config()
        
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
            text="🎵 TikTok Auto Post Bot",
            font=("Arial", 22, "bold"),
            bg="#FE2C55",
            fg="white"
        )
        title_label.pack(pady=18)
        
        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Login Section
        login_frame = tk.LabelFrame(main_frame, text="🔐 Step 1: TikTok Login", padx=15, pady=15, font=("Arial", 11, "bold"))
        login_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Username
        user_frame = tk.Frame(login_frame)
        user_frame.pack(fill=tk.X, pady=(0, 8))
        tk.Label(user_frame, text="Username/Email:", width=18, anchor=tk.W, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Entry(user_frame, textvariable=self.username, width=40, font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Password
        pass_frame = tk.Frame(login_frame)
        pass_frame.pack(fill=tk.X, pady=(0, 12))
        tk.Label(pass_frame, text="Password:", width=18, anchor=tk.W, font=("Arial", 10)).pack(side=tk.LEFT)
        tk.Entry(pass_frame, textvariable=self.password, width=40, show="•", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # Login button and status
        login_btn_frame = tk.Frame(login_frame)
        login_btn_frame.pack(fill=tk.X, pady=(0, 8))
        
        self.login_btn = tk.Button(
            login_btn_frame,
            text="🤖 Auto Login",
            command=self.test_login,
            bg="#25F4EE",
            fg="black",
            font=("Arial", 11, "bold"),
            width=15,
            height=1
        )
        self.login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.manual_login_btn = tk.Button(
            login_btn_frame,
            text="📲 QR Code Login",
            command=self.qr_login,
            bg="#FFFFFF",
            fg="black",
            font=("Arial", 11, "bold"),
            width=15,
            height=1
        )
        self.manual_login_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.login_status = tk.Label(
            login_btn_frame,
            text="❌ ยังไม่ได้ล็อกอิน",
            font=("Arial", 10, "bold"),
            fg="#FF6B6B"
        )
        self.login_status.pack(side=tk.LEFT)
        
        # Info label
        info_label = tk.Label(
            login_frame,
            text="💡 แนะนำ: ใช้ 'QR Code Login' เพื่อความรวดเร็วและไม่โดนบล็อก",
            font=("Arial", 9),
            fg="#666"
        )
        info_label.pack(anchor=tk.W, pady=(5, 0))
        
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
            state=tk.DISABLED  # Disabled until login
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
    
    def show_otp_dialog(self):
        """Show OTP input dialog"""
        dialog = tk.Toplevel(self.root)
        dialog.title("🔐 OTP Required")
        dialog.geometry("450x220")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (dialog.winfo_screenheight() // 2) - (220 // 2)
        dialog.geometry(f"450x220+{x}+{y}")
        
        # Header
        header = tk.Label(
            dialog,
            text="🔐 ตรวจพบ OTP/Verification",
            font=("Arial", 16, "bold"),
            fg="#FE2C55"
        )
        header.pack(pady=(25, 15))
        
        # Instruction
        instruction = tk.Label(
            dialog,
            text="กรุณาใส่ OTP Code ที่ส่งไปยังอีเมลหรือเบอร์โทรศัพท์",
            font=("Arial", 11)
        )
        instruction.pack(pady=(0, 20))
        
        # OTP Input
        otp_frame = tk.Frame(dialog)
        otp_frame.pack(pady=15)
        
        tk.Label(otp_frame, text="OTP Code:", font=("Arial", 11, "bold")).pack(side=tk.LEFT, padx=(0, 12))
        
        otp_var = tk.StringVar()
        otp_entry = tk.Entry(otp_frame, textvariable=otp_var, width=25, font=("Arial", 13))
        otp_entry.pack(side=tk.LEFT)
        otp_entry.focus()
        
        result = {"otp": None, "submitted": False}
        
        def on_submit():
            code = otp_var.get().strip()
            if code:
                result["otp"] = code
                result["submitted"] = True
                dialog.destroy()
            else:
                messagebox.showwarning("คำเตือน", "กรุณาใส่ OTP Code", parent=dialog)
        
        def on_cancel():
            result["submitted"] = False
            dialog.destroy()
        
        # Buttons
        button_frame = tk.Frame(dialog)
        button_frame.pack(pady=25)
        
        ok_btn = tk.Button(
            button_frame,
            text="✓ ยืนยัน",
            command=on_submit,
            bg="#25F4EE",
            fg="black",
            font=("Arial", 11, "bold"),
            width=12,
            height=1
        )
        ok_btn.pack(side=tk.LEFT, padx=7)
        
        cancel_btn = tk.Button(
            button_frame,
            text="✗ ยกเลิก",
            command=on_cancel,
            bg="#FF6B6B",
            fg="white",
            font=("Arial", 11, "bold"),
            width=12,
            height=1
        )
        cancel_btn.pack(side=tk.LEFT, padx=7)
        
        otp_entry.bind("<Return>", lambda e: on_submit())
        
        dialog.wait_window()
        
        return result["otp"] if result["submitted"] else None
    
    def show_qr_instruction(self):
        """Show QR Code instruction popup"""
        self.qr_dialog = tk.Toplevel(self.root)
        self.qr_dialog.title("📱 Scan QR Code")
        self.qr_dialog.geometry("400x250")
        self.qr_dialog.resizable(False, False)
        self.qr_dialog.transient(self.root)
        
        # Center
        self.qr_dialog.update_idletasks()
        x = (self.qr_dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.qr_dialog.winfo_screenheight() // 2) - (250 // 2)
        self.qr_dialog.geometry(f"400x250+{x}+{y}")
        
        # Icon/Emoji
        tk.Label(
            self.qr_dialog,
            text="📱",
            font=("Arial", 40)
        ).pack(pady=(20, 5))
        
        # Header
        tk.Label(
            self.qr_dialog,
            text="กรุณาสแกน QR Code",
            font=("Arial", 16, "bold"),
            fg="#FE2C55"
        ).pack(pady=5)
        
        # Instruction
        tk.Label(
            self.qr_dialog,
            text="1. เปิดแอป TikTok บนมือถือ\n2. ไปที่หน้าโปรไฟล์ > เพิ่มเพื่อน > สแกน\n3. สแกน QR Code ที่หน้าจอ Chrome",
            font=("Arial", 11),
            justify=tk.LEFT
        ).pack(pady=15)
        
        # Status
        self.qr_status_label = tk.Label(
            self.qr_dialog,
            text="⏳ กำลังรอการสแกน...",
            font=("Arial", 10, "bold"),
            fg="#FFA500"
        )
        self.qr_status_label.pack(pady=5)
    
    def test_login(self):
        """Test login to TikTok"""
        # Validate
        if not self.username.get():
            messagebox.showerror("Error", "กรุณาใส่ Username/Email")
            return
        
        if not self.password.get():
            messagebox.showerror("Error", "กรุณาใส่ Password")
            return
        
        # Disable login button
        self.login_btn.config(state=tk.DISABLED, text="กำลังล็อกอิน...")
        self.manual_login_btn.config(state=tk.DISABLED)
        self.login_status.config(text="🔄 กำลังล็อกอิน...", fg="#FFA500")
        
        # Run login in thread
        thread = threading.Thread(target=self.login_thread, daemon=True)
        thread.start()
    
    def qr_login(self):
        """QR Code login to TikTok"""
        # Disable login button
        self.login_btn.config(state=tk.DISABLED)
        self.manual_login_btn.config(state=tk.DISABLED, text="กำลังเปิด...")
        self.login_status.config(text="🔄 กำลังเปิด Chrome...", fg="#FFA500")
        
        # Run QR login in thread
        thread = threading.Thread(target=self.qr_login_thread, daemon=True)
        thread.start()
    
    def qr_login_thread(self):
        """Thread for QR login"""
        try:
            self.log("🚀 เริ่มต้น QR Code Login...")
            
            # Initialize bot if not exists
            if not self.bot:
                self.bot = TikTokBot()
                self.bot.init_driver()
                self.log("✅ เปิด Chrome สำเร็จ")
            
            self.log("🌐 กำลังไปหน้าล็อกอิน...")
            self.bot.driver.get("https://www.tiktok.com/login")
            
            # Show popup instruction in main thread
            self.root.after(0, self.show_qr_instruction)
            
            self.log("⏳ กรุณาสแกน QR Code...")
            self.login_status.config(text="⏳ รอการสแกน QR...", fg="#FFA500")
            
            # Wait for login success (check URL or cookies)
            max_wait = 300  # 5 minutes
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                try:
                    current_url = self.bot.driver.current_url
                    # If user is on profile page or feed (not login page)
                    if "login" not in current_url.lower() and ("tiktok.com" in current_url):
                        # Double check by looking for login button (if gone, we are logged in)
                        login_btns = self.bot.driver.find_elements(By.CSS_SELECTOR, "button[data-e2e='login-button']")
                        if not login_btns:
                            self.is_logged_in = True
                            self.log("✅ ตรวจพบการล็อกอินสำเร็จ!")
                            break
                except:
                    pass
                time.sleep(2)
            
            # Close popup
            if hasattr(self, 'qr_dialog') and self.qr_dialog:
                self.root.after(0, self.qr_dialog.destroy)
            
            if self.is_logged_in:
                self.login_status.config(text="✅ ล็อกอินสำเร็จ!", fg="#00C853")
                self.login_btn.config(state=tk.DISABLED)
                self.manual_login_btn.config(state=tk.DISABLED, text="✅ ล็อกอินแล้ว")
                self.start_btn.config(state=tk.NORMAL)
                self.log("✅ ล็อกอินสำเร็จ! สามารถเริ่มโพสวิดีโอได้แล้ว")
                self.root.after(0, lambda: messagebox.showinfo("สำเร็จ", "ล็อกอิน TikTok สำเร็จ!\nสามารถเริ่มโพสวิดีโอได้แล้ว 🎉"))
            else:
                self.login_status.config(text="❌ หมดเวลาล็อกอิน", fg="#FF6B6B")
                self.login_btn.config(state=tk.NORMAL, text="🤖 Auto Login")
                self.manual_login_btn.config(state=tk.NORMAL, text="📲 QR Code Login")
                self.log("❌ หมดเวลาการล็อกอิน (5 นาที)")
                
        except Exception as e:
            self.log(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            self.login_status.config(text="❌ Error", fg="#FF6B6B")
            self.login_btn.config(state=tk.NORMAL, text="🤖 Auto Login")
            self.manual_login_btn.config(state=tk.NORMAL, text="📲 QR Code Login")
    
    def login_thread(self):
        """Thread for login"""
        try:
            self.log("🚀 เริ่มทดสอบการล็อกอิน...")
            
            # Initialize bot if not exists
            if not self.bot:
                self.bot = TikTokBot()
                self.bot.init_driver()
                self.log("✅ เปิด Chrome สำเร็จ")
            
            # Try to login
            login_success = self.bot.login(
                self.username.get(),
                self.password.get(),
                otp_callback=self.show_otp_dialog,
                log_callback=self.log
            )
            
            if login_success:
                self.is_logged_in = True
                self.login_status.config(text="✅ ล็อกอินสำเร็จ!", fg="#00C853")
                self.login_btn.config(state=tk.DISABLED, text="✅ ล็อกอินแล้ว")
                self.manual_login_btn.config(state=tk.DISABLED)
                self.start_btn.config(state=tk.NORMAL)  # Enable Start Posting button
                self.log("✅ ล็อกอินสำเร็จ! สามารถเริ่มโพสวิดีโอได้แล้ว")
                messagebox.showinfo("สำเร็จ", "ล็อกอิน TikTok สำเร็จ!\nสามารถเริ่มโพสวิดีโอได้แล้ว 🎉")
            else:
                self.is_logged_in = False
                self.login_status.config(text="❌ ล็อกอินไม่สำเร็จ", fg="#FF6B6B")
                self.login_btn.config(state=tk.NORMAL, text="🤖 Auto Login")
                self.manual_login_btn.config(state=tk.NORMAL)
                messagebox.showerror("ล็อกอินไม่สำเร็จ", "กรุณาตรวจสอบ Username/Password แล้วลองใหม่อีกครั้ง")
        
        except Exception as e:
            self.log(f"❌ เกิดข้อผิดพลาด: {str(e)}")
            self.is_logged_in = False
            self.login_status.config(text="❌ ล็อกอินไม่สำเร็จ", fg="#FF6B6B")
            self.login_btn.config(state=tk.NORMAL, text="🤖 Auto Login")
            self.manual_login_btn.config(state=tk.NORMAL)
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด:\n{str(e)}")
    
    def start_posting(self):
        """Start posting"""
        # Validate login first
        if not self.is_logged_in:
            messagebox.showerror("Error", "กรุณา Test Login ก่อนเริ่มโพสวิดีโอ!")
            return
        
        # Validate
        if not self.video_files:
            messagebox.showerror("Error", "กรุณาเพิ่มไฟล์วิดีโอ")
            return
        
        # Save config
        self.save_config()
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Start in thread
        thread = threading.Thread(target=self.posting_thread, daemon=True)
        thread.start()
    
    def stop_posting(self):
        """Stop posting"""
        self.is_running = False
        self.log("⏸️ กำลังหยุดการทำงาน...")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
    
    def posting_thread(self):
        """Thread for posting"""
        try:
            self.log("🚀 เริ่มต้นระบบ...")
            
            # Initialize bot if not exists (should exist from test_login)
            if not self.bot:
                self.bot = TikTokBot()
                self.bot.init_driver()
                self.log("✅ เปิด Chrome สำเร็จ")
            
            # Login only if not logged in
            if not self.is_logged_in:
                login_success = self.bot.login(
                    self.username.get(),
                    self.password.get(),
                    otp_callback=self.show_otp_dialog,
                    log_callback=self.log
                )
                
                if not login_success:
                    raise Exception("ล็อกอินไม่สำเร็จ")
                self.is_logged_in = True
            else:
                self.log("✅ ใช้ Session ที่ล็อกอินอยู่แล้ว")
            
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
                    self.log("⏳ รอ 30 วินาทีก่อนโพสต่อไป...")
                    time.sleep(30)
            
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
            # Don't close browser automatically to allow checking results
            # or close if user wants (maybe add option later)
            # For now, let's keep it open if it was a manual login, 
            # but since this is "Start Posting", usually we finish after done.
            # But user might want to see. Let's ask user or just leave it open?
            # The original requirement didn't specify, but usually auto bots close.
            # However, since we separated login, maybe we keep it open?
            # Let's close it for now to clean up, but maybe add a flag?
            # Actually, if we close it, the 'is_logged_in' becomes invalid.
            
            self.log("✨ การทำงานเสร็จสิ้น")
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.is_running = False
            
            # Note: We are NOT closing the browser here anymore so the user can see the result
            # or post more videos without re-login.
            # User can close manually or we can add a "Close Browser" button.
    
    def save_config(self):
        """Save configuration"""
        config = {
            'username': self.username.get(),
            'caption': self.caption.get(),
            'video_files': self.video_files
        }
        
        try:
            with open('tiktok_bot_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Could not save config: {e}")
    
    def load_config(self):
        """Load configuration"""
        try:
            if os.path.exists('tiktok_bot_config.json'):
                with open('tiktok_bot_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.username.set(config.get('username', ''))
                self.caption.set(config.get('caption', ''))
                self.video_files = config.get('video_files', [])
                
                # Populate listbox
                if hasattr(self, 'video_listbox'):
                    for file_path in self.video_files:
                        if os.path.exists(file_path):
                            self.video_listbox.insert(tk.END, os.path.basename(file_path))
        
        except Exception as e:
            print(f"Could not load config: {e}")


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
