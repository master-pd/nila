"""
MASTER_REGISTRIES/features/FEATURE_REGISTRY.py
⚠️ শুধু এই ফাইলে ফিচার অ্যাড করলেই system auto create করবে
"""

FEATURES = {
    "welcome_pro": {
        "enabled": True,
        "description": "Professional welcome with admin links",
        "version": "2.0.0",
        "category": "essential",
        "dependencies": ["image_generator"],
        "admin_configurable": True,
        "settings": {
            "inbox_first": True,
            "generate_image": True,
            "show_user_info": True,
            "allow_admin_links": True
        }
    },
    
    "rules_system": {
        "enabled": True,
        "description": "Group rules creation & management",
        "version": "1.0.0",
        "category": "moderation",
        "dependencies": ["database"],
        "admin_configurable": True,
        "settings": {
            "max_rules": 20,
            "allow_formatting": True,
            "auto_enforce": False
        }
    },
    
    "image_generator": {
        "enabled": True,
        "description": "Generate professional images and stickers",
        "version": "1.5.0",
        "category": "media",
        "dependencies": [],
        "admin_configurable": True,
        "settings": {
            "cloudinary_enabled": True,
            "default_template": "modern",
            "max_image_size": 5000
        }
    },
    
    "sticker_maker": {
        "enabled": True,
        "description": "Create stickers from images",
        "version": "1.2.0",
        "category": "media",
        "dependencies": ["image_generator"],
        "admin_configurable": False,
        "settings": {
            "auto_crop": True,
            "add_border": True,
            "max_size": 512
        }
    },
    
    "live_stream": {
        "enabled": True,
        "description": "Live streaming with YouTube integration",
        "version": "1.5.0",
        "category": "entertainment",
        "dependencies": [],
        "admin_configurable": True,
        "settings": {
            "max_quality": "1080p",
            "default_source": "youtube",
            "allow_random": True
        }
    },
    
    "admin_controls": {
        "enabled": True,
        "description": "Admin control panel and management",
        "version": "3.0.0",
        "category": "admin",
        "dependencies": ["database"],
        "admin_configurable": False,
        "settings": {
            "can_manage_users": True,
            "can_manage_rules": True,
            "can_manage_features": True
        }
    }
}

# 🔽🔽🔽 NEW FEATURE ADD HERE 🔽🔽🔽
# Example: Music player add করতে
# "music_player": {
#     "enabled": True,
#     "description": "Music streaming bot",
#     "version": "1.0.0",
#     "category": "entertainment",
#     "dependencies": ["youtube_dl"],
#     "admin_configurable": True,
#     "settings": {
#         "max_queue": 10,
#         "default_volume": 80
#     }
# }

def get_all_features():
    """Return all features from registry"""
    return list(FEATURES.keys())

def get_enabled_features():
    """Return only enabled features"""
    return [name for name, config in FEATURES.items() if config["enabled"]]

def get_feature_config(feature_name):
    """Get configuration for specific feature"""
    return FEATURES.get(feature_name, {})

def is_feature_enabled(feature_name):
    """Check if a feature is enabled"""
    config = FEATURES.get(feature_name, {})
    return config.get("enabled", False)
