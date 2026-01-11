"""
SECURITY FEATURE
Basic security for Nila Bot
"""

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
from datetime import datetime, timedelta

class SecurityFeature:
    """Basic security system"""
    
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.blocked_users = set()
        self.user_warnings = {}
        self.flood_control = {}
    
    def register(self):
        """Register security handlers"""
        # Anti-flood
        self.app.add_handler(
            MessageHandler(filters.ALL & ~filters.COMMAND, self.anti_flood)
        )
    
    async def anti_flood(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Anti-flood protection"""
        user_id = update.effective_user.id
        current_time = datetime.now()
        
        # Initialize user tracking
        if user_id not in self.flood_control:
            self.flood_control[user_id] = {
                "messages": [],
                "warnings": 0,
                "muted_until": None
            }
        
        user_data = self.flood_control[user_id]
        
        # Check if user is muted
        if user_data["muted_until"] and current_time < user_data["muted_until"]:
            await update.message.delete()
            return
        
        # Add message to history
        user_data["messages"].append(current_time)
        
        # Remove old messages (older than 10 seconds)
        user_data["messages"] = [
            msg_time for msg_time in user_data["messages"]
            if current_time - msg_time < timedelta(seconds=10)
        ]
        
        # Check flood threshold (more than 5 messages in 10 seconds)
        if len(user_data["messages"]) > 5:
            user_data["warnings"] += 1
            
            if user_data["warnings"] >= 3:
                # Mute user for 5 minutes
                user_data["muted_until"] = current_time + timedelta(minutes=5)
                await update.message.reply_text(
                    f"🚫 User {update.effective_user.mention_html()} "
                    f"has been muted for 5 minutes due to flooding.",
                    parse_mode='HTML'
                )
            else:
                # Warning
                await update.message.reply_text(
                    f"⚠️ Please slow down {update.effective_user.mention_html()}!",
                    parse_mode='HTML'
                )
            
            # Clear messages after warning
            user_data["messages"] = []
    
    async def check_admin(self, user_id: int) -> bool:
        """Check if user is admin"""
        owner_id = self.config.get_owner_id()
        return user_id == owner_id
