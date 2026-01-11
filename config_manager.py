"""
config_manager.py - Configuration Manager without ENV files
"""

import os
from SETUP_CONFIG.crypto_vault import get_config, update_config

class ConfigManager:
    """Central configuration manager"""
    
    @staticmethod
    def get_bot_token():
        """Get bot token from encrypted vault"""
        token = get_config("bot_token")
        if not token:
            raise ValueError("Bot token not found! Run setup.py first")
        return token
    
    @staticmethod
    def get_admin_ids():
        """Get admin IDs"""
        return get_config("admin_ids", [])
    
    @staticmethod
    def is_admin(user_id):
        """Check if user is admin"""
        admins = ConfigManager.get_admin_ids()
        return user_id in admins
    
    @staticmethod
    def get_bot_settings():
        """Get bot settings"""
        return get_config("bot_settings", {})
    
    @staticmethod
    def get_feature_status(feature_name):
        """Check if feature is enabled"""
        features = get_config("features", {})
        return features.get(feature_name, False)
    
    @staticmethod
    def get_cloudinary_config():
        """Get Cloudinary configuration"""
        return get_config("cloudinary", {})
    
    @staticmethod
    def enable_feature(feature_name):
        """Enable a feature"""
        return update_config(f"features.{feature_name}", True)
    
    @staticmethod
    def disable_feature(feature_name):
        """Disable a feature"""
        return update_config(f"features.{feature_name}", False)
    
    @staticmethod
    def add_admin(admin_id):
        """Add new admin"""
        admins = ConfigManager.get_admin_ids()
        if admin_id not in admins:
            admins.append(admin_id)
            return update_config("admin_ids", admins)
        return True
    
    @staticmethod
    def remove_admin(admin_id):
        """Remove admin"""
        admins = ConfigManager.get_admin_ids()
        if admin_id in admins:
            admins.remove(admin_id)
            return update_config("admin_ids", admins)
        return True
    
    @staticmethod
    def get_database_path():
        """Get database path"""
        return "DATA_STORAGE/bot.db"
    
    @staticmethod
    def get_log_path():
        """Get log file path"""
        return "DATA_STORAGE/bot.log"
    
    @staticmethod
    def update_setting(key, value):
        """Update any setting"""
        return update_config(key, value)

# Global config instance
config = ConfigManager()
