"""
TERMUX HELPER
Termux-specific utilities and optimizations
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
import json

class TermuxHelper:
    """Helper functions for Termux environment"""
    
    @staticmethod
    def is_termux() -> bool:
        """Check if running in Termux"""
        return "termux" in os.environ.get("PREFIX", "")
    
    @staticmethod
    def get_termux_info() -> dict:
        """Get Termux environment information"""
        info = {
            "is_termux": TermuxHelper.is_termux(),
            "android_version": None,
            "termux_version": None,
            "architecture": platform.machine(),
            "python_version": platform.python_version(),
            "storage_access": False
        }
        
        if TermuxHelper.is_termux():
            try:
                # Try to get Android version
                if os.path.exists("/system/build.prop"):
                    with open("/system/build.prop", 'r') as f:
                        for line in f:
                            if line.startswith("ro.build.version.release="):
                                info["android_version"] = line.split("=")[1].strip()
                                break
                
                # Check storage access
                info["storage_access"] = os.path.exists("/sdcard")
                
                # Get Termux package version
                try:
                    result = subprocess.run(["termux-info"], 
                                          capture_output=True, 
                                          text=True, 
                                          shell=True)
                    info["termux_info"] = result.stdout[:500]
                except:
                    pass
                    
            except Exception:
                pass
        
        return info
    
    @staticmethod
    def setup_termux_storage():
        """Setup Termux storage access"""
        if not TermuxHelper.is_termux():
            return False
        
        try:
            # Check if storage is already setup
            if os.path.exists("/sdcard"):
                print("✅ Storage access already enabled")
                return True
            
            print("Setting up Termux storage...")
            subprocess.run(["termux-setup-storage"], shell=True)
            
            if os.path.exists("/sdcard"):
                print("✅ Storage access enabled")
                return True
            else:
                print("❌ Failed to enable storage access")
                return False
                
        except Exception as e:
            print(f"❌ Error setting up storage: {e}")
            return False
    
    @staticmethod
    def optimize_for_termux():
        """Optimize bot for Termux environment"""
        if not TermuxHelper.is_termux():
            return
        
        optimizations = []
        
        # 1. Reduce logging to save storage
        import logging
        logging.getLogger().setLevel(logging.WARNING)
        optimizations.append("Reduced logging level")
        
        # 2. Disable unnecessary features for low memory
        os.environ["PYTHONUNBUFFERED"] = "1"
        optimizations.append("Enabled unbuffered output")
        
        # 3. Use simpler JSON parser
        try:
            import ujson as json
            optimizations.append("Using ujson for faster JSON parsing")
        except:
            pass
        
        # 4. Create Termux shortcut
        TermuxHelper.create_termux_shortcut()
        
        return optimizations
    
    @staticmethod
    def create_termux_shortcut():
        """Create Termux desktop shortcut"""
        if not TermuxHelper.is_termux():
            return
        
        shortcut_dir = Path("/data/data/com.termux/files/home/.shortcuts")
        shortcut_dir.mkdir(exist_ok=True)
        
        # Create start script
        start_script = shortcut_dir / "Start_Nila_Bot.sh"
        
        script_content = """#!/data/data/com.termux/files/usr/bin/bash
echo "Starting Nila Bot..."
cd ~/NILA_BOT
python master.py
"""
        
        with open(start_script, 'w') as f:
            f.write(script_content)
        
        # Make executable
        os.chmod(start_script, 0o755)
        
        # Create stop script
        stop_script = shortcut_dir / "Stop_Nila_Bot.sh"
        
        stop_content = """#!/data/data/com.termux/files/usr/bin/bash
echo "Stopping Nila Bot..."
pkill -f "python master.py"
echo "Bot stopped!"
"""
        
        with open(stop_script, 'w') as f:
            f.write(stop_content)
        
        os.chmod(stop_script, 0o755)
        
        print("✅ Created Termux shortcuts in ~/.shortcuts/")
    
    @staticmethod
    def check_dependencies():
        """Check and install Termux dependencies"""
        if not TermuxHelper.is_termux():
            return
        
        dependencies = [
            "python", "python-pip", "git", "wget", "curl",
            "proot", "termux-api"
        ]
        
        missing = []
        
        for dep in dependencies:
            if shutil.which(dep) is None:
                missing.append(dep)
        
        if missing:
            print(f"Missing dependencies: {missing}")
            install = input("Install missing packages? (y/n): ")
            
            if install.lower() == 'y':
                try:
                    subprocess.run(["pkg", "install", "-y"] + missing, 
                                  check=True)
                    print("✅ Dependencies installed")
                except Exception as e:
                    print(f"❌ Failed to install: {e}")
        
        return missing
    
    @staticmethod
    def get_battery_info():
        """Get battery information (Termux only)"""
        if not TermuxHelper.is_termux():
            return None
        
        try:
            result = subprocess.run(["termux-battery-status"], 
                                  capture_output=True, 
                                  text=True, 
                                  shell=True)
            
            if result.returncode == 0:
                return json.loads(result.stdout)
        except:
            pass
        
        return None
    
    @staticmethod
    def send_notification(title: str, content: str):
        """Send notification (Termux only)"""
        if not TermuxHelper.is_termux():
            return False
        
        try:
            subprocess.run([
                "termux-notification",
                "--title", title,
                "--content", content
            ], shell=True)
            return True
        except:
            return False
    
    @staticmethod
    def setup_autostart():
        """Setup bot to start automatically in Termux"""
        if not TermuxHelper.is_termux():
            return False
        
        try:
            # Create boot script
            boot_script = Path("/data/data/com.termux/files/home/.termux/boot/")
            boot_script.mkdir(parents=True, exist_ok=True)
            
            autostart_script = boot_script / "start_nila_bot.sh"
            
            script_content = """#!/data/data/com.termux/files/usr/bin/bash
# Wait for network
sleep 10

# Start Nila Bot
cd ~/NILA_BOT
python master.py >> ~/nila_bot.log 2>&1 &
"""
            
            with open(autostart_script, 'w') as f:
                f.write(script_content)
            
            os.chmod(autostart_script, 0o755)
            
            print("✅ Autostart enabled")
            print("Bot will start automatically when Termux boots")
            return True
            
        except Exception as e:
            print(f"❌ Failed to setup autostart: {e}")
            return False

# Example usage
if __name__ == "__main__":
    helper = TermuxHelper()
    
    if helper.is_termux():
        print("📱 Running in Termux environment")
        
        info = helper.get_termux_info()
        print(f"Android: {info.get('android_version', 'Unknown')}")
        print(f"Arch: {info['architecture']}")
        
        # Setup storage
        helper.setup_termux_storage()
        
        # Optimize
        optimizations = helper.optimize_for_termux()
        print(f"Optimizations: {optimizations}")
        
        # Check battery
        battery = helper.get_battery_info()
        if battery:
            print(f"Battery: {battery.get('percentage', 0)}%")
        
        # Send test notification
        helper.send_notification("Nila Bot", "Bot is running in Termux!")
    else:
        print("💻 Running in regular environment")
