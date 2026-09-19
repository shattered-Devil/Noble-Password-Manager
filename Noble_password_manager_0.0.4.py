# Noble Password Manager v0.0.4
# what added to this version listed in below :
#     1- we fix path management of the app for an installer version
#     2- add some new themes 
#     3- fixed some minor bugs and glitches 

import os
import json
import base64
import time
import secrets
import ctypes
import sys
import string
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import customtkinter as ctk
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- RTL Language Support ---
try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    BIDI_SUPPORT = True
except ImportError:
    BIDI_SUPPORT = False
    
def get_resource_path(relative_path: str) -> str:
    """Returns the absolute path to resources, working both in dev and inside compiled EXEs."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    elif hasattr(sys, '__nuitka_binary_dir'):
        return os.path.join(sys.__nuitka_binary_dir, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
# --- Configuration & File Paths ---

def get_app_data_dir() -> str:
    """Creates and returns the user's AppData directory for storing application data."""
    if sys.platform == "win32":
        base_dir = os.path.join(os.getenv('APPDATA', os.path.expanduser('~')), 'NoblePasswordManager')
    else:
        base_dir = os.path.join(os.path.expanduser('~'), '.NoblePasswordManager')
    
    os.makedirs(base_dir, exist_ok=True)
    return base_dir

APP_DIR = get_app_data_dir()
VAULT_FILE = os.path.join(APP_DIR, 'noble_vault.enc')
CONFIG_FILE = os.path.join(APP_DIR, 'noble_config.json')

# --- Localization Resource Matrix ---
TEXTS = {
    "English": {
        "app_name": "Noble Password Manager",
        "login_title": "Unlock Your Vault",
        "create_title": "Setup Master Password",
        "master_pass": "Master Password",
        "confirm_pass": "Confirm Master Password",
        "unlock_btn": "Unlock Vault",
        "create_btn": "Create Secure Vault",
        "reset_vault_btn": "Reset Master Password",
        "reset_warn": "WARNING: This will permanently delete ALL your saved passwords. Are you absolutely sure?",
        "add_entry": "+ Add New Entry",
        "my_vault": "My Vault",
        "settings": "Settings",
        "theme": "App Interface Theme:",
        "language": "App System Language:",
        "about": "About Application",
        "creator": "Creator: nima zahedi",
        "version": "Version: 0.0.4",
        "copyright": "Copyright © 2026 nima zahedi. All Rights Reserved.",
        "service_name": "Service Name (e.g. GitHub)",
        "username": "Username / Email Address",
        "password": "Password",
        "additional_info": "Additional Information / Notes",
        "save_btn": "Save Encrypted Entry",
        "empty_vault": "Your security vault is empty.",
        "select_service": "Select a service from the sidebar to inspect credentials.",
        "wrong_pass": "Incorrect Master Password verification failed.",
        "pass_mismatch": "Master passwords do not match! Please check entries.",
        "locked_out": "Security Lockout active! Try again in: {}",
        "error": "Security Alert",
        "success": "Operation Successful",
        "saved_msg": "Credentials securely written to the encrypted repository.",
        "search_holder": "Search services...",
        "category": "Category:",
        "category_lbl": "Category: {}",
        "all_cat": "All Categories",
        "fav_filter": "⭐ Favorites Only",
        "strength_lbl": "Password Strength: {}",
        "str_weak": "Weak",
        "str_medium": "Medium",
        "str_strong": "Strong",
        "str_excellent": "Excellent",
        "copy_btn": "Copy",
        "reveal": "👁",
        "hide": "🙈",
        "edit_btn": "Edit Entry",
        "lock_vault_btn": "Lock Vault Instantly",
        "auto_lock_lbl": "Inactivity Auto-Lock Timer:",
        "tray_lbl": "System Tray Minimization behavior:",
        "backup_btn": "Export Encrypted Backup File",
        "import_btn": "Import Encrypted Backup File",
        "backup_success": "Encrypted backup file exported successfully.",
        "import_warn": "WARNING: Importing a backup will completely overwrite your current vault. Do you want to continue?",
        "ctx_edit": "Edit Details",
        "ctx_fav": "Toggle Favorite State",
        "ctx_delete": "Delete Entry",
        "del_warn": "Are you sure you want to permanently delete credentials for: {}?",
        "time_disabled": "Disabled",
        "time_1m": "1 Minute",
        "time_5m": "5 Minutes",
        "time_15m": "15 Minutes",
        "time_30m": "30 Minutes" ,
        "change_pass_btn": "Change Master Password",
        "change_pass_title": "Change Master Password",
        "current_pass": "Current Password",
        "new_pass": "New Password",
        "change_pass_warn": "WARNING: If you forget your new master password, your vault will be permanently inaccessible. There is no recovery option.",
        "Change master password " : " changing master password with your confirmation.",
        "pass_changed_success": "Master password successfully changed! The vault has been re-encrypted.",
        "accent_theme": "App Accent Color Theme:",
        "restart_warn": "App theme updated. A restart may be required to apply color changes everywhere.",
    },
    "Farsi": {
        "app_name": "مدیریت رمز عبور نجیب",
        "login_title": "قفل گاوصندوق را باز کنید",
        "create_title": "تنظیم رمز عبور اصلی",
        "master_pass": "رمز عبور اصلی",
        "confirm_pass": "تایید رمز عبور اصلی",
        "unlock_btn": "باز کردن قفل گاوصندوق",
        "create_btn": "ایجاد گاوصندوق امن",
        "reset_vault_btn": "بازنشانی رمز عبور اصلی",
        "reset_warn": "هشدار: این کار تمام رمزهای عبور ذخیره شده را برای همیشه حذف می کند. آیا کاملاً مطمئن هستید؟",
        "add_entry": "+ افزودن ورودی جدید",
        "my_vault": "گاوصندوق من",
        "settings": "تنظیمات سیستم",
        "theme": "پوسته ظاهری برنامه:",
        "language": "زبان سیستم برنامه:",
        "about": "درباره نرم‌افزار",
        "creator": "سازنده: نیما زاهدی",
        "version": "نسخه: 0.0.4",
        "copyright": "حق نشر © ۲۰۲۶ نیما زاهدی. تمامی حقوق محفوظ است.",
        "service_name": "نام سرویس (مانند گیت‌هاب)",
        "username": "نام کاربری / آدرس ایمیل",
        "password": "رمز عبور",
        "additional_info": "اطلاعات تکمیلی / یادداشت‌ها",
        "save_btn": "ذخیره ایمن و رمزگذاری شده",
        "empty_vault": "گاوصندوق امنیتی شما در حال حاضر خالی است.",
        "select_service": "برای مشاهده اطلاعات، یک سرویس را از منوی کناری انتخاب کنید.",
        "wrong_pass": "رمز عبور اصلی نادرست است. تأیید هویت ناموفق بود.",
        "pass_mismatch": "رمزهای عبور وارد شده مطابقت ندارند!",
        "locked_out": "قفل امنیتی فعال است! تلاش مجدد پس از: {}",
        "error": "هشدار امنیتی",
        "success": "عملیات موفق",
        "saved_msg": "اطلاعات با موفقیت رمزگذاری و در حافظه محلی ذخیره شد.",
        "search_holder": "جستجوی سرویس‌ها...",
        "category": "دسته‌بندی:",
        "category_lbl": "دسته‌بندی: {}",
        "all_cat": "همه دسته‌ها",
        "fav_filter": "⭐ فقط علاقه‌مندی‌ها",
        "strength_lbl": "قدرت رمز عبور: {}",
        "str_weak": "ضعیف",
        "str_medium": "متوسط",
        "str_strong": "قوی",
        "str_excellent": "عالی",
        "copy_btn": "کپی",
        "reveal": "👁",
        "hide": "🙈",
        "edit_btn": "ویرایش اطلاعات",
        "lock_vault_btn": "قفل کردن فوری گاوصندوق",
        "auto_lock_lbl": "زمان‌سنج قفل خودکار عدم فعالیت:",
        "tray_lbl": "رفتار کمینه شدن در نوار وظیفه (Tray):",
        "backup_btn": "خروجی پشتیبان رمزگذاری شده",
        "import_btn": "وارد کردن فایل پشتیبان",
        "backup_success": "فایل پشتیبان رمزگذاری شده با موفقیت صادر شد.",
        "import_warn": "هشدار: وارد کردن فایل پشتیبان، گاوصندوق فعلی شما را کاملاً جایگزین می‌کند. ادامه می‌دهید؟",
        "ctx_edit": "ویرایش جزئیات",
        "ctx_fav": "تغییر وضعیت علاقه‌مندی",
        "ctx_delete": "حذف ورودی",
        "del_warn": "آیا از حذف دائمی اطلاعات این سرویس اطمینان دارید: {}؟",
        "time_disabled": "غیرفعال",
        "time_1m": "۱ دقیقه",
        "time_5m": "۵ دقیقه",
        "time_15m": "۱۵ دقیقه",
        "time_30m": "۳۰ دقیقه",
        "change_pass_btn": "تغییر رمز عبور اصلی",
        "change_pass_title": "تغییر رمز عبور اصلی",
        "current_pass": "رمز عبور فعلی",
        "new_pass": "رمز عبور جدید",
        "change_pass_warn": "هشدار: در صورت فراموشی رمز عبور جدید، گاوصندوق شما برای همیشه غیرقابل دسترس خواهد بود. هیچ راه بازیابی وجود ندارد",
        "Change master password " :"تغییر رمز عبور اصلی",
        "pass_changed_success": "رمز عبور اصلی با موفقیت تغییر کرد! گاوصندوق مجدداً رمزگذاری شد.",
        "accent_theme": "رنگ‌بندی (تم) برنامه:",
        "restart_warn": "پوسته برنامه بروز شد. برای اعمال کامل رنگ‌ها ممکن است نیاز به راه‌اندازی مجدد برنامه باشد.",
    }
}
THEME_PRESETS = {
    "Dark": {
        "mode": "Dark",
        "color_theme": "blue",
        "bg": "#1a1a1a",
        "card_bg": "#2b2b2b"
    },
    "Light": {
        "mode": "Light",
        "color_theme": "blue",
        "bg": "#f3f4f6",
        "card_bg": "#ffffff"
    },
    "Midnight": {
        "mode": "Dark",
        "color_theme": "dark-blue",
        "bg": "#0b0f19",
        "card_bg": "#111827"
    },
    "OLED Black": {
        "mode": "Dark",
        "color_theme": "green",
        "bg": "#000000",
        "card_bg": "#121212"
    }
}
THEME_PRESETS = {
    "Dark": {
        "mode": "Dark",
        "color_theme": "blue",
        "bg": "#1a1a1a",
        "card_bg": "#2b2b2b"
    },
    "Light": {
        "mode": "Light",
        "color_theme": "blue",
        "bg": "#f3f4f6",
        "card_bg": "#ffffff"
    },
    "Midnight": {
        "mode": "Dark",
        "color_theme": "dark-blue",
        "bg": "#0b0f19",
        "card_bg": "#111827"
    },
    "OLED Black": {
        "mode": "Dark",
        "color_theme": "green",
        "bg": "#000000",
        "card_bg": "#121212"
    }
}

CATEGORIES = ["Login", "Work", "Personal", "Finance", "Social"]

def load_config() -> dict:
    defaults = {
        "failed_attempts": 0, 
        "lockout_until": 0.0, 
        "theme": "Dark", 
        "color_theme": "blue", 
        "language": "English", 
        "auto_lock_seconds": 300, 
        "tray_minimize": False
    }
    
    if not os.path.exists(CONFIG_FILE):
        return defaults
        
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            loaded_config = json.load(f)
            
        # Merge loaded config with defaults so new keys are added automatically
        for key, value in defaults.items():
            if key not in loaded_config:
                loaded_config[key] = value
                
        return loaded_config
    except Exception as e:
        print(f"Error reading config: {e}")
        return defaults  # Guarantees a dictionary is always returned, preventing the NoneType error

def save_config(config_data: dict):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f: json.dump(config_data, f, ensure_ascii=False, indent=4)

# --- Cryptographic Core Engine ---
def derive_key(master_password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=600_000)
    return base64.urlsafe_b64encode(kdf.derive(master_password.encode()))

def load_vault(master_password: str):
    if not os.path.exists(VAULT_FILE): return {"service_order": [], "entries": {}}, os.urandom(16)
    with open(VAULT_FILE, 'rb') as f: file_data = f.read()
    salt = file_data[:16]
    encrypted_data = file_data[16:]
    fernet = Fernet(derive_key(master_password, salt))
    try:
        parsed = json.loads(fernet.decrypt(encrypted_data).decode('utf-8'))
        if "entries" not in parsed: parsed = {"service_order": list(parsed.keys()), "entries": parsed}
        return parsed, salt
    except InvalidToken: return None, None

def save_vault(data: dict, master_password: str, salt: bytes):
    fernet = Fernet(derive_key(master_password, salt))
    encrypted_data = fernet.encrypt(json.dumps(data).encode('utf-8'))
    with open(VAULT_FILE, 'wb') as f: f.write(salt + encrypted_data)

def check_password_strength(password: str) -> tuple[float, str, str]:
    if not password: return 0.0, "Weak", "#ff4a4a"
    length = len(password)
    score = sum([length >= 8, length >= 14, any(c.isupper() for c in password) and any(c.islower() for c in password), any(c.isdigit() for c in password), any(c in string.punctuation for c in password)])
    if score <= 2: return 0.25, "Weak", "#ff4a4a"
    elif score == 3: return 0.50, "Medium", "#ffb84d"
    elif score == 4: return 0.75, "Strong", "#29a3a3"
    else: return 1.0, "Excellent", "#2eb872"
    


# --- Main Application Shell UI ---
class NoblePasswordManager(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Windows Taskbar App ID
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "Noble.PasswordManager.0.0.4 beta"
            )
        # 1. Set Windows Taskbar App ID (Fixes Taskbar grouping)
        if sys.platform == "win32":
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "NimaZahedi.NoblePasswordManager.0.0.4"
            )

        # 2. Load and Apply Icon to Titlebar and Taskbar
        self.icon_path = get_resource_path("app_icon.ico")
        if os.path.exists(self.icon_path):
            try:
                # Sets Title Bar Icon
                self.iconbitmap(self.icon_path)
            except Exception:
                pass

            try:
                # Sets Taskbar Icon (Keeps reference to prevent garbage collection)
                icon_img = Image.open(self.icon_path)
                self._app_icon_ref = ImageTk.PhotoImage(icon_img)
                self.wm_iconphoto(True, self._app_icon_ref)
            except Exception as e:
                print(f"Failed to load taskbar icon: {e}")

        
        self.config = load_config()
        
        # Initialize selected theme settings on startup
        current_theme = self.config.get("theme", "Dark")
        if current_theme not in THEME_PRESETS:
            current_theme = "Dark"
            
        preset = THEME_PRESETS[current_theme]
        ctk.set_appearance_mode(preset["mode"])
        ctk.set_default_color_theme(preset["color_theme"])
        self.configure(fg_color=preset["bg"])

        ctk.set_appearance_mode(self.config["theme"])
        ctk.set_default_color_theme("blue")

        self.title("Noble Password Manager")

        # ---------------- Icon ----------------
        icon_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "app_icon.ico"
        )

        if os.path.exists(icon_path):
            try:
                # Window icon
                self.iconbitmap(icon_path)

                # Extra compatibility
                try:
                    icon = tk.PhotoImage(file=icon_path)
                    self.iconphoto(True, icon)
                except Exception:
                    pass

            except Exception as e:
                print("Failed to load icon:", e)
        # --------------------------------------

        self.geometry("850x620")
        self.resizable(True, True)

        self.master_password = ""
        self.salt = b""
        self.vault_data = {"service_order": [], "entries": {}}
        self.selected_service = None
        self.is_password_visible = False
        
        # Auth visibility state and timer tracking
        self.is_auth_password_visible = False
        self.auth_hide_timer = None

        # Drag and Drop States
        self.dragged_service = None
        self.drag_start_y = 0
        self.drag_start_x = 0

        self.last_activity_timestamp = time.time()
        self.bind_all("<Any-KeyPress>", self.register_user_activity)
        self.bind_all("<Any-ButtonPress>", self.register_user_activity)
        self.check_inactivity_loop()
        self.protocol("WM_DELETE_WINDOW", self.handle_window_close)

        self.show_auth_screen()
        
    def bidi_format(self, text: str) -> str:
        """Reshapes and applies Right-to-Left formatting for Farsi text."""
        if self.config["language"] == "Farsi" and BIDI_SUPPORT:
            return get_display(arabic_reshaper.reshape(text))
        return text
    
    def apply_full_theme(self, theme_name: str):
        """Applies mode, accent color, and updates root/frame background colors dynamically."""
        preset = THEME_PRESETS.get(theme_name, THEME_PRESETS["Dark"])
        
        # Update CustomTkinter appearance mode & color theme
        ctk.set_appearance_mode(preset["mode"])
        ctk.set_default_color_theme(preset["color_theme"])
        
        # Dynamically set root window background
        self.configure(fg_color=preset["bg"])
        
        # Save choice to config
        self.config["theme"] = theme_name
        save_config(self.config)
        
        # Refresh current view to re-render frames with new background colors
        if hasattr(self, 'active_tab') and self.active_tab:
            self.show_panel(self.active_tab)
            
            
    def get_text(self, key: str, *format_args) -> str:
        """Fetches localized string, formats with arguments, and applies Bidi handling."""
        text = TEXTS[self.config["language"]].get(key, "")
        if format_args:
            text = text.format(*format_args)
        return self.bidi_format(text)

    def register_user_activity(self, event=None): self.last_activity_timestamp = time.time()
    
    def clear_layout(self): 
        # Safely cancel any pending auth hide timer to prevent TclError on destroyed widgets
        if hasattr(self, 'auth_hide_timer') and self.auth_hide_timer:
            self.after_cancel(self.auth_hide_timer)
            self.auth_hide_timer = None
            
        for widget in self.winfo_children(): widget.destroy()

    def check_inactivity_loop(self):
        if self.master_password and self.config["auto_lock_seconds"] > 0:
            if time.time() - self.last_activity_timestamp >= self.config["auto_lock_seconds"]:
                self.lock_vault_session()
                return
        self.after(2000, self.check_inactivity_loop)

    def lock_vault_session(self):
        self.master_password = ""
        self.salt = b""
        self.vault_data = {"service_order": [], "entries": {}}
        self.selected_service = None
        self.show_auth_screen()

    def handle_window_close(self):
        if self.config["tray_minimize"]: self.withdraw()
        else: self.destroy()

    # --- Authentication Screen ---
    def show_auth_screen(self):
        self.clear_layout()
        vault_exists = os.path.exists(VAULT_FILE)
        
        frame = ctk.CTkFrame(self, width=400, height=450)
        frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        ctk.CTkLabel(frame, text=self.get_text("app_name"), font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(35, 5))
        ctk.CTkLabel(frame, text=self.get_text("login_title" if vault_exists else "create_title"), font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0, 20))
        
        self.lockout_label = ctk.CTkLabel(frame, text="", font=ctk.CTkFont(size=12, weight="bold"), text_color="#ff4a4a")
        self.lockout_label.pack(pady=(0, 10))
        
        # Reset visibility state upon loading screen
        self.is_auth_password_visible = False
        
        # --- Master Password Field with Reveal Button ---
        pass_frame = ctk.CTkFrame(frame, fg_color="transparent")
        pass_frame.pack(pady=8)
        
        self.pass_entry = ctk.CTkEntry(pass_frame, placeholder_text=self.get_text("master_pass"), show="*", width=240)
        self.pass_entry.pack(side="left", padx=(0, 5))
        self.pass_entry.bind("<Return>", lambda e: self.handle_auth())
        
        self.auth_reveal_btn = ctk.CTkButton(pass_frame, text=self.get_text("reveal"), width=35, command=self.toggle_auth_password)
        self.auth_reveal_btn.pack(side="left")
        
        # --- Confirm Password Field (Only shown during vault creation) ---
        self.confirm_entry = None
        if not vault_exists:
            confirm_frame = ctk.CTkFrame(frame, fg_color="transparent")
            confirm_frame.pack(pady=8)
            
            self.confirm_entry = ctk.CTkEntry(confirm_frame, placeholder_text=self.get_text("confirm_pass"), show="*", width=240)
            self.confirm_entry.pack(side="left", padx=(0, 40)) 
            self.confirm_entry.bind("<Return>", lambda e: self.handle_auth())
            
        self.auth_btn = ctk.CTkButton(frame, text=self.get_text("unlock_btn" if vault_exists else "create_btn"), width=280, font=ctk.CTkFont(weight="bold"), command=self.handle_auth)
        self.auth_btn.pack(pady=(25, 10) if vault_exists else 25)
        
        # --- Reset Button if vault exists ---
        if vault_exists:
            self.reset_btn = ctk.CTkButton(frame, text=self.get_text("reset_vault_btn"), width=280, fg_color="#ff4a4a", hover_color="#cc3b3b", command=self.handle_vault_reset)
            self.reset_btn.pack(pady=(0, 10))
            
        self.enforce_lockout_check()

    def toggle_auth_password(self):
        if self.is_auth_password_visible:
            # Hide passwords
            self.pass_entry.configure(show="*")
            if self.confirm_entry:
                self.confirm_entry.configure(show="*")
            self.auth_reveal_btn.configure(text=self.get_text("reveal"))
            self.is_auth_password_visible = False
            
            # Cancel the auto-hide timer if it's currently running
            if self.auth_hide_timer:
                self.after_cancel(self.auth_hide_timer)
                self.auth_hide_timer = None
        else:
            # Show passwords
            self.pass_entry.configure(show="")
            if self.confirm_entry:
                self.confirm_entry.configure(show="")
            self.auth_reveal_btn.configure(text=self.get_text("hide"))
            self.is_auth_password_visible = True
            
            # Set auto-hide timer (5000 ms = 5 seconds)
            if self.auth_hide_timer:
                self.after_cancel(self.auth_hide_timer)
            self.auth_hide_timer = self.after(5000, self.force_hide_auth_password)

    def force_hide_auth_password(self):
        if getattr(self, 'is_auth_password_visible', False):
            self.toggle_auth_password()

    def handle_vault_reset(self):
        if messagebox.askyesno(self.get_text("error"), self.get_text("reset_warn")):
            if os.path.exists(VAULT_FILE):
                os.remove(VAULT_FILE)
            
            self.config["failed_attempts"] = 0
            self.config["lockout_until"] = 0.0
            save_config(self.config)
            
            self.master_password = ""
            self.salt = b""
            self.vault_data = {"service_order": [], "entries": {}}
            self.show_auth_screen()

    def enforce_lockout_check(self):
        current_time = time.time()
        if current_time < self.config["lockout_until"]:
            remaining = int(self.config["lockout_until"] - current_time)
            self.pass_entry.configure(state="disabled")
            if self.confirm_entry: self.confirm_entry.configure(state="disabled")
            self.auth_btn.configure(state="disabled")
            if hasattr(self, 'reset_btn'): self.reset_btn.configure(state="disabled")
            
            m, s = divmod(remaining, 60); h, m = divmod(m, 60)
            t_str = f"{h:02d}:{m:02d}:{s:02d}" if h > 0 else f"{m:02d}:{s:02d}"
            self.lockout_label.configure(text=self.get_text('locked_out', t_str))
            self.after(1000, self.enforce_lockout_check)
        else:
            self.pass_entry.configure(state="normal")
            if self.confirm_entry: self.confirm_entry.configure(state="normal")
            self.auth_btn.configure(state="normal")
            if hasattr(self, 'reset_btn'): self.reset_btn.configure(state="normal")
            self.lockout_label.configure(text="")

    def handle_auth(self):
        pwd = self.pass_entry.get()
        if not pwd: return

        if not os.path.exists(VAULT_FILE):
            if pwd != self.confirm_entry.get():
                messagebox.showerror(self.get_text("error"), self.get_text("pass_mismatch"))
                return
            self.master_password = pwd
            self.vault_data = {"service_order": [], "entries": {}}
            _, self.salt = load_vault(pwd)
            save_vault(self.vault_data, self.master_password, self.salt)
            self.show_dashboard()
            return

        data, salt = load_vault(pwd)
        if data is None:
            self.config["failed_attempts"] += 1
            attempts = self.config["failed_attempts"]
            penalty = 300 if attempts == 5 else 1800 if attempts == 6 else 3600 * (attempts - 5) if attempts >= 7 else 0
            if penalty > 0: self.config["lockout_until"] = time.time() + penalty
            save_config(self.config)
            messagebox.showerror(self.get_text("error"), self.get_text("wrong_pass"))
            self.enforce_lockout_check()
        else:
            self.config["failed_attempts"] = 0
            self.config["lockout_until"] = 0.0
            save_config(self.config)
            self.master_password = pwd; self.salt = salt; self.vault_data = data
            self.show_dashboard()

    # --- Dashboard Environment ---
    def show_dashboard(self):
        self.clear_layout()
        self.register_user_activity()
        
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        align = "w" if self.config["language"] == "English" else "e"
        
        self.sb_title = ctk.CTkLabel(self.sidebar, text=self.get_text("my_vault"), font=ctk.CTkFont(size=18, weight="bold"))
        self.sb_title.pack(pady=(15, 10), padx=20, anchor=align)
        
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.render_records_list())
        
        self.search_bar = ctk.CTkEntry(self.sidebar, placeholder_text=self.get_text("search_holder"), textvariable=self.search_var, height=28)
        if self.config["language"] == "Farsi":
            self.search_bar.configure(justify="right")
        self.search_bar.pack(fill="x", padx=15, pady=5)
        
        display_categories = [self.get_text("all_cat")] + [self.bidi_format(c) for c in CATEGORIES]
        
        self.cat_filter = ctk.CTkOptionMenu(self.sidebar, values=display_categories, command=lambda x: self.render_records_list(), height=28)
        self.cat_filter.pack(fill="x", padx=15, pady=5)
        
        self.fav_filter_var = tk.BooleanVar(value=False)
        self.fav_checkbox = ctk.CTkCheckBox(self.sidebar, text=self.get_text("fav_filter"), variable=self.fav_filter_var, command=self.render_records_list, font=ctk.CTkFont(size=12))
        self.fav_checkbox.pack(anchor=align, padx=20, pady=5)
        
        self.list_container = ctk.CTkScrollableFrame(self.sidebar, width=230)
        self.list_container.pack(expand=True, fill="both", padx=10, pady=5)
        
        self.add_entry_btn = ctk.CTkButton(self.sidebar, text=self.get_text("add_entry"), command=lambda: self.spawn_entry_modal(), font=ctk.CTkFont(weight="bold"))
        self.add_entry_btn.pack(pady=(10, 5), padx=15, fill="x")
        
        self.settings_btn = ctk.CTkButton(self.sidebar, text=self.get_text("settings"), fg_color="gray30", hover_color="gray40", command=self.show_settings_panel)
        self.settings_btn.pack(pady=(5, 15), padx=15, fill="x")
        
        self.workspace = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace.pack(side="right", expand=True, fill="both", padx=20, pady=20)
        
        self.context_menu = tk.Menu(self, tearoff=0, bg="#2b2b2b", fg="white", activebackground="#1f538d", activeforeground="white", borderwidth=0)
        
        self.render_records_list()
        if self.selected_service: self.inspect_record(self.selected_service)
        else: self.show_placeholder_workspace()

    def show_placeholder_workspace(self):
        for w in self.workspace.winfo_children(): w.destroy()
        placeholder = ctk.CTkLabel(self.workspace, text=self.get_text("select_service"), font=ctk.CTkFont(size=13), text_color="gray")
        placeholder.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)

    # --- Rendering & Drag-And-Drop ---
    def render_records_list(self):
        for widget in self.list_container.winfo_children(): widget.destroy()
        
        search_query = self.search_var.get().lower().strip()
        selected_category = self.cat_filter.get()
        
        raw_selected_cat = "All"
        if selected_category != self.get_text("all_cat"):
            for raw_cat in CATEGORIES:
                if self.bidi_format(raw_cat) == selected_category:
                    raw_selected_cat = raw_cat
                    break
                    
        filter_favorites = self.fav_filter_var.get()
        
        ordered_services = self.vault_data.get("service_order", [])
        for svc in list(self.vault_data["entries"].keys()):
            if svc not in ordered_services: ordered_services.append(svc)
        self.vault_data["service_order"] = ordered_services
        
        btn_align = "w" if self.config["language"] == "English" else "e"
        visible_entries_exist = False
        
        for service in ordered_services:
            if service not in self.vault_data["entries"]: continue
            entry = self.vault_data["entries"][service]
            
            if search_query and search_query not in service.lower() and search_query not in entry.get("username", "").lower(): continue
            if raw_selected_cat != "All" and entry.get("category", "Login") != raw_selected_cat: continue
            if filter_favorites and not entry.get("favorite", False): continue
            
            visible_entries_exist = True
            display_string = f"⭐  {service}" if entry.get("favorite", False) else f"    {service}"
            
            btn = ctk.CTkButton(
                self.list_container, text=self.bidi_format(display_string), 
                fg_color="transparent" if self.selected_service != service else "#1f538d", 
                text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), anchor=btn_align
            )
            btn.pack(pady=1, fill="x")
            
            btn.bind("<Button-1>", lambda event, s=service: self.on_drag_start(event, s))
            btn.bind("<ButtonRelease-1>", self.on_drag_release)
            btn.bind("<Button-3>", lambda event, s=service: self.spawn_context_menu(event, s))
            btn.bind("<Button-2>", lambda event, s=service: self.spawn_context_menu(event, s))
            
        if not visible_entries_exist:
            lbl = ctk.CTkLabel(self.list_container, text=self.get_text("empty_vault"), font=ctk.CTkFont(size=11), text_color="gray")
            lbl.pack(pady=10)

    def on_drag_start(self, event, service_name):
        self.dragged_service = service_name
        self.drag_start_y = event.y_root
        self.drag_start_x = event.x_root

    def on_drag_release(self, event):
        if not self.dragged_service: return
        dy = abs(event.y_root - self.drag_start_y)
        dx = abs(event.x_root - self.drag_start_x)
        
        if dy < 5 and dx < 5:
            self.inspect_record(self.dragged_service)
            self.dragged_service = None
            return
            
        if self.search_var.get().strip() or self.cat_filter.get() != self.get_text("all_cat") or self.fav_filter_var.get():
            self.dragged_service = None
            return

        release_y = event.y_root
        widgets = self.list_container.winfo_children()
        target_index = 0
        
        for i, w in enumerate(widgets):
            if isinstance(w, ctk.CTkButton):
                w_y = w.winfo_rooty()
                w_h = w.winfo_height()
                if release_y > w_y + (w_h / 2):
                    target_index = i + 1

        current_idx = self.vault_data["service_order"].index(self.dragged_service)
        self.vault_data["service_order"].pop(current_idx)
        if current_idx < target_index: target_index -= 1
        
        self.vault_data["service_order"].insert(target_index, self.dragged_service)
        save_vault(self.vault_data, self.master_password, self.salt)
        self.render_records_list()
        self.dragged_service = None

    # --- Context Menu Additions ---
    def spawn_context_menu(self, event, service_name):
        self.register_user_activity()
        self.context_menu.delete(0, tk.END)
        self.context_menu.add_command(label=self.get_text("ctx_edit"), command=lambda: self.spawn_entry_modal(service_name))
        self.context_menu.add_command(label=self.get_text("ctx_fav"), command=lambda: self.toggle_favorite_state(service_name))
        self.context_menu.add_separator()
        self.context_menu.add_command(label=self.get_text("ctx_delete"), command=lambda: self.delete_entry(service_name))
        self.context_menu.post(event.x_root, event.y_root)

    def toggle_favorite_state(self, service_name):
        self.vault_data["entries"][service_name]["favorite"] = not self.vault_data["entries"][service_name].get("favorite", False)
        save_vault(self.vault_data, self.master_password, self.salt)
        self.render_records_list()

    def delete_entry(self, service_name):
        if messagebox.askyesno(self.get_text("ctx_delete"), self.get_text('del_warn', service_name)):
            del self.vault_data["entries"][service_name]
            if service_name in self.vault_data["service_order"]:
                self.vault_data["service_order"].remove(service_name)
            save_vault(self.vault_data, self.master_password, self.salt)
            if self.selected_service == service_name:
                self.selected_service = None
                self.show_placeholder_workspace()
            self.render_records_list()

    # --- Records Inspection Pane Layer ---
    def inspect_record(self, service_name: str):
        self.register_user_activity()
        self.selected_service = service_name
        self.is_password_visible = False
        
        for w in self.workspace.winfo_children(): w.destroy()
        self.render_records_list() 
        
        entry = self.vault_data["entries"][service_name]
        align = "w" if self.config["language"] == "English" else "e"
        
        header_frame = ctk.CTkFrame(self.workspace, fg_color="transparent")
        header_frame.pack(fill="x", pady=(5, 15))
        ctk.CTkLabel(header_frame, text=self.bidi_format(service_name), font=ctk.CTkFont(size=22, weight="bold")).pack(side="left" if align=="w" else "right")
        ctk.CTkLabel(header_frame, text="⭐" if entry.get("favorite", False) else "", font=ctk.CTkFont(size=18)).pack(side="left" if align=="w" else "right", padx=10)
        
        cat_display = self.bidi_format(entry.get('category', 'Login'))
        ctk.CTkLabel(self.workspace, text=self.get_text("category_lbl", cat_display), font=ctk.CTkFont(size=12, slant="italic"), text_color="cyan").pack(anchor=align, pady=(0, 10))
        
        ctk.CTkLabel(self.workspace, text=self.get_text("username"), text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor=align)
        u_frame = ctk.CTkFrame(self.workspace, fg_color="transparent")
        u_frame.pack(fill="x", pady=(0, 15))
        u_field = ctk.CTkEntry(u_frame, width=420)
        u_field.insert(0, entry["username"])
        if self.config["language"] == "Farsi": u_field.configure(justify="right")
        u_field.configure(state="disabled")
        u_field.pack(side="left" if align=="w" else "right")
        ctk.CTkButton(u_frame, text=self.get_text("copy_btn"), width=60, command=lambda: self.copy_to_clipboard(entry["username"])).pack(side="left" if align=="w" else "right", padx=5)
        
        ctk.CTkLabel(self.workspace, text=self.get_text("password"), text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor=align)
        p_frame = ctk.CTkFrame(self.workspace, fg_color="transparent")
        p_frame.pack(fill="x", pady=(0, 5))
        
        self.p_field_inspect = ctk.CTkEntry(p_frame, width=420, show="*")
        self.p_field_inspect.insert(0, entry["password"])
        self.p_field_inspect.configure(state="disabled")
        self.p_field_inspect.pack(side="left" if align=="w" else "right")
        
        self.reveal_btn = ctk.CTkButton(p_frame, text=self.get_text("reveal"), width=30, command=self.toggle_password_visibility)
        self.reveal_btn.pack(side="left" if align=="w" else "right", padx=3)
        ctk.CTkButton(p_frame, text=self.get_text("copy_btn"), width=60, command=lambda: self.copy_to_clipboard(entry["password"])).pack(side="left" if align=="w" else "right", padx=2)
        
        strength_frame = ctk.CTkFrame(self.workspace, fg_color="transparent")
        strength_frame.pack(fill="x", pady=(0, 15))
        strength_val, strength_str, strength_color = check_password_strength(entry["password"])
        self.strength_meter = ctk.CTkProgressBar(strength_frame, width=250, progress_color=strength_color)
        self.strength_meter.set(strength_val)
        self.strength_meter.pack(side="left" if align=="w" else "right", pady=8)
        
        formatted_str = self.get_text('str_' + strength_str.lower())
        self.strength_label = ctk.CTkLabel(strength_frame, text=self.get_text("strength_lbl", formatted_str), text_color=strength_color, font=ctk.CTkFont(size=11, weight="bold"))
        self.strength_label.pack(side="left" if align=="w" else "right", padx=10)
        
        ctk.CTkLabel(self.workspace, text=self.get_text("additional_info"), text_color="gray", font=ctk.CTkFont(size=12)).pack(anchor=align)
        i_field = ctk.CTkTextbox(self.workspace, width=490, height=100)
        i_field.insert("1.0", entry.get("info", ""))
        if self.config["language"] == "Farsi": i_field.tag_config("rtl", justify="right"); i_field.tag_add("rtl", "1.0", "end")
        i_field.configure(state="disabled")
        i_field.pack(pady=(0, 15), anchor=align)
        
        ctk.CTkButton(self.workspace, text=self.get_text("edit_btn"), fg_color="#2eb872", hover_color="#25965d", command=lambda: self.spawn_entry_modal(service_name)).pack(anchor=align)

    def toggle_password_visibility(self):
        if self.is_password_visible:
            self.p_field_inspect.configure(show="*")
            self.reveal_btn.configure(text=self.get_text("reveal"))
        else:
            self.p_field_inspect.configure(show="")
            self.reveal_btn.configure(text=self.get_text("hide"))
        self.is_password_visible = not self.is_password_visible

    def copy_to_clipboard(self, text_val):
        self.clipboard_clear()
        self.clipboard_append(text_val)
        self.after(30000, self.wipe_system_clipboard, text_val)

    def wipe_system_clipboard(self, original_text):
        try:
            if self.clipboard_get() == original_text:
                self.clipboard_clear()
                self.clipboard_append("")
        except: pass

    # --- Vault Insertion/Mutation Window Module (Add & Edit Data) ---
    def spawn_entry_modal(self, service_name=None):
        self.register_user_activity()
        modal = ctk.CTkToplevel(self)
        modal.title(self.get_text("add_entry") if not service_name else self.get_text("edit_btn"))
        modal.geometry("450x620")
        modal.resizable(False, False)
        modal.attributes("-topmost", True)
        
        align = "w" if self.config["language"] == "English" else "e"
        padx_val = (40, 40)
        
        is_edit = service_name is not None
        default_data = self.vault_data["entries"].get(service_name, {}) if is_edit else {}
        
        ctk.CTkLabel(modal, text=self.get_text("service_name"), font=ctk.CTkFont(size=12)).pack(anchor=align, padx=padx_val, pady=(15, 2))
        s_in = ctk.CTkEntry(modal, width=370)
        s_in.insert(0, service_name if service_name else "")
        if self.config["language"] == "Farsi": s_in.configure(justify="right")
        if is_edit: s_in.configure(state="disabled") 
        s_in.pack(padx=padx_val, pady=(0, 8))
        
        ctk.CTkLabel(modal, text=self.get_text("category"), font=ctk.CTkFont(size=12)).pack(anchor=align, padx=padx_val, pady=(2, 2))
        
        bidi_categories = [self.bidi_format(c) for c in CATEGORIES]
        cat_in = ctk.CTkOptionMenu(modal, values=bidi_categories, width=370)
        cat_in.set(self.bidi_format(default_data.get("category", "Login")))
        cat_in.pack(padx=padx_val, pady=(0, 8))
        
        ctk.CTkLabel(modal, text=self.get_text("username"), font=ctk.CTkFont(size=12)).pack(anchor=align, padx=padx_val, pady=(2, 2))
        u_in = ctk.CTkEntry(modal, width=370)
        u_in.insert(0, default_data.get("username", ""))
        if self.config["language"] == "Farsi": u_in.configure(justify="right")
        u_in.pack(padx=padx_val, pady=(0, 8))
        
        ctk.CTkLabel(modal, text=self.get_text("password"), font=ctk.CTkFont(size=12)).pack(anchor=align, padx=padx_val, pady=(2, 2))
        p_frame = ctk.CTkFrame(modal, fg_color="transparent")
        p_frame.pack(padx=padx_val, fill="x", pady=(0, 4))
        p_in = ctk.CTkEntry(p_frame, width=330)
        p_in.insert(0, default_data.get("password", ""))
        p_in.pack(side="left")
        
        def inject_generated_string():
            pool = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.<>?"
            generated_str = "".join(secrets.choice(pool) for _ in range(32))
            p_in.delete(0, tk.END)
            p_in.insert(0, generated_str)
            update_modal_strength_indicator()
            
        gen_pop_btn = ctk.CTkButton(p_frame, text="⚡", width=30, command=inject_generated_string)
        gen_pop_btn.pack(side="right")
        
        m_strength_frame = ctk.CTkFrame(modal, fg_color="transparent")
        m_strength_frame.pack(padx=padx_val, fill="x", pady=(0, 10))
        m_meter = ctk.CTkProgressBar(m_strength_frame, width=200)
        m_meter.set(0.0)
        m_meter.pack(side="left", pady=6)
        m_lbl = ctk.CTkLabel(m_strength_frame, text="", font=ctk.CTkFont(size=11, weight="bold"))
        m_lbl.pack(side="left", padx=10)
        
        def update_modal_strength_indicator(*args):
            v, s, col = check_password_strength(p_in.get())
            m_meter.configure(progress_color=col)
            m_meter.set(v)
            m_lbl.configure(text=self.get_text("str_" + s.lower()), text_color=col)
            
        p_in.bind("<KeyRelease>", update_modal_strength_indicator)
        update_modal_strength_indicator()
        
        ctk.CTkLabel(modal, text=self.get_text("additional_info"), font=ctk.CTkFont(size=12)).pack(anchor=align, padx=padx_val, pady=(2, 2))
        i_in = ctk.CTkTextbox(modal, width=370, height=80)
        i_in.insert("1.0", default_data.get("info", ""))
        if self.config["language"] == "Farsi": i_in.tag_config("rtl", justify="right"); i_in.tag_add("rtl", "1.0", "end")
        i_in.pack(padx=padx_val, pady=(0, 20))
        
        def commit_record():
            svc = s_in.get().strip()
            if not svc: return
            if not is_edit:
                if svc in self.vault_data["entries"]: return
                if "service_order" not in self.vault_data: self.vault_data["service_order"] = []
                self.vault_data["service_order"].append(svc)
            
            selected_bidi_cat = cat_in.get()
            raw_cat_to_save = "Login"
            for raw_cat in CATEGORIES:
                if self.bidi_format(raw_cat) == selected_bidi_cat:
                    raw_cat_to_save = raw_cat
                    break

            self.vault_data["entries"][svc] = {
                "category": raw_cat_to_save, "username": u_in.get(), "password": p_in.get(),
                "info": i_in.get("1.0", "end-1c"), "favorite": default_data.get("favorite", False)
            }
            save_vault(self.vault_data, self.master_password, self.salt)
            self.render_records_list()
            modal.destroy()
            if self.selected_service == svc: self.inspect_record(svc)
            messagebox.showinfo(self.get_text("success"), self.get_text("saved_msg"))
            
        ctk.CTkButton(modal, text=self.get_text("save_btn"), font=ctk.CTkFont(weight="bold"), command=commit_record, width=370).pack(padx=padx_val)

    # --- System Settings Menu ---
    def show_settings_panel(self):
        self.register_user_activity()
        self.selected_service = None
        for w in self.workspace.winfo_children(): w.destroy()
        self.render_records_list()
        
        settings_scroll = ctk.CTkScrollableFrame(self.workspace, fg_color="transparent")
        settings_scroll.pack(expand=True, fill="both")
        
        align = "w" if self.config["language"] == "English" else "e"
        
       # ---- BUTTON ROW (Lock Vault & Change Password Side-by-Side) ----
        action_btn_frame = ctk.CTkFrame(settings_scroll, fg_color="transparent")
        action_btn_frame.pack(anchor=align, pady=(0, 15))
        
        ctk.CTkButton(action_btn_frame, text=self.get_text("lock_vault_btn"), 
                      fg_color="#ff4a4a", hover_color="#cc3b3b", 
                      command=self.lock_vault_session).pack(side="left" if align=="w" else "right", padx=(0, 10))
        
        ctk.CTkButton(action_btn_frame, text=self.get_text("change_pass_btn"), 
                      fg_color="#ff4a4a", hover_color="#cc3b3b", 
                      command=self.spawn_change_password_modal).pack(side="left" if align=="w" else "right")
        
  # ---- THEME SELECTOR ----
        ctk.CTkLabel(settings_scroll, text=self.get_text("theme"), font=ctk.CTkFont(size=12, weight="bold")).pack(anchor=align, pady=(5, 2))
        
        theme_menu = ctk.CTkOptionMenu(
            settings_scroll, 
            values=list(THEME_PRESETS.keys()), 
            command=self.apply_full_theme, 
            width=220
        )
        theme_menu.set(self.config.get("theme", "Dark"))
        theme_menu.pack(anchor=align, pady=(0, 12))

        # ---- MODERN COLOR THEME (Blue, Green, Dark-Blue) ----
        ctk.CTkLabel(settings_scroll, text=self.get_text("accent_theme"), font=ctk.CTkFont(size=12, weight="bold")).pack(anchor=align, pady=(5, 2))
        color_menu = ctk.CTkOptionMenu(settings_scroll, values=["blue", "green", "dark-blue"], command=self.update_color_theme_state, width=220)
        color_menu.set(self.config.get("color_theme", "blue"))
        color_menu.pack(anchor=align, pady=(0, 12))
        
        ctk.CTkLabel(settings_scroll, text=self.get_text("language"), font=ctk.CTkFont(size=12, weight="bold")).pack(anchor=align, pady=(5, 2))
        lang_menu = ctk.CTkOptionMenu(settings_scroll, values=["English", "Farsi"], command=self.update_language_state, width=220)
        lang_menu.set(self.config["language"])
        lang_menu.pack(anchor=align, pady=(0, 12))
        
        ctk.CTkLabel(settings_scroll, text=self.get_text("auto_lock_lbl"), font=ctk.CTkFont(size=12, weight="bold")).pack(anchor=align, pady=(5, 2))
        time_map = {self.get_text("time_disabled"): 0, self.get_text("time_1m"): 60, self.get_text("time_5m"): 300, self.get_text("time_15m"): 900, self.get_text("time_30m"): 1800}
        time_menu = ctk.CTkOptionMenu(settings_scroll, values=list(time_map.keys()), command=lambda k: self.update_inactivity_state(time_map[k]), width=220)
        curr_t_str = self.get_text("time_disabled")
        for k, v in time_map.items():
            if v == self.config["auto_lock_seconds"]: curr_t_str = k
        time_menu.set(curr_t_str)
        time_menu.pack(anchor=align, pady=(0, 12))
        
        tray_var = tk.BooleanVar(value=self.config["tray_minimize"])
        
        def toggle_tray():
            self.config["tray_minimize"] = tray_var.get()
            save_config(self.config)
        ctk.CTkCheckBox(settings_scroll, text=self.get_text("tray_lbl"), variable=tray_var, command=toggle_tray, font=ctk.CTkFont(size=12)).pack(anchor=align, pady=(5, 15))
        
        btn_frame = ctk.CTkFrame(settings_scroll, fg_color="transparent")
        btn_frame.pack(anchor=align, pady=(5, 15))
        ctk.CTkButton(btn_frame, text=self.get_text("backup_btn"), fg_color="#1f538d", command=self.execute_secure_vault_export).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_frame, text=self.get_text("import_btn"), fg_color="#916a08", hover_color="#735406", command=self.execute_secure_vault_import).pack(side="left")
        
        ctk.CTkFrame(settings_scroll, height=2, fg_color="gray30", width=480).pack(anchor=align, pady=10)
        
        ctk.CTkLabel(settings_scroll, text=self.get_text("about"), font=ctk.CTkFont(size=14, weight="bold"), text_color="gray").pack(anchor=align, pady=(5, 2))
        ctk.CTkLabel(settings_scroll, text="Noble Password Manager", font=ctk.CTkFont(size=13, weight="bold")).pack(anchor=align, pady=1)
        ctk.CTkLabel(settings_scroll, text=self.get_text("creator"), font=ctk.CTkFont(size=12)).pack(anchor=align, pady=1)
        ctk.CTkLabel(settings_scroll, text=self.get_text("version"), font=ctk.CTkFont(size=12), text_color="cyan").pack(anchor=align, pady=1)
        ctk.CTkLabel(settings_scroll, text=self.get_text("copyright"), font=ctk.CTkFont(size=11), text_color="gray").pack(anchor=align, pady=10)
        
    def spawn_change_password_modal(self):
        self.register_user_activity()
        
        modal = ctk.CTkToplevel(self)
        modal.title(self.get_text("change_pass_title"))
        modal.geometry("450x450")
        modal.resizable(False, False)
        
        # --- FIX: Set Modal Window Icon safely ---
        if hasattr(self, 'icon_path') and os.path.exists(self.icon_path):
            def set_modal_icon():
                try:
                    # Windows native .ico loader
                    modal.iconbitmap(self.icon_path)
                except Exception:
                    # Fallback for PNG/JPG formats across platforms
                    try:
                        from PIL import Image, ImageTk
                        # Store image on the modal instance to prevent garbage collection
                        modal._icon_ref = ImageTk.PhotoImage(Image.open(self.icon_path))
                        modal.iconphoto(False, modal._icon_ref)
                    except Exception as e:
                        print(f"Could not load modal icon: {e}")

            # 200ms delay gives Windows enough time to draw the window handle
            modal.after(200, set_modal_icon)
            
        modal.attributes("-topmost", True)
        modal.grab_set()
        modal.attributes("-topmost", True)
        modal.grab_set()  # Blocks interaction with the main window until closed
        
        align = "w" if self.config["language"] == "English" else "e"
        padx_val = (40, 40)
        
        # Warning Label
        warn_lbl = ctk.CTkLabel(modal, text=self.get_text("change_pass_warn"), 
                                text_color="#ff4a4a", font=ctk.CTkFont(size=12, weight="bold"), 
                                wraplength=370, justify="left" if align=="w" else "right")
        warn_lbl.pack(padx=padx_val, pady=(20, 15))

        # Current Password
        ctk.CTkLabel(modal, text=self.get_text("current_pass"), font=ctk.CTkFont(size=12)).pack(anchor=align, padx=padx_val, pady=(5, 2))
        current_entry = ctk.CTkEntry(modal, width=370, show="*")
        if self.config["language"] == "Farsi": current_entry.configure(justify="right")
        current_entry.pack(padx=padx_val, pady=(0, 10))

        # New Password
        ctk.CTkLabel(modal, text=self.get_text("new_pass"), font=ctk.CTkFont(size=12)).pack(anchor=align, padx=padx_val, pady=(5, 2))
        new_entry = ctk.CTkEntry(modal, width=370, show="*")
        if self.config["language"] == "Farsi": new_entry.configure(justify="right")
        new_entry.pack(padx=padx_val, pady=(0, 10))

        # Confirm New Password
        ctk.CTkLabel(modal, text=self.get_text("confirm_pass"), font=ctk.CTkFont(size=12)).pack(anchor=align, padx=padx_val, pady=(5, 2))
        confirm_entry = ctk.CTkEntry(modal, width=370, show="*")
        if self.config["language"] == "Farsi": confirm_entry.configure(justify="right")
        confirm_entry.pack(padx=padx_val, pady=(0, 20))

        # Save Button Logic
        def process_password_change():
            curr = current_entry.get()
            new_p = new_entry.get()
            conf_p = confirm_entry.get()

            if curr != self.master_password:
                messagebox.showerror(self.get_text("error"), self.get_text("wrong_pass"))
                return
            if new_p != conf_p:
                messagebox.showerror(self.get_text("error"), self.get_text("pass_mismatch"))
                return
            if not new_p:
                return

            # Re-encrypt vault with new password and new salt
            self.master_password = new_p
            self.salt = os.urandom(16)
            save_vault(self.vault_data, self.master_password, self.salt)

            messagebox.showinfo(self.get_text("success"), self.get_text("pass_changed_success"))
            modal.destroy()

        ctk.CTkButton(modal, text=self.get_text("change_pass_btn"), 
                      fg_color="#ff4a4a", hover_color="#cc3b3b", font=ctk.CTkFont(weight="bold"), 
                      command=process_password_change, width=370).pack(padx=padx_val)
        
        
    def update_theme_state(self, chosen_theme: str):
        self.config["theme"] = chosen_theme
        ctk.set_appearance_mode(chosen_theme)
        save_config(self.config)
        
    def update_color_theme_state(self, chosen_color: str):
        self.config["color_theme"] = chosen_color
        save_config(self.config)
        ctk.set_default_color_theme(chosen_color)
        messagebox.showinfo(self.get_text("success"), self.get_text("restart_warn"))
        
    def update_language_state(self, chosen_lang: str):
        self.config["language"] = chosen_lang
        save_config(self.config)
        self.show_dashboard()
        self.show_settings_panel()

    def update_inactivity_state(self, seconds_val: int):
        self.config["auto_lock_seconds"] = seconds_val
        save_config(self.config)

    def execute_secure_vault_export(self):
        self.register_user_activity()
        if not os.path.exists(VAULT_FILE): return
        dest = filedialog.asksaveasfilename(defaultextension=".enc", filetypes=[("Encrypted Vault Backup", "*.enc")], initialfile="noble_backup.enc", title=self.get_text("backup_btn"))
        if dest:
            try:
                with open(VAULT_FILE, 'rb') as source, open(dest, 'wb') as destination: destination.write(source.read())
                messagebox.showinfo(self.get_text("success"), self.get_text("backup_success"))
            except Exception as e: messagebox.showerror(self.get_text("error"), str(e))

    def execute_secure_vault_import(self):
        self.register_user_activity()
        target = filedialog.askopenfilename(filetypes=[("Encrypted Vault Backup", "*.enc")], title=self.get_text("import_btn"))
        if target:
            if messagebox.askyesno(self.get_text("import_btn"), self.get_text("import_warn")):
                try:
                    shutil.copy(target, VAULT_FILE)
                    self.lock_vault_session() 
                except Exception as e:
                    messagebox.showerror(self.get_text("error"), str(e))

if __name__ == "__main__":
    app = NoblePasswordManager()
    app.deiconify()
    app.mainloop()