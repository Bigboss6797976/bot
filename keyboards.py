"""
Keyboard layouts for the bot
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from config import GAME_CONFIGS, LANGUAGES, PAYMENT_METHODS
from locales.i18n import get_text

def get_main_menu_keyboard(lang="en"):
    """Main menu keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_text("enter_game", lang), callback_data="menu_games")],
        [
            InlineKeyboardButton(get_text("top_up", lang), callback_data="menu_deposit"),
            InlineKeyboardButton(get_text("withdrawal", lang), callback_data="menu_withdraw")
        ],
        [
            InlineKeyboardButton(get_text("invite_friends", lang), callback_data="menu_invite"),
            InlineKeyboardButton(get_text("customer_service", lang), url="https://t.me/your_support")
        ],
        [
            InlineKeyboardButton(get_text("download_app", lang), callback_data="menu_download"),
            InlineKeyboardButton(get_text("official_channel", lang), url="https://t.me/your_channel")
        ],
        [
            InlineKeyboardButton(get_text("account_info", lang), callback_data="menu_account"),
            InlineKeyboardButton(get_text("switch_language", lang), callback_data="menu_language")
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_games_keyboard(lang="en"):
    """Games selection keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(get_text("dice", lang), callback_data="game_dice"),
            InlineKeyboardButton(get_text("slots", lang), callback_data="game_slots")
        ],
        [
            InlineKeyboardButton(get_text("coin", lang), callback_data="game_coin"),
            InlineKeyboardButton(get_text("roulette", lang), callback_data="game_roulette")
        ],
        [
            InlineKeyboardButton(get_text("crash", lang), callback_data="game_crash")
        ],
        [
            InlineKeyboardButton(get_text("leaderboard", lang), callback_data="menu_leaderboard"),
            InlineKeyboardButton(get_text("history", lang), callback_data="menu_history")
        ],
        [InlineKeyboardButton(get_text("back", lang), callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_keyboard(lang="en", callback="menu_main"):
    """Simple back button"""
    keyboard = [[InlineKeyboardButton(get_text("back", lang), callback_data=callback)]]
    return InlineKeyboardMarkup(keyboard)

def get_bet_amounts_keyboard(lang="en", game="dice", min_bet=1, max_bet=1000):
    """Quick bet amounts keyboard"""
    amounts = [1, 5, 10, 25, 50, 100, 250, 500, 1000]
    valid_amounts = [a for a in amounts if min_bet <= a <= max_bet]

    keyboard = []
    row = []
    for i, amount in enumerate(valid_amounts):
        row.append(InlineKeyboardButton(str(amount), callback_data=f"bet_{game}_{amount}"))
        if (i + 1) % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    keyboard.append([InlineKeyboardButton(get_text("back", lang), callback_data="menu_games")])
    return InlineKeyboardMarkup(keyboard)

def get_dice_choice_keyboard(lang="en", bet_amount=10):
    """Dice number selection"""
    keyboard = []
    row = []
    for i in range(1, 7):
        row.append(InlineKeyboardButton(str(i), callback_data=f"dice_num_{bet_amount}_{i}"))
        if i % 3 == 0:
            keyboard.append(row)
            row = []

    keyboard.append([
        InlineKeyboardButton(get_text("red", lang), callback_data=f"dice_color_{bet_amount}_over"),
        InlineKeyboardButton(get_text("black", lang), callback_data=f"dice_color_{bet_amount}_under")
    ])
    keyboard.append([InlineKeyboardButton(get_text("back", lang), callback_data=f"game_dice")])
    return InlineKeyboardMarkup(keyboard)

def get_coin_choice_keyboard(lang="en", bet_amount=10):
    """Coin flip choice"""
    keyboard = [
        [
            InlineKeyboardButton(get_text("heads", lang), callback_data=f"coin_choice_{bet_amount}_heads"),
            InlineKeyboardButton(get_text("tails", lang), callback_data=f"coin_choice_{bet_amount}_tails")
        ],
        [InlineKeyboardButton(get_text("back", lang), callback_data="game_coin")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_roulette_choice_keyboard(lang="en", bet_amount=10):
    """Roulette choice"""
    keyboard = [
        [
            InlineKeyboardButton(get_text("red", lang), callback_data=f"roulette_color_{bet_amount}_red"),
            InlineKeyboardButton(get_text("black", lang), callback_data=f"roulette_color_{bet_amount}_black"),
            InlineKeyboardButton(get_text("green", lang), callback_data=f"roulette_color_{bet_amount}_green")
        ],
        [
            InlineKeyboardButton("Even", callback_data=f"roulette_eo_{bet_amount}_even"),
            InlineKeyboardButton("Odd", callback_data=f"roulette_eo_{bet_amount}_odd")
        ]
    ]

    # Number grid
    numbers_row = []
    for i in range(37):
        numbers_row.append(InlineKeyboardButton(str(i), callback_data=f"roulette_num_{bet_amount}_{i}"))
        if (i + 1) % 7 == 0 or i == 36:
            keyboard.append(numbers_row)
            numbers_row = []

    keyboard.append([InlineKeyboardButton(get_text("back", lang), callback_data="game_roulette")])
    return InlineKeyboardMarkup(keyboard)

def get_crash_keyboard(lang="en"):
    """Crash game keyboard"""
    keyboard = [
        [InlineKeyboardButton(get_text("start_crash", lang), callback_data="crash_start")],
        [InlineKeyboardButton(get_text("cash_out", lang), callback_data="crash_cashout")],
        [InlineKeyboardButton(get_text("back", lang), callback_data="menu_games")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_payment_methods_keyboard(lang="en"):
    """Payment methods keyboard"""
    keyboard = []
    for key, method in PAYMENT_METHODS.items():
        keyboard.append([InlineKeyboardButton(
            method["name"], 
            callback_data=f"deposit_method_{key}"
        )])
    keyboard.append([InlineKeyboardButton(get_text("back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(keyboard)

def get_language_keyboard(lang="en"):
    """Language selection keyboard"""
    keyboard = []
    for code, name in LANGUAGES.items():
        keyboard.append([InlineKeyboardButton(name, callback_data=f"lang_{code}")])
    keyboard.append([InlineKeyboardButton(get_text("back", lang), callback_data="menu_main")])
    return InlineKeyboardMarkup(keyboard)

def get_account_keyboard(lang="en"):
    """Account info keyboard"""
    keyboard = [
        [
            InlineKeyboardButton(get_text("daily_bonus", lang), callback_data="claim_daily_bonus"),
            InlineKeyboardButton(get_text("history", lang), callback_data="menu_history")
        ],
        [
            InlineKeyboardButton(get_text("leaderboard", lang), callback_data="menu_leaderboard"),
            InlineKeyboardButton(get_text("settings", lang), callback_data="menu_settings")
        ],
        [InlineKeyboardButton(get_text("back", lang), callback_data="menu_main")]
    ]
    return InlineKeyboardMarkup(keyboard)
