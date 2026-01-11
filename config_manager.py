"""
CONFIG MANAGER
No ENV, No Hardcode - Auto Config Loader
"""

import json
import os
import hashlib
import base64
from pathlib import Path
from typing import Dict, Any, Optional
from cryptography.fernet import Fernet
from datetime import datetime

class ConfigManager:
    """Auto Configuration Manager"""
    
    _instance = None
    _config = None
    _secret_key = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.data_dir = Path(__file__).parent / "data"
            self._load_config()
    
    def _load_config(self):
        """Load encrypted configuration"""
        config_file = self.data_dir / "config.vault"
        secret_file = self.data_dir / ".secret.key"
        
        if not config_file.exists() or not secret_file.exists():
            print("⚠️  Configuration not found. Please run setup.py first.")
            return self._create_default_config()
        
        try:
            # Load secret key
            with open(secret_file, 'r') as f:
                self._secret_key = f.read().strip()
            
            # Load encrypted config
            with open(config_file, 'r') as f:
                encrypted_data = f.read()
            
            # Decrypt
            self._config = self._decrypt_data(encrypted_data)
            return True
            
        except Exception as e:
            print(f"❌ Error loading config: {e}")
            return self._create_default_config()
    
    def _create_default_config(self):
        """Create default configuration"""
        print("⚙️  Creating default configuration...")
        
        self._config = {
            "bot_name": "Nila Bot",
            "bot_token": "",
            "owner_id": 0,
            "admin_password": "admin123",
            "welcome_message": "Hello! 👋",
            "setup_date": datetime.now().isoformat(),
            "version": "2.0.0",
            "features": {
                "welcome": True,
                "security": True,
                "auto_response": True,
                "live_stream": False,
                "games": False,
                "music": False
            },
            "settings": {
                "log_level": "INFO",
                "max_file_size": 50,  # MB
                "auto_backup": True,
                "backup_interval": 24,  # hours
                "language": "en",
                "timezone": "UTC"
            }
        }
        
        self.data_dir.mkdir(exist_ok=True)
        self.save_config()
        return True
    
    def _encrypt_data(self, data: Dict) -> str:
        """Encrypt configuration data"""
        key_hash = hashlib.sha256(self._secret_key.encode()).digest()
        fernet = Fernet(base64.urlsafe_b64encode(key_hash))
        
        encrypted = fernet.encrypt(json.dumps(data).encode())
        return encrypted.decode()
    
    def _decrypt_data(self, encrypted_data: str) -> Dict:
        """Decrypt configuration data"""
        key_hash = hashlib.sha256(self._secret_key.encode()).digest()
        fernet = Fernet(base64.urlsafe_b64encode(key_hash))
        
        decrypted = fernet.decrypt(encrypted_data.encode())
        return json.loads(decrypted.decode())
    
    def save_config(self):
        """Save configuration to encrypted vault"""
        if not self._secret_key:
            # Generate new secret key
            import random
            import string
            chars = string.ascii_letters + string.digits + string.punctuation
            self._secret_key = ''.join(random.choice(chars) for _ in range(50))
            
            # Save secret key
            with open(self.data_dir / ".secret.key", 'w') as f:
                f.write(self._secret_key)
        
        # Encrypt and save
        encrypted = self._encrypt_data(self._config)
        
        with open(self.data_dir / "config.vault", 'w') as f:
            f.write(encrypted)
        
        # Also save readable version (without sensitive data)
        safe_config = self._config.copy()
        if "bot_token" in safe_config and safe_config["bot_token"]:
            safe_config["bot_token"] = "***" + safe_config["bot_token"][-6:]
        if "admin_password" in safe_config:
            safe_config["admin_password"] = "********"
        
        with open(self.data_dir / "bot_config.json", 'w') as f:
            json.dump(safe_config, f, indent=2)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self._config
        
        for i, k in enumerate(keys[:-1]):
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def update_feature(self, feature: str, enabled: bool):
        """Update feature status"""
        if "features" not in self._config:
            self._config["features"] = {}
        
        self._config["features"][feature] = enabled
        self.save_config()
    
    def get_bot_token(self) -> str:
        """Get bot token safely"""
        return self.get("bot_token", "")
    
    def get_owner_id(self) -> int:
        """Get owner ID"""
        return self.get("owner_id", 0)
    
    def get_all_config(self) -> Dict:
        """Get all configuration (safe version)"""
        safe_config = self._config.copy()
        
        # Hide sensitive data
        if "bot_token" in safe_config and safe_config["bot_token"]:
            safe_config["bot_token"] = "***" + safe_config["bot_token"][-6:]
        
        if "admin_password" in safe_config:
            safe_config["admin_password"] = "********"
        
        return safe_config
    
    def validate_config(self) -> bool:
        """Validate configuration"""
        token = self.get_bot_token()
        owner_id = self.get_owner_id()
        
        if not token or len(token) < 30:
            print("❌ Invalid bot token")
            return False
        
        if not owner_id or owner_id == 0:
            print("❌ Owner ID not set")
            return False
        
        return True

# Global instance
config = ConfigManager()
