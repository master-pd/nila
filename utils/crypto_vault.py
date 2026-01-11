"""
CRYPTO VAULT
Advanced encryption for secure storage
"""

import os
import json
import base64
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import secrets

class CryptoVault:
    """Advanced cryptographic vault for secure storage"""
    
    def __init__(self, vault_name="nila_vault"):
        self.vault_dir = Path(__file__).parent.parent / "data" / "vaults"
        self.vault_file = self.vault_dir / f"{vault_name}.enc"
        self.key_file = self.vault_dir / f"{vault_name}.key"
        
        # Create vault directory
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize
        self._init_vault()
    
    def _init_vault(self):
        """Initialize or load vault"""
        if not self.key_file.exists():
            self._create_new_vault()
        else:
            self._load_vault_key()
    
    def _create_new_vault(self):
        """Create new encrypted vault"""
        # Generate master key
        master_key = secrets.token_bytes(32)
        
        # Generate salt
        salt = secrets.token_bytes(16)
        
        # Derive encryption key
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(master_key))
        
        # Save key and salt
        key_data = {
            "master_key": base64.b64encode(master_key).decode(),
            "salt": base64.b64encode(salt).decode()
        }
        
        with open(self.key_file, 'w') as f:
            json.dump(key_data, f)
        
        self.fernet = Fernet(key)
        
        # Create empty vault
        self._save_vault({})
    
    def _load_vault_key(self):
        """Load vault encryption key"""
        try:
            with open(self.key_file, 'r') as f:
                key_data = json.load(f)
            
            master_key = base64.b64decode(key_data["master_key"])
            salt = base64.b64decode(key_data["salt"])
            
            # Derive key
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(master_key))
            self.fernet = Fernet(key)
            
        except Exception as e:
            print(f"❌ Failed to load vault key: {e}")
            # Create new vault
            os.remove(self.key_file)
            self._create_new_vault()
    
    def _save_vault(self, data: dict):
        """Save data to encrypted vault"""
        encrypted = self.fernet.encrypt(json.dumps(data).encode())
        
        with open(self.vault_file, 'wb') as f:
            f.write(encrypted)
    
    def _load_vault(self) -> dict:
        """Load data from encrypted vault"""
        if not self.vault_file.exists():
            return {}
        
        try:
            with open(self.vault_file, 'rb') as f:
                encrypted = f.read()
            
            decrypted = self.fernet.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except:
            return {}
    
    def store(self, key: str, value):
        """Store value in vault"""
        data = self._load_vault()
        data[key] = value
        self._save_vault(data)
    
    def retrieve(self, key: str, default=None):
        """Retrieve value from vault"""
        data = self._load_vault()
        return data.get(key, default)
    
    def delete(self, key: str):
        """Delete value from vault"""
        data = self._load_vault()
        if key in data:
            del data[key]
            self._save_vault(data)
            return True
        return False
    
    def get_all(self) -> dict:
        """Get all data from vault"""
        return self._load_vault()
    
    def clear(self):
        """Clear all data from vault"""
        self._save_vault({})
    
    def backup(self, backup_path: str = None):
        """Create backup of vault"""
        if backup_path is None:
            backup_dir = self.vault_dir / "backups"
            backup_dir.mkdir(exist_ok=True)
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"vault_backup_{timestamp}.enc"
        
        # Copy vault file
        import shutil
        shutil.copy2(self.vault_file, backup_path)
        
        return str(backup_path)
    
    def restore(self, backup_path: str):
        """Restore vault from backup"""
        import shutil
        shutil.copy2(backup_path, self.vault_file)
        return True

# Global vault instance
vault = CryptoVault()
