"""
AUTO COMMAND SYSTEM
Dynamic command creation without editing files
"""

import os
import json
import inspect
from pathlib import Path
from typing import Dict, List, Any, Callable
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

class AutoCommandSystem:
    """Auto-command creation and management"""
    
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.commands_dir = Path(__file__).parent / "commands"
        self.commands_file = self.commands_dir / "command_list.json"
        self.loaded_commands = {}
        
        # Create directories
        self.commands_dir.mkdir(exist_ok=True)
        
        # Load existing commands
        self._load_commands()
    
    def _load_commands(self):
        """Load commands from file"""
        if self.commands_file.exists():
            with open(self.commands_file, 'r') as f:
                self.commands_data = json.load(f)
        else:
            self.commands_data = {
                "commands": {},
                "auto_responses": {},
                "aliases": {}
            }
    
    def _save_commands(self):
        """Save commands to file"""
        with open(self.commands_file, 'w') as f:
            json.dump(self.commands_data, f, indent=2)
    
    def create_command(self, 
                      command_name: str,
                      description: str,
                      handler: Callable,
                      aliases: List[str] = None,
                      admin_only: bool = False,
                      group_only: bool = False,
                      cooldown: int = 0):
        """
        Create a new command dynamically
        
        Args:
            command_name: Command name (without /)
            description: Command description
            handler: Function to handle command
            aliases: List of aliases
            admin_only: Only admins can use
            group_only: Only works in groups
            cooldown: Cooldown in seconds
        """
        # Register command
        self.app.add_handler(CommandHandler(command_name, handler))
        
        # Add aliases
        if aliases:
            for alias in aliases:
                self.app.add_handler(CommandHandler(alias, handler))
        
        # Save to file
        self.commands_data["commands"][command_name] = {
            "description": description,
            "aliases": aliases or [],
            "admin_only": admin_only,
            "group_only": group_only,
            "cooldown": cooldown,
            "created": inspect.getsource(handler)[:200]  # Store code snippet
        }
        
        # Save aliases mapping
        if aliases:
            for alias in aliases:
                self.commands_data["aliases"][alias] = command_name
        
        self._save_commands()
        
        print(f"✅ Command created: /{command_name}")
    
    def create_auto_response(self,
                           trigger: str,
                           response: str,
                           response_type: str = "text",
                           file_path: str = None,
                           case_sensitive: bool = False):
        """
        Create auto-response
        
        Args:
            trigger: Text that triggers response
            response: Response text or file
            response_type: text, photo, video, audio, voice
            file_path: Path to file (if not text)
            case_sensitive: Whether to match case
        """
        self.commands_data["auto_responses"][trigger] = {
            "response": response,
            "type": response_type,
            "file_path": file_path,
            "case_sensitive": case_sensitive
        }
        
        self._save_commands()
        
        # Register handler
        async def response_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            message = update.message.text
            
            # Check case sensitivity
            if case_sensitive:
                match = message == trigger
            else:
                match = message.lower() == trigger.lower()
            
            if match:
                if response_type == "text":
                    await update.message.reply_text(response)
                elif response_type == "photo" and file_path:
                    await update.message.reply_photo(photo=open(file_path, 'rb'))
                elif response_type == "video" and file_path:
                    await update.message.reply_video(video=open(file_path, 'rb'))
                elif response_type == "audio" and file_path:
                    await update.message.reply_audio(audio=open(file_path, 'rb'))
                elif response_type == "voice" and file_path:
                    await update.message.reply_voice(voice=open(file_path, 'rb'))
        
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, response_handler))
        
        print(f"✅ Auto-response created: '{trigger}' -> {response_type}")
    
    def get_all_commands(self) -> Dict:
        """Get all registered commands"""
        return self.commands_data
    
    def delete_command(self, command_name: str):
        """Delete a command"""
        if command_name in self.commands_data["commands"]:
            del self.commands_data["commands"][command_name]
            
            # Remove aliases
            aliases_to_remove = []
            for alias, cmd in self.commands_data["aliases"].items():
                if cmd == command_name:
                    aliases_to_remove.append(alias)
            
            for alias in aliases_to_remove:
                del self.commands_data["aliases"][alias]
            
            self._save_commands()
            print(f"✅ Command deleted: /{command_name}")
        else:
            print(f"❌ Command not found: /{command_name}")
    
    def generate_help_text(self) -> str:
        """Generate help text from commands"""
        help_text = "🤖 *Available Commands:*\n\n"
        
        for cmd, data in self.commands_data["commands"].items():
            help_text += f"• /{cmd}"
            if data["aliases"]:
                help_text += f" (aliases: {', '.join(data['aliases'])})"
            help_text += f" - {data['description']}\n"
            
            if data["admin_only"]:
                help_text += "  👑 *Admin only*\n"
            if data["group_only"]:
                help_text += "  👥 *Group only*\n"
            if data["cooldown"] > 0:
                help_text += f"  ⏱️ *Cooldown: {data['cooldown']}s*\n"
            
            help_text += "\n"
        
        # Add auto-responses section
        if self.commands_data["auto_responses"]:
            help_text += "\n🔤 *Auto-Responses:*\n\n"
            for trigger, data in self.commands_data["auto_responses"].items():
                help_text += f"• '{trigger}' -> {data['type']}\n"
        
        return help_text

# Example command creators
def create_default_commands(app, config, auto_cmd):
    """Create default commands for Nila Bot"""
    
    # Start command
    async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from stylish_text import StylishText
        
        bot_name = config.get("bot_name", "Nila Bot")
        styled_name = StylishText.generate(bot_name, "bold")
        
        welcome = f"""
{styled_name} 🤖

✨ *Welcome to {bot_name}!* ✨

I'm an advanced Telegram bot with:
🎭 Stylish text generation
🔧 Dynamic commands
🎨 Auto-responses
🛡️ Security features
🎬 Media tools

Use /help to see all commands!
Use /admin to access admin panel.
        """
        
        await update.message.reply_text(welcome, parse_mode='Markdown')
    
    auto_cmd.create_command(
        command_name="start",
        description="Start the bot",
        handler=start_command
    )
    
    # Help command
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = auto_cmd.generate_help_text()
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    auto_cmd.create_command(
        command_name="help",
        description="Show help message",
        handler=help_command
    )
    
    # Stylish text command
    async def style_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        from stylish_text import StylishText
        
        if not context.args:
            # Show style options
            styles = StylishText.get_all_styles()
            style_list = "\n".join([f"• {s}" for s in styles])
            
            await update.message.reply_text(
                f"🎨 *Available Styles:*\n\n{style_list}\n\n"
                f"Usage: /style <text> [style_name]\n"
                f"Example: /style Hello bold",
                parse_mode='Markdown'
            )
            return
        
        text = " ".join(context.args)
        style = "random"
        
        # Check if last arg is a style name
        if context.args[-1] in StylishText.get_all_styles():
            style = context.args[-1]
            text = " ".join(context.args[:-1])
        
        styled = StylishText.generate(text, style)
        await update.message.reply_text(styled)
    
    auto_cmd.create_command(
        command_name="style",
        description="Convert text to stylish format",
        handler=style_command,
        aliases=["stylish", "font"]
    )
    
    # Admin command
    async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        owner_id = config.get_owner_id()
        
        if user_id != owner_id:
            await update.message.reply_text("🚫 Access denied!")
            return
        
        # Admin panel
        admin_menu = """
🔧 *Admin Panel*

Commands:
• /admin_stats - Bot statistics
• /admin_users - User management
• /admin_backup - Backup data
• /admin_restart - Restart bot
• /admin_update - Update bot

Settings:
• /config_view - View config
• /config_set - Set config value
• /config_reset - Reset config
        """
        
        await update.message.reply_text(admin_menu, parse_mode='Markdown')
    
    auto_cmd.create_command(
        command_name="admin",
        description="Admin panel",
        handler=admin_command,
        admin_only=True
    )
    
    # Ping command
    async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        import time
        start_time = time.time()
        msg = await update.message.reply_text("🏓 Pong!")
        end_time = time.time()
        
        latency = round((end_time - start_time) * 1000, 2)
        await msg.edit_text(f"🏓 Pong! Latency: {latency}ms")
    
    auto_cmd.create_command(
        command_name="ping",
        description="Check bot latency",
        handler=ping_command
    )
    
    # Create some auto-responses
    auto_cmd.create_auto_response(
        trigger="hello",
        response="Hello there! 👋",
        response_type="text"
    )
    
    auto_cmd.create_auto_response(
        trigger="good morning",
        response="Good morning! ☀️",
        response_type="text"
    )
    
    auto_cmd.create_auto_response(
        trigger="good night",
        response="Good night! 🌙",
        response_type="text"
    )
    
    print("✅ Default commands created")
