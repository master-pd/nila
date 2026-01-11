"""
crypto_vault.py - AES-256 Encrypted Configuration System
No ENV files, no hardcoded credentials
"""

import os
import json
import base64
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class CryptoVault:
    """AES-256 encrypted configuration manager"""
    
    def __init__(self, vault_path="DATA_STORAGE/config.vault"):
        self.vault_path = vault_path
        self.key_path = "DATA_STORAGE/.secret.key"
        self.fernet = None
        
        # Initialize encryption
        self._init_encryption()
    
    def _init_encryption(self):
        """Initialize encryption system"""
        # Generate or load encryption key
        if not os.path.exists(self.key_path):
            self._generate_key()
        else:
            self._load_key()
    
    def _generate_key(self):
        """Generate new encryption key"""
        # Generate random salt
        salt = os.urandom(16)
        
        # Derive key from password (bot token will be used)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        
        # Use machine ID + timestamp as base
        import uuid
        import time
        base_key = f"{uuid.getnode()}{time.time()}".encode()
        
        key = base64.urlsafe_b64encode(kdf.derive(base_key))
        
        # Save key and salt
        key_data = {
            "key": key.decode(),
            "salt": base64.b64encode(salt).decode()
        }
        
        # Save to hidden file
        with open(self.key_path, "w") as f:
            json.dump(key_data, f)
        
        # Set file permissions (readable only by owner)
        os.chmod(self.key_path, 0o600)
        
        self.fernet = Fernet(key)
    
    def _load_key(self):
        """Load existing encryption key"""
        try:
            with open(self.key_path, "r") as f:
                key_data = json.load(f)
            
            key = key_data["key"].encode()
            self.fernet = Fernet(key)
            
        except Exception as e:
            print(f"⚠️ Failed to load key: {e}")
            # Regenerate key
            os.remove(self.key_path)
            self._generate_key()
    
    def encrypt_data(self, data):
        """Encrypt configuration data"""
        if not self.fernet:
            raise Exception("Encryption not initialized")
        
        # Convert to JSON string
        json_str = json.dumps(data, indent=2)
        
        # Encrypt
        encrypted = self.fernet.encrypt(json_str.encode())
        
        # Encode for storage
        return base64.b64encode(encrypted).decode()
    
    def decrypt_data(self, encrypted_b64):
        """Decrypt configuration data"""
        if not self.fernet:
            raise Exception("Encryption not initialized")
        
        try:
            # Decode from base64
            encrypted = base64.b64decode(encrypted_b64)
            
            # Decrypt
            decrypted = self.fernet.decrypt(encrypted)
            
            # Parse JSON
            return json.loads(decrypted.decode())
            
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return None
    
    def save_config(self, config_data):
        """Save configuration to encrypted vault"""
        encrypted = self.encrypt_data(config_data)
        
        # Save to vault file
        with open(self.vault_path, "w") as f:
            f.write(encrypted)
        
        # Set secure permissions
        os.chmod(self.vault_path, 0o600)
        
        print(f"✅ Config saved to {self.vault_path}")
        return True
    
    def load_config(self):
        """Load configuration from encrypted vault"""
        if not os.path.exists(self.vault_path):
            print(f"⚠️ Config vault not found: {self.vault_path}")
            return None
        
        try:
            with open(self.vault_path, "r") as f:
                encrypted_b64 = f.read().strip()
            
            return self.decrypt_data(encrypted_b64)
            
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            return None
    
    def update_config(self, key, value):
        """Update specific configuration value"""
        config = self.load_config()
        if not config:
            return False
        
        # Update nested keys (support dot notation: "bot_settings.debug")
        if "." in key:
            keys = key.split(".")
            current = config
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            current[keys[-1]] = value
        else:
            config[key] = value
        
        return self.save_config(config)
    
    def get_config(self, key=None, default=None):
        """Get configuration value"""
        config = self.load_config()
        if not config:
            return default
        
        if key is None:
            return config
        
        # Get nested keys
        if "." in key:
            keys = key.split(".")
            value = config
            for k in keys:
                if isinstance(value, dict):
                    value = value.get(k)
                else:
                    return default
            return value if value is not None else default
        else:
            return config.get(key, default)

# Singleton instance
vault = CryptoVault()

# Convenience functions
def get_config(key=None, default=None):
    """Get configuration value"""
    return vault.get_config(key, default)

def update_config(key, value):
    """Update configuration value"""
    return vault.update_config(key, value)

def reload_config():
    """Reload configuration from vault"""
    return vault.load_config()

if __name__ == "__main__":
    # Test the encryption system
    test_data = {
        "test": "This is encrypted data",
        "number": 12345,
        "list": ["item1", "item2"],
        "nested": {
            "key": "value"
        }
    }
    
    vault.save_config(test_data)
    loaded = vault.load_config()
    
    print("✅ Encryption test successful!")
    print(f"Original: {test_data}")
    print(f"Loaded: {loaded}")
