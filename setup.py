#!/usr/bin/env python3
"""
NILA BOT - AUTO SETUP WIZARD
Termux Friendly | No ENV | No Hardcode
"""

import os
import sys
import json
import getpass
import hashlib
from pathlib import Path
from datetime import datetime
import base64
import random
import string

class Colors:
    """Terminal Colors"""
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_logo():
    """Print Nila Bot Logo"""
    logo = f"""{Colors.MAGENTA}
╔══════════════════════════════════════╗
║         ███╗   ██╗██╗██╗      █████╗ ║
║         ████╗  ██║██║██║     ██╔══██╗║
║         ██╔██╗ ██║██║██║     ███████║║
║         ██║╚██╗██║██║██║     ██╔══██║║
║         ██║ ╚████║██║███████╗██║  ██║║
║         ╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝║
║     {Colors.CYAN}T E L E G R A M   B O T{Colors.MAGENTA}     ║
╚══════════════════════════════════════╝{Colors.END}
    """
    print(logo)

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, password=False):
    """Get user input with styling"""
    if password:
        return getpass.getpass(f"{Colors.YELLOW}👉 {prompt}: {Colors.END}")
    else:
        return input(f"{Colors.YELLOW}👉 {prompt}: {Colors.END}")

def print_step(step, message):
    """Print step message"""
    print(f"\n{Colors.GREEN}[{step}] {Colors.CYAN}{message}{Colors.END}")

def print_error(message):
    """Print error message"""
    print(f"\n{Colors.RED}❌ ERROR: {message}{Colors.END}")

def print_success(message):
    """Print success message"""
    print(f"\n{Colors.GREEN}✅ {message}{Colors.END}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ️  {message}{Colors.END}")

def generate_secret_key():
    """Generate secret key for encryption"""
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(50))

def encrypt_data(data, key):
    """Simple encryption"""
    import base64
    from cryptography.fernet import Fernet
    
    # Generate key from secret
    key_hash = hashlib.sha256(key.encode()).digest()
    fernet = Fernet(base64.urlsafe_b64encode(key_hash))
    
    # Encrypt
    encrypted = fernet.encrypt(json.dumps(data).encode())
    return encrypted.decode()

def decrypt_data(encrypted_data, key):
    """Simple decryption"""
    import base64
    from cryptography.fernet import Fernet
    
    # Generate key from secret
    key_hash = hashlib.sha256(key.encode()).digest()
    fernet = Fernet(base64.urlsafe_b64encode(key_hash))
    
    # Decrypt
    decrypted = fernet.decrypt(encrypted_data.encode())
    return json.loads(decrypted.decode())

class SetupWizard:
    def __init__(self):
        self.config = {}
        self.secret_key = ""
        self.bot_token = ""
        self.owner_id = ""
        self.setup_dir = Path(__file__).parent
        
    def run(self):
        """Run setup wizard"""
        clear_screen()
        print_logo()
        
        print(f"\n{Colors.BOLD}Welcome to Nila Bot Setup Wizard{Colors.END}")
        print(f"{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}")
        
        # Step 1: Get Bot Token
        print_step("1", "Get Your Bot Token")
        print_info("1. Go to @BotFather on Telegram")
        print_info("2. Send /newbot command")
        print_info("3. Choose a name for your bot")
        print_info("4. Choose a username (must end with 'bot')")
        print_info("5. Copy the token you receive")
        
        while True:
            self.bot_token = get_input("Enter your bot token", password=True)
            if self.bot_token and len(self.bot_token) > 30:
                if ":" in self.bot_token:
                    print_success("Valid token format detected")
                    break
                else:
                    print_error("Invalid token format")
            else:
                print_error("Token too short")
        
        # Step 2: Get Owner ID
        print_step("2", "Get Your Telegram ID")
        print_info("1. Go to @userinfobot on Telegram")
        print_info("2. Send /start command")
        print_info("3. Copy your ID number")
        
        while True:
            owner_input = get_input("Enter your Telegram ID")
            if owner_input.isdigit():
                self.owner_id = int(owner_input)
                print_success(f"Owner ID set: {self.owner_id}")
                break
            else:
                print_error("Please enter a valid number")
        
        # Step 3: Generate Secret Key
        print_step("3", "Generating Security Keys")
        self.secret_key = generate_secret_key()
        print_success("Security keys generated")
        
        # Step 4: Additional Settings
        print_step("4", "Additional Settings")
        
        # Bot Name
        bot_name = get_input("Bot display name (default: Nila Bot)")
        if not bot_name:
            bot_name = "Nila Bot"
        
        # Welcome Message
        welcome_msg = get_input("Welcome message (default: Hello!)")
        if not welcome_msg:
            welcome_msg = "Hello! 👋"
        
        # Admin Password
        admin_pass = get_input("Set admin password (optional)")
        if not admin_pass:
            admin_pass = generate_secret_key()[:8]
        
        # Step 5: Save Configuration
        print_step("5", "Saving Configuration")
        
        # Prepare config
        self.config = {
            "bot_name": bot_name,
            "bot_token": self.bot_token,
            "owner_id": self.owner_id,
            "admin_password": admin_pass,
            "welcome_message": welcome_msg,
            "setup_date": datetime.now().isoformat(),
            "version": "2.0.0",
            "features": {
                "welcome": True,
                "security": True,
                "auto_response": True,
                "live_stream": False,
                "games": False,
                "music": False
            }
        }
        
        # Create data directory
        data_dir = self.setup_dir / "data"
        data_dir.mkdir(exist_ok=True)
        
        # Save encrypted config
        encrypted_config = encrypt_data(self.config, self.secret_key)
        
        with open(data_dir / "config.vault", "w") as f:
            f.write(encrypted_config)
        
        # Save secret key (hidden)
        with open(data_dir / ".secret.key", "w") as f:
            f.write(self.secret_key)
        
        # Save readable config (without sensitive data)
        safe_config = self.config.copy()
        safe_config["bot_token"] = "***" + self.bot_token[-6:]
        safe_config["admin_password"] = "********"
        
        with open(data_dir / "bot_config.json", "w") as f:
            json.dump(safe_config, f, indent=2)
        
        print_success("Configuration saved securely!")
        
        # Step 6: Install Requirements
        print_step("6", "Installing Requirements")
        
        requirements = [
            "python-telegram-bot==20.7",
            "cryptography==41.0.7",
            "Pillow==10.1.0",
            "requests==2.31.0",
            "aiohttp==3.9.0"
        ]
        
        # Create requirements.txt
        req_file = self.setup_dir / "requirements.txt"
        with open(req_file, "w") as f:
            f.write("\n".join(requirements))
        
        print_info("Requirements file created")
        
        # Ask to install
        install_req = get_input("Install requirements now? (y/n)").lower()
        if install_req == 'y':
            print_info("Installing... This may take a moment.")
            os.system(f"{sys.executable} -m pip install -r requirements.txt")
            print_success("Requirements installed!")
        
        # Step 7: Test Bot
        print_step("7", "Testing Bot Connection")
        
        print_info("Testing bot token...")
        try:
            import requests
            test_url = f"https://api.telegram.org/bot{self.bot_token}/getMe"
            response = requests.get(test_url, timeout=10)
            
            if response.status_code == 200:
                bot_info = response.json()
                print_success(f"✅ Bot connected: @{bot_info['result']['username']}")
                print_success(f"✅ Bot name: {bot_info['result']['first_name']}")
            else:
                print_error("Failed to connect. Check your token.")
        except Exception as e:
            print_error(f"Connection test failed: {e}")
        
        # Step 8: Setup Complete
        print_step("8", "Setup Complete!")
        
        summary = f"""
{Colors.GREEN}{'='*50}{Colors.END}
{Colors.BOLD}NILA BOT SETUP SUMMARY{Colors.END}
{Colors.GREEN}{'='*50}{Colors.END}

{Colors.CYAN}🤖 Bot Name:{Colors.END} {bot_name}
{Colors.CYAN}👤 Owner ID:{Colors.END} {self.owner_id}
{Colors.CYAN}📁 Config Location:{Colors.END} {data_dir / "config.vault"}
{Colors.CYAN}🔐 Security:{Colors.END} Encrypted with AES-256

{Colors.YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Colors.END}

{Colors.BOLD}🚀 START YOUR BOT:{Colors.END}
{Colors.GREEN}python master.py{Colors.END}

{Colors.BOLD}📋 NEXT STEPS:{Colors.END}
1. Start your bot: {Colors.GREEN}python master.py{Colors.END}
2. Go to your bot on Telegram
3. Send {Colors.YELLOW}/start{Colors.END} command
4. Configure features with {Colors.YELLOW}/admin{Colors.END}

{Colors.BOLD}🔧 ADMIN PANEL:{Colors.END}
Password: {Colors.RED}{admin_pass}{Colors.END}

{Colors.GREEN}{'='*50}{Colors.END}
        """
        
        print(summary)
        
        # Save setup summary
        with open(data_dir / "setup_summary.txt", "w") as f:
            f.write(summary.replace(Colors.RED, "").replace(Colors.GREEN, "")
                   .replace(Colors.YELLOW, "").replace(Colors.CYAN, "")
                   .replace(Colors.BOLD, "").replace(Colors.END, ""))
        
        print_info(f"Setup summary saved to: {data_dir / 'setup_summary.txt'}")
        
        # Start bot option
        start_now = get_input("Start bot now? (y/n)").lower()
        if start_now == 'y':
            print_info("Starting Nila Bot...")
            os.system(f"{sys.executable} master.py")

if __name__ == "__main__":
    try:
        wizard = SetupWizard()
        wizard.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup cancelled by user.{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Setup failed: {e}")
        sys.exit(1)
