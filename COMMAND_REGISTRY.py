"""
MASTER_REGISTRIES/commands/COMMAND_REGISTRY.py
⚠️ শুধু এই ফাইলে কমান্ড অ্যাড করলেই system auto create করবে
"""

COMMANDS = {
    "start": {
        "enabled": True,
        "description": "Start the bot and show welcome",
        "aliases": ["hello", "menu", "bot"],
        "admin_only": False,
        "group_only": False,
        "cooldown": 0,
        "category": "general",
        "feature_dependency": None
    },
    
    "help": {
        "enabled": True,
        "description": "Show all available commands",
        "aliases": ["commands", "menu", "info"],
        "admin_only": False,
        "group_only": False,
        "cooldown": 5,
        "category": "general",
        "feature_dependency": None
    },
    
    "rules": {
        "enabled": True,
        "description": "Group rules management system",
        "aliases": ["rule", "grouprules", "নিয়ম"],
        "admin_only": False,
        "group_only": True,
        "cooldown": 3,
        "category": "moderation",
        "feature_dependency": "rules_system"
    },
    
    "admin": {
        "enabled": True,
        "description": "Admin control panel",
        "aliases": ["control", "settings", "এডমিন"],
        "admin_only": True,
        "group_only": False,
        "cooldown": 2,
        "category": "admin",
        "feature_dependency": "admin_controls"
    },
    
    "welcome": {
        "enabled": True,
        "description": "Welcome message configuration",
        "aliases": ["ওয়েলকাম", "greet", "স্বাগতম"],
        "admin_only": True,
        "group_only": True,
        "cooldown": 5,
        "category": "admin",
        "feature_dependency": "welcome_pro"
    },
    
    "image": {
        "enabled": True,
        "description": "Generate professional images",
        "aliases": ["img", "photo", "ছবি"],
        "admin_only": False,
        "group_only": False,
        "cooldown": 10,
        "category": "media",
        "feature_dependency": "image_generator"
    },
    
    "sticker": {
        "enabled": True,
        "description": "Create sticker from image",
        "aliases": ["stiker", "স্টিকার"],
        "admin_only": False,
        "group_only": False,
        "cooldown": 5,
        "category": "media",
        "feature_dependency": "sticker_maker"
    },
    
    "live": {
        "enabled": True,
        "description": "Live streaming system",
        "aliases": ["stream", "লাইভ"],
        "admin_only": True,
        "group_only": True,
        "cooldown": 30,
        "category": "entertainment",
        "feature_dependency": "live_stream"
    }
}

# 🔽🔽🔽 NEW COMMAND ADD HERE 🔽🔽🔽
# Example: Music command add করতে
# "music": {
#     "enabled": True,
#     "description": "Play music in voice chat",
#     "aliases": ["song", "play", "গান"],
#     "admin_only": False,
#     "group_only": True,
#     "cooldown": 10,
#     "category": "entertainment",
#     "feature_dependency": "music_player"
# }

def get_all_commands():
    """Return all commands from registry"""
    return list(COMMANDS.keys())

def get_enabled_commands():
    """Return only enabled commands"""
    return [name for name, config in COMMANDS.items() if config["enabled"]]

def get_command_config(command_name):
    """Get configuration for specific command"""
    return COMMANDS.get(command_name, {})

def is_command_enabled(command_name):
    """Check if a command is enabled"""
    config = COMMANDS.get(command_name, {})
    return config.get("enabled", False)

def get_commands_by_category(category):
    """Get all commands in a category"""
    return [name for name, config in COMMANDS.items() 
            if config.get("category") == category and config.get("enabled", False)]

def get_commands_by_feature(feature_name):
    """Get commands that depend on a feature"""
    return [name for name, config in COMMANDS.items() 
            if config.get("feature_dependency") == feature_name and config.get("enabled", False)]
