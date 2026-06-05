"""
Game Bot Configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Token - 从 @BotFather 获取
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Admin IDs (逗号分隔)
ADMIN_IDS = [int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///game_bot.db")

# Game Settings
MIN_BET = 1
MAX_BET = 10000
REFERRAL_BONUS = 5  # 邀请奖励金额
DAILY_BONUS = 10    # 每日签到奖励

# Payment Settings
PAYMENT_METHODS = {
    "usdt": {"name": "USDT (TRC20)", "min": 10, "max": 10000},
    "usdt_erc": {"name": "USDT (ERC20)", "min": 20, "max": 50000},
    "btc": {"name": "Bitcoin", "min": 0.001, "max": 10},
}

# Withdrawal Settings
MIN_WITHDRAW = 10
WITHDRAW_FEE = 0.02  # 2%手续费

# Game Configs
GAME_CONFIGS = {
    "dice": {"name": "🎲 Dice", "min_bet": 1, "max_bet": 1000},
    "slots": {"name": "🎰 Slots", "min_bet": 1, "max_bet": 5000},
    "coin": {"name": "🪙 Coin Flip", "min_bet": 1, "max_bet": 500},
    "roulette": {"name": "🎡 Roulette", "min_bet": 5, "max_bet": 10000},
    "crash": {"name": "📈 Crash", "min_bet": 1, "max_bet": 5000},
}

# Languages
LANGUAGES = {
    "en": "🇬🇧 English",
    "zh": "🇨🇳 中文",
    "ja": "🇯🇵 日本語",
    "ko": "🇰🇷 한국어",
    "ru": "🇷🇺 Русский",
}

# Official Links
OFFICIAL_CHANNEL = os.getenv("OFFICIAL_CHANNEL", "")
CUSTOMER_SERVICE = os.getenv("CUSTOMER_SERVICE", "")
APP_DOWNLOAD_URL = os.getenv("APP_DOWNLOAD_URL", "")
