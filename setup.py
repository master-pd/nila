"""
setup.py - Interactive Setup Wizard
User শুধু এই ফাইলটি রান করবে
"""

import os
import sys
import subprocess
import getpass
from pathlib import Path
from datetime import datetime

# Color codes for beautiful interface
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Show beautiful banner"""
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}
╔══════════════════════════════════════════════════════╗
║                                                      ║
║      🚀 𝗡ɪʟᴀ♡ʚɞ ←●_0 𝗕𝗢𝗧 𝗦𝗘𝗧𝗨𝗣 𝗪𝗜𝗭𝗔𝗥𝗗          ║
║                                                      ║
║     Version: 6.0.0 | Professional Telegram Bot      ║
║     No ENV | No Hardcode | Auto Setup              ║
║                                                      ║
╚══════════════════════════════════════════════════════╗{Colors.END}
"""
    print(banner)

def check_python_version():
    """Check Python version compatibility"""
    if sys.version_info < (3, 8):
        print(f"{Colors.RED}❌ Python 3.8+ required!{Colors.END}")
        sys.exit(1)
    print(f"{Colors.GREEN}✅ Python {sys.version_info.major}.{sys.version_info.minor} detected{Colors.END}")

def install_dependencies():
    """Install required packages"""
    print(f"\n{Colors.CYAN}📦 Installing dependencies...{Colors.END}")
    
    requirements = [
        "python-telegram-bot==20.7",
        "Pillow==10.1.0",
        "cryptography==41.0.7",
        "python-dotenv==1.0.0",
        "sqlite3",
        "requests==2.31.0",
        "cloudinary==1.36.0",
        "yt-dlp==2023.10.13",
        "opencv-python==4.8.1.78",
        "numpy==1.24.3"
    ]
    
    try:
        # Create requirements.txt
        with open("requirements.txt", "w") as f:
            for req in requirements:
                f.write(req + "\n")
        
        # Install using pip
        print(f"{Colors.YELLOW}Installing packages...{Colors.END}")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        
        print(f"{Colors.GREEN}✅ All dependencies installed!{Colors.END}")
        return True
        
    except Exception as e:
        print(f"{Colors.RED}❌ Failed to install dependencies: {e}{Colors.END}")
        return False

def get_bot_token():
    """Get bot token from user"""
    print(f"\n{Colors.CYAN}🤖 BOT TOKEN SETUP{Colors.END}")
    print(f"{Colors.YELLOW}1. Go to @BotFather on Telegram")
    print(f"2. Create new bot with /newbot")
    print(f"3. Copy the bot token{Colors.END}")
    
    while True:
        token = getpass.getpass(f"\n{Colors.BLUE}Enter bot token (hidden): {Colors.END}")
        
        if len(token) < 10:
            print(f"{Colors.RED}❌ Invalid token! Try again.{Colors.END}")
            continue
            
        # Validate token format
        if ":" not in token:
            print(f"{Colors.RED}❌ Token must contain ':' character{Colors.END}")
            continue
            
        return token

def get_admin_id():
    """Get admin Telegram ID"""
    print(f"\n{Colors.CYAN}👑 ADMIN ID SETUP{Colors.END}")
    print(f"{Colors.YELLOW}1. Go to @userinfobot on Telegram")
    print(f"2. Send /start")
    print(f"3. Copy your Telegram ID{Colors.END}")
    
    while True:
        try:
            admin_id = input(f"\n{Colors.BLUE}Enter your Telegram ID: {Colors.END}")
            
            if not admin_id.isdigit():
                print(f"{Colors.RED}❌ ID must be numeric!{Colors.END}")
                continue
                
            return int(admin_id)
            
        except ValueError:
            print(f"{Colors.RED}❌ Enter valid number!{Colors.END}")

def setup_cloudinary():
    """Setup Cloudinary for media storage"""
    print(f"\n{Colors.CYAN}☁️ CLOUDINARY SETUP{Colors.END}")
    print(f"{Colors.YELLOW}1. Go to https://cloudinary.com")
    print(f"2. Sign up for free account")
    print(f"3. Get API credentials from dashboard{Colors.END}")
    
    use_cloudinary = input(f"\n{Colors.BLUE}Use Cloudinary for media storage? (y/n): {Colors.END}").lower()
    
    if use_cloudinary == 'y':
        cloud_name = input(f"{Colors.BLUE}Cloud Name: {Colors.END}")
        api_key = getpass.getpass(f"{Colors.BLUE}API Key (hidden): {Colors.END}")
        api_secret = getpass.getpass(f"{Colors.BLUE}API Secret (hidden): {Colors.END}")
        
        return {
            "use_cloudinary": True,
            "cloud_name": cloud_name,
            "api_key": api_key,
            "api_secret": api_secret
        }
    else:
        return {"use_cloudinary": False}

def generate_config(token, admin_id, cloudinary_config):
    """Generate encrypted config file"""
    from SETUP_CONFIG.crypto_vault import CryptoVault
    
    config_data = {
        "bot_token": token,
        "admin_ids": [admin_id],
        "bot_settings": {
            "name": "𝗡ɪʟᴀ♡ʚɞ ←●_0",
            "version": "6.0.0",
            "auto_setup": True,
            "debug_mode": False
        },
        "features": {
            "welcome_pro": True,
            "rules_system": True,
            "live_stream": True,
            "image_generator": True,
            "sticker_maker": True
        },
        "cloudinary": cloudinary_config,
        "setup_date": datetime.now().isoformat()
    }
    
    # Create data directory if not exists
    os.makedirs("DATA_STORAGE", exist_ok=True)
    
    # Encrypt and save config
    vault = CryptoVault()
    vault.save_config(config_data)
    
    print(f"{Colors.GREEN}✅ Encrypted config created: DATA_STORAGE/config.vault{Colors.END}")
    return True

def test_bot_connection(token):
    """Test connection to Telegram API"""
    import requests
    
    print(f"\n{Colors.CYAN}🔗 Testing bot connection...{Colors.END}")
    
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_name = data["result"]["first_name"]
                print(f"{Colors.GREEN}✅ Connected successfully!{Colors.END}")
                print(f"{Colors.BLUE}🤖 Bot Name: {bot_name}{Colors.END}")
                return True
    except Exception as e:
        print(f"{Colors.RED}❌ Connection failed: {e}{Colors.END}")
        return False

def create_project_structure():
    """Create all required folders and files"""
    folders = [
        "SETUP_CONFIG",
        "CORE_SYSTEM", 
        "MASTER_REGISTRIES/features",
        "MASTER_REGISTRIES/commands",
        "MASTER_REGISTRIES/admin",
        "MASTER_REGISTRIES/features/auto_features",
        "MASTER_REGISTRIES/commands/auto_commands", 
        "MASTER_REGISTRIES/admin/auto_admin",
        "MEDIA_TOOLS",
        "DATABASE/models",
        "UTILITIES",
        "DATA_STORAGE"
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"{Colors.GREEN}📁 Created: {folder}{Colors.END}")
    
    # Create __init__.py files
    for root, dirs, files in os.walk("."):
        if "__pycache__" not in root:
            init_file = os.path.join(root, "__init__.py")
            if not os.path.exists(init_file):
                with open(init_file, "w") as f:
                    f.write('"""Package initialization"""\n')
    
    print(f"{Colors.GREEN}✅ Project structure created!{Colors.END}")

def show_summary(token, admin_id):
    """Show setup summary"""
    clear_screen()
    print_banner()
    
    summary = f"""
{Colors.GREEN}{Colors.BOLD}🎉 SETUP COMPLETED SUCCESSFULLY!{Colors.END}

{Colors.CYAN}📋 SETUP SUMMARY:{Colors.END}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔹 {Colors.BLUE}Bot Name: {Colors.END}𝗡ɪʟᴀ♡ʚɞ ←●_0
🔹 {Colors.BLUE}Version: {Colors.END}6.0.0
🔹 {Colors.BLUE}Admin ID: {Colors.END}{admin_id}
🔹 {Colors.BLUE}Config File: {Colors.END}DATA_STORAGE/config.vault
🔹 {Colors.BLUE}Database: {Colors.END}DATA_STORAGE/bot.db

{Colors.CYAN}🚀 FEATURES ENABLED:{Colors.END}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Professional Welcome System
✅ Rules Management  
✅ Live Streaming
✅ Image Generator
✅ Sticker Maker
✅ Admin Controls
✅ Auto Setup System

{Colors.CYAN}📖 NEXT STEPS:{Colors.END}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. {Colors.GREEN}Start the bot:{Colors.END}
   {Colors.YELLOW}python master.py{Colors.END}

2. {Colors.GREEN}Add features:{Colors.END}
   Edit MASTER_REGISTRIES/features/FEATURE_REGISTRY.py

3. {Colors.GREEN}Add commands:{Colors.END}  
   Edit MASTER_REGISTRIES/commands/COMMAND_REGISTRY.py

4. {Colors.GREEN}Join group and use /admin{Colors.END}
   to configure the bot

{Colors.PURPLE}🔧 Support: @YourSupportChannel{Colors.END}
"""
    print(summary)

def main():
    """Main setup wizard"""
    clear_screen()
    print_banner()
    
    print(f"{Colors.YELLOW}🎯 Welcome to Nila Bot Pro Setup!{Colors.END}")
    print(f"{Colors.CYAN}This wizard will guide you through setup.{Colors.END}\n")
    
    input(f"{Colors.BLUE}Press Enter to continue...{Colors.END}")
    
    # Step 1: Check Python
    check_python_version()
    
    # Step 2: Create structure
    create_project_structure()
    
    # Step 3: Install dependencies
    if not install_dependencies():
        return
    
    # Step 4: Get bot token
    token = get_bot_token()
    
    # Step 5: Test connection
    if not test_bot_connection(token):
        retry = input(f"{Colors.RED}Connection failed! Retry? (y/n): {Colors.END}")
        if retry.lower() == 'y':
            token = get_bot_token()
            test_bot_connection(token)
    
    # Step 6: Get admin ID
    admin_id = get_admin_id()
    
    # Step 7: Cloudinary setup
    cloudinary_config = setup_cloudinary()
    
    # Step 8: Generate config
    generate_config(token, admin_id, cloudinary_config)
    
    # Step 9: Show summary
    show_summary(token, admin_id)
    
    # Step 10: Option to start bot
    start_now = input(f"\n{Colors.BLUE}Start bot now? (y/n): {Colors.END}")
    if start_now.lower() == 'y':
        print(f"{Colors.GREEN}🚀 Starting Nila Bot Pro...{Colors.END}")
        os.system("python master.py")

if __name__ == "__main__":
    main()
