#!/usr/bin/env python3
"""
NILA BOT - MAIN CONTROLLER
Professional Telegram Bot | No ENV | No Hardcode
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from telegram.ext import Application
from config_manager import config
from stylish_text import StylishText
from auto_commands import AutoCommandSystem, create_default_commands
from features.welcome_pro import WelcomeProFeature
from features.security import SecurityFeature
from features.auto_responses import AutoResponseFeature

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

class NilaBot:
    """Main Nila Bot Controller"""
    
    def __init__(self):
        self.config = config
        self.app = None
        self.auto_cmd = None
        self.features = {}
        
    async def start(self):
        """Start the bot"""
        try:
            # Validate configuration
            if not self.config.validate_config():
                logger.error("❌ Invalid configuration. Please run setup.py")
                return
            
            bot_token = self.config.get_bot_token()
            bot_name = self.config.get("bot_name", "Nila Bot")
            
            # Create stylish banner
            banner = StylishText.create_banner(f"{bot_name} STARTING")
            print(banner)
            
            # Initialize Telegram application
            logger.info("🚀 Initializing Nila Bot...")
            self.app = Application.builder().token(bot_token).build()
            
            # Initialize auto-command system
            self.auto_cmd = AutoCommandSystem(self.app, self.config)
            
            # Create default commands
            create_default_commands(self.app, self.config, self.auto_cmd)
            
            # Load features based on config
            await self._load_features()
            
            # Start the bot
            logger.info("✅ Bot initialized successfully")
            logger.info(f"🤖 Bot Name: {bot_name}")
            logger.info(f"👤 Owner ID: {self.config.get_owner_id()}")
            logger.info(f"📊 Features: {len(self.features)} loaded")
            
            # Run bot
            await self.app.initialize()
            await self.app.start()
            logger.info("🟢 Bot is now running!")
            
            # Run forever
            await self._run_forever()
            
        except Exception as e:
            logger.error(f"❌ Error starting bot: {e}")
            raise
    
    async def _load_features(self):
        """Load enabled features"""
        features_config = self.config.get("features", {})
        
        # Welcome feature
        if features_config.get("welcome", False):
            try:
                welcome_feature = WelcomeProFeature(self.app, self.config)
                welcome_feature.register()
                self.features["welcome"] = welcome_feature
                logger.info("✅ Welcome feature loaded")
            except Exception as e:
                logger.error(f"❌ Failed to load welcome feature: {e}")
        
        # Security feature
        if features_config.get("security", False):
            try:
                security_feature = SecurityFeature(self.app, self.config)
                security_feature.register()
                self.features["security"] = security_feature
                logger.info("✅ Security feature loaded")
            except Exception as e:
                logger.error(f"❌ Failed to load security feature: {e}")
        
        # Auto-response feature
        if features_config.get("auto_response", False):
            try:
                auto_response = AutoResponseFeature(self.app, self.config, self.auto_cmd)
                auto_response.register()
                self.features["auto_response"] = auto_response
                logger.info("✅ Auto-response feature loaded")
            except Exception as e:
                logger.error(f"❌ Failed to load auto-response feature: {e}")
    
    async def _run_forever(self):
        """Keep the bot running"""
        try:
            # Run until stopped
            while True:
                await asyncio.sleep(3600)  # Sleep for 1 hour
        except asyncio.CancelledError:
            logger.info("Bot stopping...")
        finally:
            await self._shutdown()
    
    async def _shutdown(self):
        """Shutdown bot gracefully"""
        logger.info("🛑 Shutting down Nila Bot...")
        
        if self.app:
            await self.app.stop()
            await self.app.shutdown()
        
        logger.info("✅ Bot shutdown complete")

async def main():
    """Main entry point"""
    bot = NilaBot()
    
    try:
        await bot.start()
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if setup is needed
    if not config.get_bot_token():
        print("\n" + "="*50)
        print("❌ Nila Bot is not configured!")
        print("💡 Please run setup.py first")
        print("="*50 + "\n")
        print("Command: python setup.py")
        sys.exit(1)
    
    # Run the bot
    asyncio.run(main())
