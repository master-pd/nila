"""
AUTO RESPONSE FEATURE
Smart auto-responses
"""

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters
import random

class AutoResponseFeature:
    """Smart auto-response system"""
    
    def __init__(self, app, config, auto_cmd):
        self.app = app
        self.config = config
        self.auto_cmd = auto_cmd
        
        # Default responses
        self.responses = {
            "how are you": [
                "I'm doing great, thanks for asking! 😊",
                "I'm excellent! How about you? 🌟",
                "All systems operational! 🤖",
                "Feeling amazing today! ✨"
            ],
            "thank you": [
                "You're welcome! 😊",
                "My pleasure! 🌟",
                "Anytime! 😄",
                "Happy to help! 🤖"
            ],
            "what can you do": [
                "I can do many things! Use /help to see my commands! 🤖",
                "I'm a multi-talented bot! Check /help for details! 🌟",
                "Lots of cool features! Type /help to explore! ✨"
            ],
            "who made you": [
                "I was created by a talented developer! 🤖✨",
                "I'm the creation of an amazing programmer! 🌟",
                "A wonderful developer brought me to life! 💫"
            ]
        }
    
    def register(self):
        """Register auto-response handler"""
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.auto_respond)
        )
    
    async def auto_respond(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle auto-responses"""
        message = update.message.text.lower()
        
        # Check for matching responses
        for trigger, responses in self.responses.items():
            if trigger in message:
                response = random.choice(responses)
                await update.message.reply_text(response)
                break
