# 🎮 Game Bot - Telegram Casino Bot

A fully functional, real-time interactive Telegram game bot with multiple casino-style games, payment integration, referral system, and multi-language support.

## ✨ Features

- 🎲 **Dice** - Guess the number, win up to 5.8x
- 🎰 **Slots** - Match symbols, win up to 50x
- 🪙 **Coin Flip** - Heads or Tails, win 1.9x
- 🎡 **Roulette** - Numbers/Colors, win up to 35x
- 📈 **Crash** - Cash out before it crashes!
- 💰 **Top Up** - Multiple payment methods
- 💳 **Withdrawal** - Secure withdrawal system
- 👫 **Invite Friends** - Referral bonus system
- 🎁 **Daily Bonus** - Daily login rewards
- 🌍 **Multi-language** - EN/ZH/JA/KO/RU
- 🔧 **Admin Panel** - Full admin controls

## 🚀 Quick Start

### 1. Get Bot Token
- Go to [@BotFather](https://t.me/BotFather) on Telegram
- Create a new bot and copy the token

### 2. Clone & Setup
```bash
git clone <your-repo>
cd game_bot
chmod +x deploy.sh
./deploy.sh
```

### 3. Configure
Edit `.env` file:
```env
BOT_TOKEN=your_bot_token_here
ADMIN_IDS=your_telegram_id
```

### 4. Run
```bash
python3 bot.py
```

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

## ☁️ Render Deployment

1. Connect your GitHub repo to Render
2. Set environment variables in Render Dashboard
3. Deploy as a Web Service or Worker

## 📁 Project Structure

```
game_bot/
├── bot.py              # Main bot file
├── config.py           # Configuration
├── database.py         # Database models
├── keyboards.py        # Keyboard layouts
├── requirements.txt    # Dependencies
├── .env.example       # Environment template
├── games/             # Game logic
│   ├── __init__.py
│   ├── dice.py
│   ├── slots.py
│   ├── coin.py
│   ├── roulette.py
│   └── crash.py
├── locales/           # Translations
│   └── i18n.py
├── deploy.sh          # Deployment script
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 🛡️ Security Notes

- Never commit `.env` file
- Use strong database passwords in production
- Enable HTTPS for webhooks
- Regularly backup your database

## 📜 License

MIT License
