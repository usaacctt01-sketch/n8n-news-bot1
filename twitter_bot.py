import os
import time
import random
from pathlib import Path
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import json




class TwitterBot:
    def __init__(self, profile_path=None, browser_type="chrome", use_profile=True):
        self.profile_path = profile_path
        self.browser_type = browser_type.lower()
        self.use_profile = use_profile
        self.driver = None
        
    def init_driver(self):
        """Initialize browser driver with or without existing profile"""
        try:
            if self.browser_type == "chrome":
                self._init_chrome()
            elif self.browser_type == "edge":
                self._init_edge()
            elif self.browser_type == "firefox":
                self._init_firefox()
            else:
                raise ValueError(f"Unsupported browser: {self.browser_type}")
            
            self.driver.maximize_window()
            
        except Exception as e:
            raise Exception(f"ไม่สามารถเปิด {self.browser_type.title()} ได้: {str(e)}")
    
    def _init_chrome(self):
        """Initialize Chrome driver"""
        options = ChromeOptions()
        if self.use_profile and self.profile_path:
            options.add_argument(f"user-data-dir={self.profile_path}")
            # Add remote debugging port to allow multiple instances
            options.add_argument("--remote-debugging-port=9222")
        
        # Anti-detection options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Allow reusing profiles that are already in use
        options.add_argument("--disable-features=LockProfileCookieDatabase")
        
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        
        self.driver = webdriver.Chrome(options=options)
        
        # Execute CDP commands to hide automation
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en', 'th']
                    });
                """
            })
        except:
            pass
    
    def _init_edge(self):
        """Initialize Edge driver"""
        options = EdgeOptions()
        if self.use_profile and self.profile_path:
            options.add_argument(f"user-data-dir={self.profile_path}")
            # Add remote debugging port to allow multiple instances
            options.add_argument("--remote-debugging-port=9223")
        
        # Anti-detection options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0")
        
        # Allow reusing profiles that are already in use
        options.add_argument("--disable-features=LockProfileCookieDatabase")
        
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        
        self.driver = webdriver.Edge(options=options)
        
        # Execute CDP commands to hide automation
        try:
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['en-US', 'en', 'th']
                    });
                """
            })
        except:
            pass
    
    def _init_firefox(self):
        """Initialize Firefox driver"""
        options = FirefoxOptions()
        # Firefox uses different profile structure
        if self.use_profile and self.profile_path:
            options.add_argument("-profile")
            options.add_argument(self.profile_path)
        
        # Anti-detection preferences
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("useAutomationExtension", False)
        options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0")
        
        self.driver = webdriver.Firefox(options=options)
    
    def login_to_twitter(self, email, password, otp_code=None, log_callback=None):
        """Login to Twitter with email and password, with 2FA support"""
        try:
            if log_callback:
                log_callback("กำลังเข้าสู่หน้าล็อกอิน Twitter...")
            
            # Go to login page
            self.driver.get("https://twitter.com/i/flow/login")
            time.sleep(3)
            
            # Enter username/email
            if log_callback:
                log_callback("กำลังกรอก Email/Username...")
            
            username_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[autocomplete='username']"))
            )
            username_input.send_keys(email)
            time.sleep(1)
            
            # Click next button
            try:
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='LoginForm_Login_Next_Button']"))
                )
            except:
                next_button = self.driver.find_element(By.XPATH, "//span[text()='Next' or text()='ถัดไป']/..")
            
            next_button.click()
            time.sleep(2)
            
            # Enter password
            if log_callback:
                log_callback("กำลังกรอก Password...")
            
            password_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='password']"))
            )
            password_input.send_keys(password)
            time.sleep(1)
            
            # Click login button
            try:
                login_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='LoginForm_Login_Button']"))
                )
            except:
                login_button = self.driver.find_element(By.XPATH, "//span[text()='Log in' or text()='เข้าสู่ระบบ']/..")
            
            login_button.click()
            time.sleep(5)
            
            # Check if login was successful
            current_url = self.driver.current_url
            
            if "home" in current_url or "compose" in current_url:
                if log_callback:
                    log_callback("✓ ล็อกอินสำเร็จ!")
                return True
            
            # Check for error messages (e.g. Wrong password)
            try:
                error_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='toast'], [role='alert']")
                if error_element.is_displayed():
                    if log_callback:
                        log_callback(f"❌ Login Error: {error_element.text}")
                    return False
            except:
                pass
            
            # Check for 2FA/OTP requirement
            if log_callback:
                log_callback("⚠️ ตรวจพบ 2FA/Verification...")
            
            # If OTP code was provided, try to use it
            if otp_code:
                if log_callback:
                    log_callback(f"กำลังใส่ OTP Code: {otp_code}")
                
                try:
                    otp_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='text']"))
                    )
                    otp_input.send_keys(otp_code)
                    time.sleep(1)
                    
                    # Click next/verify button
                    try:
                        verify_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-testid='LoginForm_Login_Next_Button']"))
                        )
                    except:
                        verify_button = self.driver.find_element(By.XPATH, "//span[text()='Next' or text()='ถัดไป']/..")
                    
                    verify_button.click()
                    time.sleep(5)
                    
                    if "home" in self.driver.current_url or "compose" in self.driver.current_url:
                        if log_callback:
                            log_callback("✓ ล็อกอินสำเร็จด้วย OTP!")
                        return True
                    else:
                        raise Exception("OTP Code ไม่ถูกต้อง")
                        
                except Exception as e:
                    if log_callback:
                        log_callback(f"❌ ไม่สามารถใช้ OTP ได้: {str(e)}")
                    return False
            
            # If no OTP provided, return special code to show popup
            return "NEED_OTP"
            
        except Exception as e:
            raise Exception(f"เกิดข้อผิดพลาดในการล็อกอิน: {str(e)}")
        
    def open_twitter(self):
        """Open Twitter/X"""
        self.driver.get("https://twitter.com/compose/tweet")
        time.sleep(3)
        
    def post_tweet(self, media_path, hashtags, log_callback=None):
        """Post a tweet with media and hashtags"""
        try:
            if log_callback:
                log_callback(f"เริ่มโพสทวิต: {os.path.basename(media_path)}")
            
            # Navigate to compose tweet
            self.driver.get("https://twitter.com/compose/tweet")
            time.sleep(3)
            
            # Find and upload media
            if log_callback:
                log_callback("กำลังค้นหาปุ่มอัพโหลด...")
            
            # Try multiple selectors for file input
            file_input = None
            selectors = [
                "input[type='file']",
                "input[data-testid='fileInput']",
                "input[accept*='image']",
                "input[accept*='video']"
            ]
            
            for selector in selectors:
                try:
                    file_input = WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    if log_callback:
                        log_callback(f"✓ พบปุ่มอัพโหลด: {selector}")
                    break
                except:
                    continue
            
            if not file_input:
                raise Exception("ไม่พบปุ่มอัพโหลดไฟล์")
            
            # Upload the file
            if log_callback:
                log_callback("กำลังอัพโหลดไฟล์...")
            
            file_input.send_keys(str(Path(media_path).absolute()))
            time.sleep(3)
            
            # Wait for upload to complete
            if log_callback:
                log_callback("รอการอัพโหลดเสร็จสิ้น...")
            time.sleep(7)  # Increased wait time
            
            # Add text with hashtags
            if hashtags:
                if log_callback:
                    log_callback("กำลังเพิ่มแฮชแท็ก...")
                
                # Try multiple selectors for text box
                text_box = None
                text_selectors = [
                    "[data-testid='tweetTextarea_0']",
                    "[contenteditable='true'][role='textbox']",
                    ".public-DraftEditor-content",
                    "div[data-contents='true']"
                ]
                
                for selector in text_selectors:
                    try:
                        text_box = WebDriverWait(self.driver, 5).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                        )
                        if log_callback:
                            log_callback(f"✓ พบช่องใส่ข้อความ")
                        break
                    except:
                        continue
                
                if text_box:
                    hashtag_text = " ".join([f"#{tag.strip('#')}" for tag in hashtags.split()])
                    text_box.send_keys(hashtag_text)
                    time.sleep(2)
                else:
                    if log_callback:
                        log_callback("⚠️ ไม่พบช่องใส่ข้อความ - ข้ามการใส่แฮชแท็ก")
            
            # Click tweet button
            if log_callback:
                log_callback("กำลังมองหาปุ่มโพส...")
            
            # Try multiple selectors for tweet button
            tweet_button = None
            button_selectors = [
                "[data-testid='tweetButtonInline']",
                "[data-testid='tweetButton']",
                "button[data-testid='tweetButton']",
                "div[data-testid='tweetButton']",
                "//button[contains(@data-testid, 'tweet')]",
                "//span[text()='Post']/..",
                "//span[text()='Tweet']/.."
            ]
            
            for selector in button_selectors:
                try:
                    if selector.startswith("//"):
                        # XPath selector
                        tweet_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                    else:
                        # CSS selector
                        tweet_button = WebDriverWait(self.driver, 3).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                    
                    if log_callback:
                        log_callback(f"✓ พบปุ่มโพส")
                    break
                except:
                    continue
            
            if not tweet_button:
                raise Exception("ไม่พบปุ่มโพส - กรุณาตรวจสอบว่าล็อกอิน Twitter แล้ว")
            
            # Click the button
            if log_callback:
                log_callback("กำลังโพสทวิต...")
            
            tweet_button.click()
            
            # Wait for tweet to be posted
            time.sleep(6)
            
            if log_callback:
                log_callback("✓ โพสทวิตสำเร็จ!")
            
            return True
            
        except Exception as e:
            error_msg = str(e)
            if log_callback:
                log_callback(f"❌ เกิดข้อผิดพลาด: {error_msg}")
                
                # Additional debugging info
                try:
                    current_url = self.driver.current_url
                    log_callback(f"URL ปัจจุบัน: {current_url}")
                    
                    # Check if logged in
                    if "login" in current_url.lower():
                        log_callback("⚠️ ดูเหมือนว่ายังไม่ได้ล็อกอิน Twitter")
                except:
                    pass
            
            return False
    
    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()



class TwitterBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Twitter Auto Post Bot")
        self.root.geometry("800x900")  # Increased height for new controls
        self.root.resizable(False, False)
        
        # Variables
        self.media_files = []
        self.browser_type = tk.StringVar(value="Chrome")
        
        # Login method: "profile" or "credentials"
        self.login_method = tk.StringVar(value="normal")  # "normal", "profile", "credentials"
        self.browser_profile = tk.StringVar()
        self.twitter_email = tk.StringVar()
        self.twitter_password = tk.StringVar()
        
        self.hashtags = tk.StringVar()
        self.num_posts = tk.IntVar(value=1)
        self.interval_minutes = tk.IntVar(value=10)
        self.is_running = False
        self.bot = None
        
        # Load config if exists
        self.load_config()
        
        # Setup UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_frame = tk.Frame(self.root, bg="#1DA1F2", height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame, 
            text="🐦 Twitter Auto Post Bot", 
            font=("Arial", 20, "bold"),
            bg="#1DA1F2",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # Main container
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Browser Selection Section
        browser_frame = tk.LabelFrame(main_frame, text="Browser Selection", padx=10, pady=10)
        browser_frame.pack(fill=tk.X, pady=(0, 10))
        
        browser_select_frame = tk.Frame(browser_frame)
        browser_select_frame.pack(fill=tk.X)
        
        tk.Label(browser_select_frame, text="เลือกบราวเซอร์:", width=15, anchor=tk.W).pack(side=tk.LEFT)
        browser_combo = ttk.Combobox(
            browser_select_frame, 
            textvariable=self.browser_type,
            values=["Chrome", "Edge", "Firefox"],
            state="readonly",
            width=20
        )
        browser_combo.pack(side=tk.LEFT)
        browser_combo.bind("<<ComboboxSelected>>", self.on_browser_change)
        
        # Login Method Section
        login_frame = tk.LabelFrame(main_frame, text="วิธีการล็อกอิน Twitter", padx=10, pady=10)
        login_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(login_frame, text="เลือกวิธีการล็อกอิน:").pack(anchor=tk.W)
        
        # Radio buttons for login method
        radio_frame = tk.Frame(login_frame)
        radio_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Radiobutton(
            radio_frame,
            text="🌐 เปิดบราวเซอร์แบบธรรมดา (ต้องล็อกอินเอง)",
            variable=self.login_method,
            value="normal",
            command=self.toggle_login_controls
        ).pack(anchor=tk.W, pady=2)
        
        tk.Radiobutton(
            radio_frame,
            text="👤 ใช้ Profile ที่ล็อกอินไว้แล้ว (ปลอดภัย - แนะนำ)",
            variable=self.login_method,
            value="profile",
            command=self.toggle_login_controls
        ).pack(anchor=tk.W, pady=2)
        
        tk.Radiobutton(
            radio_frame,
            text="🔑 ล็อกอินอัตโนมัติด้วย Email/Password (สะดวก แต่มีความเสี่ยง)",
            variable=self.login_method,
            value="credentials",
            command=self.toggle_login_controls
        ).pack(anchor=tk.W, pady=2)
        
        # Profile Path Section (for profile method)
        self.profile_frame = tk.LabelFrame(main_frame, text="Browser Profile Path", padx=10, pady=10)
        self.profile_frame.pack(fill=tk.X, pady=(0, 10))
        
        profile_input_frame = tk.Frame(self.profile_frame)
        profile_input_frame.pack(fill=tk.X)
        
        self.profile_entry = tk.Entry(profile_input_frame, textvariable=self.browser_profile, width=60)
        self.profile_entry.pack(side=tk.LEFT, padx=(0, 5))
        self.profile_browse_btn = tk.Button(profile_input_frame, text="Browse", command=self.browse_profile)
        self.profile_browse_btn.pack(side=tk.LEFT)
        
        self.help_label = tk.Label(self.profile_frame, text="", font=("Arial", 8), fg="gray")
        self.help_label.pack(anchor=tk.W)
        
        # Credentials Section (for credentials method)
        self.credentials_frame = tk.LabelFrame(main_frame, text="Twitter Login Credentials", padx=10, pady=10)
        self.credentials_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Email
        email_frame = tk.Frame(self.credentials_frame)
        email_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(email_frame, text="Email/Username:", width=15, anchor=tk.W).pack(side=tk.LEFT)
        self.email_entry = tk.Entry(email_frame, textvariable=self.twitter_email, width=45)
        self.email_entry.pack(side=tk.LEFT)
        
        # Password
        password_frame = tk.Frame(self.credentials_frame)
        password_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(password_frame, text="Password:", width=15, anchor=tk.W).pack(side=tk.LEFT)
        self.password_entry = tk.Entry(password_frame, textvariable=self.twitter_password, width=45, show="•")
        self.password_entry.pack(side=tk.LEFT)
        
        # 2FA/OTP Code (optional)
        otp_frame = tk.Frame(self.credentials_frame)
        otp_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(otp_frame, text="2FA/OTP Code:", width=15, anchor=tk.W, fg="blue").pack(side=tk.LEFT)
        self.otp_var = tk.StringVar()
        self.otp_entry = tk.Entry(otp_frame, textvariable=self.otp_var, width=45)
        self.otp_entry.pack(side=tk.LEFT)
        tk.Label(otp_frame, text="(เว้นว่างถ้าไม่มี)", font=("Arial", 8), fg="gray").pack(side=tk.LEFT, padx=(5, 0))
        
        # Warning label
        warning_label = tk.Label(
            self.credentials_frame,
            text="⚠️ คำเตือน: ถ้ามี 2FA จะมี Popup ให้ใส่ OTP | แนะนำใช้ Profile แทน",
            font=("Arial", 8),
            fg="red"
        )
        warning_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Initialize visibility
        self.update_help_text()
        
        # Media Files Section
        self.media_frame = tk.LabelFrame(main_frame, text="Media Files (รูปภาพ/วิดีโอ)", padx=10, pady=10)
        self.media_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Media listbox
        listbox_frame = tk.Frame(self.media_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.media_listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set, height=8)
        self.media_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.media_listbox.yview)
        
        # Media buttons
        btn_frame = tk.Frame(self.media_frame)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        tk.Button(btn_frame, text="Add Files", command=self.add_media_files, bg="#1DA1F2", fg="white").pack(side=tk.LEFT, padx=(0, 5))
        tk.Button(btn_frame, text="Clear All", command=self.clear_media_files, bg="#E1E8ED").pack(side=tk.LEFT)
        
        # Initialize login controls visibility (after media_frame is created)
        self.toggle_login_controls()
        
        # Hashtags Section
        hashtag_frame = tk.LabelFrame(main_frame, text="Hashtags", padx=10, pady=10)
        hashtag_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Entry(hashtag_frame, textvariable=self.hashtags, width=70).pack()
        tk.Label(hashtag_frame, text="ตัวอย่าง: #Thailand #Bangkok #Travel", font=("Arial", 8), fg="gray").pack(anchor=tk.W)
        
        # Settings Section
        settings_frame = tk.LabelFrame(main_frame, text="Settings", padx=10, pady=10)
        settings_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Number of posts
        posts_frame = tk.Frame(settings_frame)
        posts_frame.pack(fill=tk.X, pady=(0, 5))
        tk.Label(posts_frame, text="จำนวนโพส:", width=20, anchor=tk.W).pack(side=tk.LEFT)
        tk.Spinbox(posts_frame, from_=1, to=100, textvariable=self.num_posts, width=10).pack(side=tk.LEFT)
        
        # Interval
        interval_frame = tk.Frame(settings_frame)
        interval_frame.pack(fill=tk.X)
        tk.Label(interval_frame, text="ช่วงเวลาระหว่างโพส (นาที):", width=20, anchor=tk.W).pack(side=tk.LEFT)
        tk.Spinbox(interval_frame, from_=1, to=1440, textvariable=self.interval_minutes, width=10).pack(side=tk.LEFT)
        
        # Control Buttons
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.start_btn = tk.Button(
            control_frame, 
            text="🚀 Start Posting", 
            command=self.start_posting,
            bg="#1DA1F2",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2
        )
        self.start_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.stop_btn = tk.Button(
            control_frame, 
            text="⏹ Stop", 
            command=self.stop_posting,
            bg="#E0245E",
            fg="white",
            font=("Arial", 12, "bold"),
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Log Section
        log_frame = tk.LabelFrame(main_frame, text="Log", padx=10, pady=10)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        log_scroll = tk.Scrollbar(log_frame)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.log_text = tk.Text(log_frame, height=8, yscrollcommand=log_scroll.set, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        log_scroll.config(command=self.log_text.yview)
    
    def on_browser_change(self, event=None):
        """Handle browser selection change"""
        self.update_help_text()
    
    def update_help_text(self):
        """Update help text based on selected browser"""
        browser = self.browser_type.get()
        
        if browser == "Chrome":
            help_text = "ตัวอย่าง: C:\\Users\\YourName\\AppData\\Local\\Google\\Chrome\\User Data"
        elif browser == "Edge":
            help_text = "ตัวอย่าง: C:\\Users\\YourName\\AppData\\Local\\Microsoft\\Edge\\User Data"
        elif browser == "Firefox":
            help_text = "ตัวอย่าง: C:\\Users\\YourName\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\xxxxxxxx.default"
        else:
            help_text = ""
        
        if hasattr(self, 'help_label'):
            self.help_label.config(text=help_text)
    
    def toggle_login_controls(self):
        """Show/hide controls based on selected login method"""
        method = self.login_method.get()
        
        # First, hide both frames
        self.profile_frame.pack_forget()
        self.credentials_frame.pack_forget()
        
        # Then show the appropriate one
        if method == "normal":
            # Hide both - already done above
            pass
            
        elif method == "profile":
            # Show profile only
            # Insert before media_frame
            self.profile_frame.pack(fill=tk.X, pady=(0, 10), before=self.media_frame)
            
        elif method == "credentials":
            # Show credentials only
            # Insert before media_frame
            self.credentials_frame.pack(fill=tk.X, pady=(0, 10), before=self.media_frame)
    
    def show_otp_dialog(self):
        """Show popup dialog for OTP/2FA code input"""
        # Create popup window
        dialog = tk.Toplevel(self.root)
        dialog.title("2FA/OTP Required")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Center the dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Header
        header = tk.Label(
            dialog,
            text="🔐 ตรวจพบ 2FA/Verification",
            font=("Arial", 14, "bold"),
            fg="#1DA1F2"
        )
        header.pack(pady=(20, 10))
        
        # Instruction
        instruction = tk.Label(
            dialog,
            text="กรุณาใส่ OTP Code หรือ Username\n(กรณี Twitter ถามหาชื่อผู้ใช้)",
            font=("Arial", 10)
        )
        instruction.pack(pady=(0, 15))
        
        # OTP Input
        otp_frame = tk.Frame(dialog)
        otp_frame.pack(pady=10)
        
        tk.Label(otp_frame, text="OTP Code:", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
        
        otp_var = tk.StringVar()
        otp_entry = tk.Entry(otp_frame, textvariable=otp_var, width=20, font=("Arial", 12))
        otp_entry.pack(side=tk.LEFT)
        otp_entry.focus()
        
        # Result variable
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
        button_frame.pack(pady=20)
        
        ok_btn = tk.Button(
            button_frame,
            text="✓ ตกลง",
            command=on_submit,
            bg="#1DA1F2",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            height=1
        )
        ok_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(
            button_frame,
            text="✗ ยกเลิก",
            command=on_cancel,
            bg="#E0245E",
            fg="white",
            font=("Arial", 10, "bold"),
            width=10,
            height=1
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to submit
        otp_entry.bind("<Return>", lambda e: on_submit())
        
        # Wait for dialog to close
        dialog.wait_window()
        
        return result["otp"] if result["submitted"] else None
        
    def browse_profile(self):
        """Browse for browser profile directory"""
        directory = filedialog.askdirectory()
        if directory:
            self.browser_profile.set(directory)
            
    def add_media_files(self):
        """Add media files to the list"""
        files = filedialog.askopenfilenames(
            title="Select Media Files",
            filetypes=[
                ("Media Files", "*.jpg *.jpeg *.png *.gif *.mp4 *.mov *.avi"),
                ("Images", "*.jpg *.jpeg *.png *.gif"),
                ("Videos", "*.mp4 *.mov *.avi"),
                ("All Files", "*.*")
            ]
        )
        
        for file in files:
            if file not in self.media_files:
                self.media_files.append(file)
                self.media_listbox.insert(tk.END, os.path.basename(file))
                
    def clear_media_files(self):
        """Clear all media files"""
        self.media_files.clear()
        self.media_listbox.delete(0, tk.END)
        
    def log(self, message):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        
    def validate_inputs(self):
        """Validate user inputs"""
        login_method = self.login_method.get()
        
        # Validate based on login method
        if login_method == "profile":
            if not self.browser_profile.get():
                messagebox.showerror("Error", f"กรุณาระบุ {self.browser_type.get()} Profile Path")
                return False
                
            if not os.path.exists(self.browser_profile.get()):
                messagebox.showerror("Error", f"{self.browser_type.get()} Profile Path ไม่ถูกต้อง")
                return False
                
        elif login_method == "credentials":
            if not self.twitter_email.get():
                messagebox.showerror("Error", "กรุณาใส่ Email/Username")
                return False
                
            if not self.twitter_password.get():
                messagebox.showerror("Error", "กรุณาใส่ Password")
                return False
        
        # Validate media files
        if not self.media_files:
            messagebox.showerror("Error", "กรุณาเพิ่มไฟล์รูปภาพหรือวิดีโอ")
            return False
            
        # Validate hashtags (optional warning)
        if not self.hashtags.get():
            result = messagebox.askyesno("Warning", "คุณไม่ได้ใส่แฮชแท็ก ต้องการดำเนินการต่อหรือไม่?")
            if not result:
                return False
                
        return True
        
    def start_posting(self):
        """Start the posting process"""
        if not self.validate_inputs():
            return
            
        # Save config
        self.save_config()
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Start posting in a separate thread
        thread = threading.Thread(target=self.posting_thread, daemon=True)
        thread.start()
        
    def stop_posting(self):
        """Stop the posting process"""
        self.is_running = False
        self.log("กำลังหยุดการทำงาน...")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
    def posting_thread(self):
        """Thread function for posting"""
        try:
            self.log("เริ่มต้นระบบ...")
            
            # Get login method and browser settings
            browser_name = self.browser_type.get()
            login_method = self.login_method.get()
            
            # Initialize bot based on login method
            if login_method == "profile":
                # Use profile
                profile_path = self.browser_profile.get()
                self.bot = TwitterBot(
                    profile_path=profile_path,
                    browser_type=browser_name.lower(),
                    use_profile=True
                )
                self.log(f"กำลังเปิด {browser_name} ด้วย Profile ที่ล็อกอินไว้...")
                
            elif login_method == "credentials":
                # Use email/password login
                self.bot = TwitterBot(
                    profile_path=None,
                    browser_type=browser_name.lower(),
                    use_profile=False
                )
                self.log(f"กำลังเปิด {browser_name} เพื่อล็อกอินอัตโนมัติ...")
                
            else:  # normal
                # Open normal browser
                self.bot = TwitterBot(
                    profile_path=None,
                    browser_type=browser_name.lower(),
                    use_profile=False
                )
                self.log(f"กำลังเปิด {browser_name} แบบธรรมดา...")
            
            # Initialize driver
            self.bot.init_driver()
            
            # Perform login if using credentials method
            if login_method == "credentials":
                email = self.twitter_email.get()
                password = self.twitter_password.get()
                otp_code = self.otp_var.get().strip() if hasattr(self, 'otp_var') else None
                
                self.log("กำลังล็อกอิน Twitter...")
                
                # Try login with OTP if provided
                login_result = self.bot.login_to_twitter(email, password, otp_code, log_callback=self.log)
                
                # If 2FA is required and no OTP was provided, show popup
                if login_result == "NEED_OTP":
                    self.log("⚠️ ต้องการ 2FA/OTP Code!")
                    self.log("กำลังแสดง Popup สำหรับใส่ OTP...")
                    
                    # Show OTP dialog
                    otp_code = self.show_otp_dialog()
                    
                    if otp_code:
                        self.log(f"ได้รับ OTP Code แล้ว กำลังลองล็อกอินอีกครั้ง...")
                        # Try login again with OTP
                        login_result = self.bot.login_to_twitter(email, password, otp_code, log_callback=self.log)
                        
                        if not login_result or login_result == "NEED_OTP":
                            raise Exception("ล็อกอินไม่สำเร็จแม้ใส่ OTP แล้ว - โปรดตรวจสอบ OTP Code")
                    else:
                        raise Exception("ยกเลิกการล็อกอิน - ไม่ได้ใส่ OTP Code")
                
                elif not login_result:
                    raise Exception("ล็อกอินไม่สำเร็จ - โปรดตรวจสอบ Email/Password")
            
            self.log("กำลังเปิด Twitter...")
            self.bot.open_twitter()
            
            num_posts = self.num_posts.get()
            interval = self.interval_minutes.get() * 60  # Convert to seconds
            
            self.log(f"จะโพสทั้งหมด {num_posts} โพส")
            self.log(f"ช่วงเวลาระหว่างโพส: {self.interval_minutes.get()} นาที")
            
            for i in range(num_posts):
                if not self.is_running:
                    break
                    
                self.log(f"\n--- โพสที่ {i+1}/{num_posts} ---")
                
                # Select random media file
                media_file = random.choice(self.media_files)
                
                # Post tweet
                success = self.bot.post_tweet(
                    media_file, 
                    self.hashtags.get(),
                    log_callback=self.log
                )
                
                if success:
                    self.log(f"โพสสำเร็จ! ({i+1}/{num_posts})")
                else:
                    self.log(f"โพสไม่สำเร็จ ({i+1}/{num_posts})")
                
                # Wait for next post
                if i < num_posts - 1 and self.is_running:
                    next_post_time = datetime.now() + timedelta(seconds=interval)
                    self.log(f"โพสต่อไปในเวลา: {next_post_time.strftime('%H:%M:%S')}")
                    
                    # Wait with periodic checks
                    for _ in range(interval):
                        if not self.is_running:
                            break
                        time.sleep(1)
            
            self.log("\n✓ เสร็จสิ้นการโพสทั้งหมด!")
            
        except Exception as e:
            self.log(f"เกิดข้อผิดพลาด: {str(e)}")
            messagebox.showerror("Error", f"เกิดข้อผิดพลาด:\n{str(e)}")
            
        finally:
            if self.bot:
                self.log(f"กำลังปิด {self.browser_type.get()}...")
                self.bot.close()
            
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.is_running = False
            
    def save_config(self):
        """Save configuration to file"""
        config = {
            'browser_type': self.browser_type.get(),
            'login_method': self.login_method.get(),
            'browser_profile': self.browser_profile.get(),
            'twitter_email': self.twitter_email.get(),  # Save email but not password
            'hashtags': self.hashtags.get(),
            'num_posts': self.num_posts.get(),
            'interval_minutes': self.interval_minutes.get(),
            'media_files': self.media_files
        }
        
        try:
            with open('twitter_bot_config.json', 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Could not save config: {e}")
            
    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists('twitter_bot_config.json'):
                with open('twitter_bot_config.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                self.browser_type.set(config.get('browser_type', 'Chrome'))
                self.login_method.set(config.get('login_method', 'normal'))
                self.browser_profile.set(config.get('browser_profile', ''))
                self.twitter_email.set(config.get('twitter_email', ''))
                # Password is not saved for security
                self.hashtags.set(config.get('hashtags', ''))
                self.num_posts.set(config.get('num_posts', 1))
                self.interval_minutes.set(config.get('interval_minutes', 10))
                self.media_files = config.get('media_files', [])
                
                # Populate media listbox with saved files
                if hasattr(self, 'media_listbox'):
                    self.media_listbox.delete(0, tk.END)
                    for file_path in self.media_files:
                        if os.path.exists(file_path):
                            self.media_listbox.insert(tk.END, os.path.basename(file_path))
                        else:
                            # File doesn't exist anymore, remove from list
                            self.media_files.remove(file_path)
                
        except Exception as e:
            print(f"Could not load config: {e}")


def main():
    root = tk.Tk()
    _app = TwitterBotGUI(root)  # noqa: F841
    root.mainloop()


if __name__ == "__main__":
    main()
