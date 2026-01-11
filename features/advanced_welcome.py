"""
ADVANCED WELCOME SYSTEM
With AI image generation and animations
"""

import asyncio
import random
from datetime import datetime
from typing import Dict, List
from pathlib import Path
import aiohttp
from io import BytesIO

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, MessageHandler, filters
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np

from stylish_text import StylishText
from utils.termux_helper import TermuxHelper

class AdvancedWelcomeSystem:
    """Ultra advanced welcome system with AI features"""
    
    def __init__(self, app, config):
        self.app = app
        self.config = config
        self.templates = self._load_templates()
        self.user_profiles = {}
        
        # Background image URLs (free sources)
        self.backgrounds = [
            "https://images.unsplash.com/photo-1550684376-efcbd6e3f031?w=800",
            "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=800",
            "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800",
            "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=800"
        ]
    
    def _load_templates(self) -> Dict:
        """Load welcome templates"""
        return {
            "cyberpunk": {
                "bg_color": "#0a0a0a",
                "text_color": "#00ff9d",
                "accent_color": "#ff00ff",
                "font": "cyberpunk",
                "effects": ["glitch", "scan_lines", "neon_glow"]
            },
            "elegant": {
                "bg_color": "#1a1a2e",
                "text_color": "#ffffff",
                "accent_color": "#e94560",
                "font": "elegant",
                "effects": ["gold_border", "gradient", "shadow"]
            },
            "modern": {
                "bg_color": "#16213e",
                "text_color": "#e6e6e6",
                "accent_color": "#0fcea7",
                "font": "modern",
                "effects": ["blur", "grid", "particles"]
            },
            "vintage": {
                "bg_color": "#2d2424",
                "text_color": "#e0c097",
                "accent_color": "#b85c38",
                "font": "vintage",
                "effects": ["noise", "sepia", "texture"]
            },
            "futuristic": {
                "bg_color": "#000428",
                "text_color": "#4cc9f0",
                "accent_color": "#f72585",
                "font": "futuristic",
                "effects": ["hologram", "data_stream", "pulse"]
            }
        }
    
    def register(self):
        """Register welcome handlers"""
        self.app.add_handler(
            MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, self.advanced_welcome)
        )
        
        # Welcome test command
        from auto_commands import AutoCommandSystem
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent))
        
        # Get auto_cmd instance
        from master import NilaBot
        # Note: This would need to be refactored for proper dependency injection
    
    async def advanced_welcome(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Advanced welcome with AI features"""
        chat = update.effective_chat
        
        for member in update.message.new_chat_members:
            if member.is_bot:
                continue
            
            # Get user profile
            user_profile = await self._get_user_profile(member)
            
            # Select template based on user profile
            template = self._select_template(user_profile)
            
            # Generate welcome package
            welcome_package = await self._generate_welcome_package(member, chat, template, user_profile)
            
            # Send welcome
            await self._send_welcome_package(update, member, welcome_package)
            
            # Update analytics
            self._update_analytics(member.id, chat.id)
    
    async def _get_user_profile(self, user) -> Dict:
        """Get user profile with AI analysis"""
        profile = {
            "id": user.id,
            "name": user.first_name or user.username or "User",
            "username": user.username,
            "join_date": datetime.now(),
            "profile_photo": None,
            "activity_score": random.randint(30, 100),
            "style_preference": random.choice(list(self.templates.keys())),
            "interests": self._detect_interests(user)
        }
        
        # Try to get profile photo
        try:
            photos = await user.get_profile_photos(limit=1)
            if photos.total_count > 0:
                file = await photos.photos[0][-1].get_file()
                profile["profile_photo"] = file.file_path
        except:
            pass
        
        # Store profile
        self.user_profiles[user.id] = profile
        
        return profile
    
    def _detect_interests(self, user) -> List[str]:
        """Detect user interests (simulated AI)"""
        interests_pool = [
            "gaming", "music", "art", "technology", "sports",
            "movies", "programming", "photography", "travel",
            "food", "fitness", "books", "science", "business"
        ]
        
        # Simulate AI detection based on username and name
        user_text = (user.first_name or "") + (user.username or "")
        user_text = user_text.lower()
        
        detected = []
        for interest in interests_pool:
            if interest in user_text or random.random() > 0.7:
                detected.append(interest)
        
        return detected[:3]  # Return top 3 interests
    
    def _select_template(self, profile: Dict) -> str:
        """Select welcome template based on user profile"""
        # Check if user has style preference
        if profile["style_preference"] in self.templates:
            return profile["style_preference"]
        
        # Select based on interests
        interests = profile["interests"]
        
        if "gaming" in interests or "technology" in interests:
            return "cyberpunk"
        elif "art" in interests or "photography" in interests:
            return "elegant"
        elif "science" in interests or "programming" in interests:
            return "futuristic"
        elif "travel" in interests or "food" in interests:
            return "vintage"
        else:
            return "modern"
    
    async def _generate_welcome_package(self, user, chat, template: str, profile: Dict) -> Dict:
        """Generate complete welcome package"""
        package = {}
        
        # 1. Generate AI image
        package["image"] = await self._generate_welcome_image(user, chat, template, profile)
        
        # 2. Generate styled message
        package["message"] = self._generate_welcome_message(user, chat, template, profile)
        
        # 3. Generate interactive buttons
        package["buttons"] = self._generate_interactive_buttons(user, profile)
        
        # 4. Generate audio welcome (if enabled)
        if self.config.get("features.audio_welcome", False):
            package["audio"] = await self._generate_welcome_audio(user, profile)
        
        # 5. Generate animation (GIF)
        if self.config.get("features.animated_welcome", False):
            package["animation"] = await self._generate_welcome_animation(user, template)
        
        return package
    
    async def _generate_welcome_image(self, user, chat, template: str, profile: Dict) -> Image.Image:
        """Generate AI-powered welcome image"""
        try:
            # Download background
            bg_url = random.choice(self.backgrounds)
            async with aiohttp.ClientSession() as session:
                async with session.get(bg_url) as response:
                    bg_data = await response.read()
            
            background = Image.open(BytesIO(bg_data)).resize((800, 400))
            
            # Apply template effects
            template_data = self.templates[template]
            background = self._apply_template_effects(background, template_data)
            
            # Create drawing context
            draw = ImageDraw.Draw(background)
            
            # Add user name with stylish text
            user_name = StylishText.generate(profile["name"], "bold")
            
            # Load font (use default if custom font not available)
            try:
                font_path = Path(__file__).parent / "fonts" / f"{template_data['font']}.ttf"
                if font_path.exists():
                    font = ImageFont.truetype(str(font_path), 40)
                else:
                    font = ImageFont.load_default()
            except:
                font = ImageFont.load_default()
            
            # Draw user name
            text_bbox = draw.textbbox((0, 0), user_name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = (background.width - text_width) // 2
            text_y = 100
            
            draw.text((text_x, text_y), user_name, font=font, fill=template_data["text_color"])
            
            # Add welcome text
            welcome_text = "WELCOME TO"
            welcome_font = ImageFont.load_default()
            
            if hasattr(font, 'size'):
                welcome_font = ImageFont.truetype(str(font_path), 24) if font_path.exists() else ImageFont.load_default()
            
            welcome_bbox = draw.textbbox((0, 0), welcome_text, font=welcome_font)
            welcome_width = welcome_bbox[2] - welcome_bbox[0]
            
            welcome_x = (background.width - welcome_width) // 2
            welcome_y = text_y - 40
            
            draw.text((welcome_x, welcome_y), welcome_text, font=welcome_font, fill=template_data["accent_color"])
            
            # Add chat name
            chat_name = chat.title if hasattr(chat, 'title') else "Our Community"
            chat_text = f"🎯 {chat_name}"
            
            chat_bbox = draw.textbbox((0, 0), chat_text, font=welcome_font)
            chat_width = chat_bbox[2] - chat_bbox[0]
            
            chat_x = (background.width - chat_width) // 2
            chat_y = text_y + text_height + 20
            
            draw.text((chat_x, chat_y), chat_text, font=welcome_font, fill=template_data["text_color"])
            
            # Add user info
            info_y = chat_y + 40
            info_lines = [
                f"🆔 ID: {user.id}",
                f"📅 Joined: {datetime.now().strftime('%d %b %Y')}",
                f"⭐ Activity Score: {profile['activity_score']}/100"
            ]
            
            for i, line in enumerate(info_lines):
                draw.text((50, info_y + i*30), line, font=welcome_font, fill="#ffffff")
            
            # Add interests
            if profile["interests"]:
                interests_text = "🎯 Interests: " + ", ".join(profile["interests"])
                draw.text((50, info_y + 100), interests_text, font=welcome_font, fill=template_data["accent_color"])
            
            # Add decorative elements
            self._add_decorative_elements(draw, background, template_data)
            
            return background
            
        except Exception as e:
            print(f"Error generating image: {e}")
            # Return simple image as fallback
            return self._generate_fallback_image(user, profile)
    
    def _apply_template_effects(self, image: Image.Image, template: Dict) -> Image.Image:
        """Apply template effects to image"""
        effects = template.get("effects", [])
        
        for effect in effects:
            if effect == "blur":
                image = image.filter(ImageFilter.GaussianBlur(1))
            elif effect == "glitch":
                # Simple glitch effect
                import random
                pixels = image.load()
                width, height = image.size
                
                for _ in range(100):  # Add 100 glitch pixels
                    x = random.randint(0, width-1)
                    y = random.randint(0, height-1)
                    pixels[x, y] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            elif effect == "sepia":
                # Convert to sepia
                sepia = image.convert("RGB")
                width, height = sepia.size
                pixels = sepia.load()
                
                for py in range(height):
                    for px in range(width):
                        r, g, b = pixels[px, py]
                        tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                        tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                        tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                        pixels[px, py] = (min(255, tr), min(255, tg), min(255, tb))
                
                image = sepia
        
        return image
    
    def _add_decorative_elements(self, draw, image, template: Dict):
        """Add decorative elements to image"""
        width, height = image.size
        
        # Add border
        border_color = template["accent_color"]
        draw.rectangle([(10, 10), (width-10, height-10)], outline=border_color, width=3)
        
        # Add corner accents
        corner_size = 20
        draw.line([(10, 10), (10+corner_size, 10)], fill=border_color, width=2)
        draw.line([(10, 10), (10, 10+corner_size)], fill=border_color, width=2)
        
        draw.line([(width-10, 10), (width-10-corner_size, 10)], fill=border_color, width=2)
        draw.line([(width-10, 10), (width-10, 10+corner_size)], fill=border_color, width=2)
        
        draw.line([(10, height-10), (10+corner_size, height-10)], fill=border_color, width=2)
        draw.line([(10, height-10), (10, height-10-corner_size)], fill=border_color, width=2)
        
        draw.line([(width-10, height-10), (width-10-corner_size, height-10)], fill=border_color, width=2)
        draw.line([(width-10, height-10), (width-10, height-10-corner_size)], fill=border_color, width=2)
        
        # Add random decorative dots
        import random
        for _ in range(20):
            x = random.randint(20, width-20)
            y = random.randint(20, height-20)
            radius = random.randint(1, 3)
            draw.ellipse([(x-radius, y-radius), (x+radius, y+radius)], fill=template["text_color"])
    
    def _generate_fallback_image(self, user, profile: Dict) -> Image.Image:
        """Generate fallback welcome image"""
        image = Image.new('RGB', (800, 400), color='#1a1a2e')
        draw = ImageDraw.Draw(image)
        
        # Simple welcome text
        welcome_text = f"Welcome {profile['name']}!"
        font = ImageFont.load_default()
        
        # Try to load a larger font
        try:
            font = ImageFont.truetype("/system/fonts/Roboto-Regular.ttf", 40)
        except:
            pass
        
        text_bbox = draw.textbbox((0, 0), welcome_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        
        text_x = (800 - text_width) // 2
        text_y = 150
        
        draw.text((text_x, text_y), welcome_text, font=font, fill='#ffffff')
        
        # Add simple decoration
        draw.rectangle([(50, 50), (750, 350)], outline='#e94560', width=2)
        
        return image
    
    def _generate_welcome_message(self, user, chat, template: str, profile: Dict) -> str:
        """Generate styled welcome message"""
        template_data = self.templates[template]
        
        # Get stylish name
        styled_name = StylishText.generate(profile["name"], "bold")
        
        # Get random welcome phrase
        welcome_phrases = [
            f"🌟 A warm welcome to {styled_name}!",
            f"✨ {styled_name} has joined the party!",
            f"🎉 Welcome aboard, {styled_name}!",
            f"👋 Hello there, {styled_name}!",
            f"💫 {styled_name} just made our day brighter!",
            f"🔥 {styled_name} is here to set things on fire!"
        ]
        
        welcome_line = random.choice(welcome_phrases)
        
        # Generate message
        message = f"""
{template_data.get('emoji', '✨')} {welcome_line} {template_data.get('emoji', '✨')}

━━━━━━━━━━━━━━━━━━━━━━
📋 *User Information:*
├─ 🆔 ID: `{user.id}`
├─ 👤 Username: @{profile['username'] or 'N/A'}
├─ 📅 Joined: {datetime.now().strftime('%Y-%m-%d %H:%M')}
└─ ⭐ Activity Score: {profile['activity_score']}/100

🎯 *Detected Interests:*
{', '.join(profile['interests']) if profile['interests'] else 'Exploring...'}

━━━━━━━━━━━━━━━━━━━━━━
💡 *Quick Tips:*
• Use /help to see all commands
• Read the group rules
• Be respectful to everyone
• Have fun! 🎊

━━━━━━━━━━━━━━━━━━━━━━
        """
        
        return message
    
    def _generate_interactive_buttons(self, user, profile: Dict) -> InlineKeyboardMarkup:
        """Generate interactive welcome buttons"""
        buttons = []
        
        # Row 1: Basic actions
        buttons.append([
            InlineKeyboardButton("📜 Rules", callback_data=f"rules_{user.id}"),
            InlineKeyboardButton("🤖 Commands", callback_data=f"commands_{user.id}")
        ])
        
        # Row 2: User actions
        buttons.append([
            InlineKeyboardButton("👤 Profile", callback_data=f"profile_{user.id}"),
            InlineKeyboardButton("⭐ Rate", callback_data=f"rate_{user.id}")
        ])
        
        # Row 3: Special actions based on interests
        if profile["interests"]:
            interest = profile["interests"][0]
            if interest == "gaming":
                buttons.append([
                    InlineKeyboardButton("🎮 Play Game", callback_data=f"game_{user.id}")
                ])
            elif interest == "music":
                buttons.append([
                    InlineKeyboardButton("🎵 Music", callback_data=f"music_{user.id}")
                ])
            elif interest == "art":
                buttons.append([
                    InlineKeyboardButton("🎨 Art Gallery", callback_data=f"art_{user.id}")
                ])
        
        # Row 4: Admin actions (if user is special)
        if profile["activity_score"] > 80:
            buttons.append([
                InlineKeyboardButton("🌟 Premium Welcome", callback_data=f"premium_{user.id}")
            ])
        
        return InlineKeyboardMarkup(buttons)
    
    async def _generate_welcome_audio(self, user, profile: Dict):
        """Generate welcome audio message"""
        # This would require text-to-speech API
        # For now, return None
        return None
    
    async def _generate_welcome_animation(self, user, template: str):
        """Generate welcome animation"""
        # This would require GIF generation
        # For now, return None
        return None
    
    async def _send_welcome_package(self, update, user, package: Dict):
        """Send complete welcome package"""
        try:
            # Convert image to bytes
            img_byte_arr = BytesIO()
            package["image"].save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Send image with caption
            await update.message.reply_photo(
                photo=img_byte_arr,
                caption=package["message"],
                parse_mode='Markdown',
                reply_markup=package["buttons"]
            )
            
            # Send audio if available
            if "audio" in package and package["audio"]:
                await update.message.reply_voice(
                    voice=package["audio"],
                    caption="🎵 Welcome audio message!"
                )
            
            # Send animation if available
            if "animation" in package and package["animation"]:
                await update.message.reply_animation(
                    animation=package["animation"],
                    caption="🎬 Animated welcome!"
                )
                
        except Exception as e:
            print(f"Error sending welcome: {e}")
            # Fallback to simple welcome
            await update.message.reply_text(
                f"👋 Welcome {user.first_name or user.username}!",
                reply_markup=package["buttons"]
            )
    
    def _update_analytics(self, user_id: int, chat_id: int):
        """Update welcome analytics"""
        # Store analytics in vault
        from utils.crypto_vault import vault
        
        analytics = vault.retrieve("welcome_analytics", {})
        
        today = datetime.now().strftime("%Y-%m-%d")
        
        if today not in analytics:
            analytics[today] = {"total": 0, "users": []}
        
        analytics[today]["total"] += 1
        analytics[today]["users"].append({
            "user_id": user_id,
            "chat_id": chat_id,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 30 days
        dates = sorted(analytics.keys(), reverse=True)
        if len(dates) > 30:
            for old_date in dates[30:]:
                del analytics[old_date]
        
        vault.store("welcome_analytics", analytics)
