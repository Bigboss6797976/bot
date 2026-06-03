import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

GAME_BASE_URL = "https://j88sports.com/home/index"

GAME_PATHS = {
    "sports": "/sports",
    "live_casino": "/live-casino",
    "slots": "/slots",
    "chess": "/chess",
    "promotions": "/promotions"
}

OFFICIAL_CHANNEL = "https://t.me/J88sportsbot"
OFFICIAL_GROUP = "https://t.me/J88sportsbot"
OFFICIAL_SUPPORT = "https://t.me/J88sportsbot"
GAME_BOT = "https://t.me/J88sportsbot"
