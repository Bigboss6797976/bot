from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import GAME_BASE_URL, OFFICIAL_CHANNEL, OFFICIAL_GROUP, OFFICIAL_SUPPORT, GAME_BOT

def main_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="🎰 进入游戏", url=GAME_BASE_URL)],
        [InlineKeyboardButton(text="📢 官方频道", url=OFFICIAL_CHANNEL)],
        [InlineKeyboardButton(text="💬 官方群组", url=OFFICIAL_GROUP)],
        [InlineKeyboardButton(text="👤 官方客服", url=OFFICIAL_SUPPORT)],
        [InlineKeyboardButton(text="🤖 游戏机器人", url=GAME_BOT)],
        [InlineKeyboardButton(text="🔐 官方认证公告", callback_data="security")],
        [InlineKeyboardButton(text="⚠️ 风险提示", callback_data="risk")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def back_button() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀ 返回主菜单", callback_data="back_to_main")]
    ])
