"""
PROFESSIONAL WELCOME FEATURE
Advanced welcome messages with stylish text
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
import random
from datetime import datetime

class WelcomeProFeature:
    """Professional welcome system"""
    
    def __init__(self, app, config):
        self.app = app
        self.config = config
        
        # Welcome messages
        self.welcome_messages = [
            "✨ Welcome {name}! We're excited to have you here!",
            "🌟 Hello {name}! Enjoy your stay in our community!",
            "🎉 Welcome aboard {name}! Feel free to explore!",
            "👋 Hey {name}! Great to see you here!",
            "💫 Welcome {name}! Make yourself at home!",
            "🎊 Hello {name}! You're now part of our family!",
            "🔥 Welcome {name}! Let's make great memories!",
            "🌈 Hello {name}! You've just made this place brighter!"
        ]
        
        # Emoji sets
        self.emojis = {
            "stars": ["✨", "🌟", "⭐", "💫", "☄️"],
            "hearts": ["❤️", "🧡", "💛", "💚", "💙"],
            "objects": ["🎯", "🎮", "🎨", "🎪", "🎭"],
            "nature": ["🌸", "🌺", "🌹", "🌻", "🌼"]
        }
    
    def register(self):
        """Register welcome handler"""
        self.app.add_handler(
            MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.welcome_new_member)
        )
    
    async def welcome_new_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome new members"""
        for member in update.message.new_chat_members:
            if member.is_bot:
                continue
            
            # Prepare welcome message
            welcome_msg = self._prepare_welcome(member, update.effective_chat)
            
            # Send welcome
            await update.message.reply_text(
                welcome_msg,
                parse_mode='HTML',
                reply_markup=self._get_welcome_buttons(member)
            )
    
    def _prepare_welcome(self, user, chat):
        """Prepare welcome message"""
        # Get random welcome template
        template = random.choice(self.welcome_messages)
        
        # Format with user info
        name = user.first_name or user.username or "New Member"
        welcome_text = template.format(name=name)
        
        # Add stylish formatting
        from stylish_text import StylishText
        styled_name = StylishText.generate(name, random.choice(["bold", "italic", "bold_italic"]))
        welcome_text = welcome_text.replace(name, styled_name)
        
        # Add emoji decoration
        emoji_type = random.choice(list(self.emojis.keys()))
        emoji = random.choice(self.emojis[emoji_type])
        
        # Create final message
        final_msg = f"""
{emoji * 3}

{welcome_text}

📅 Joined: {datetime.now().strftime('%Y-%m-%d %H:%M')}
👤 ID: <code>{user.id}</code>
👥 Chat: {chat.title if hasattr(chat, 'title') else 'Private'}

{emoji * 3}

🎯 <i>Use /help to see available commands</i>
        """
        
        return final_msg
    
    def _get_welcome_buttons(self, user):
        """Create welcome buttons"""
        buttons = [
            [
                InlineKeyboardButton("📜 Rules", callback_data="welcome_rules"),
                InlineKeyboardButton("🤖 Commands", callback_data="welcome_commands")
            ],
            [
                InlineKeyboardButton("👤 Profile", url=f"tg://user?id={user.id}"),
                InlineKeyboardButton("🌟 Star", callback_data="welcome_star")
            ]
        ]
        
        return InlineKeyboardMarkup(buttons)
