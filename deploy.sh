#!/bin/bash
# 🎮 Game Bot Deployment Script

echo "🚀 Starting Game Bot Deployment..."

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.9+"
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env if not exists
if [ ! -f .env ]; then
    echo "📝 Creating .env from example..."
    cp .env.example .env
    echo "⚠️ Please edit .env and add your BOT_TOKEN!"
fi

# Initialize database
echo "🗄️ Initializing database..."
python3 -c "from database import db; print('Database ready!')"

echo ""
echo "✅ Setup complete!"
echo "📝 Edit .env file with your BOT_TOKEN and ADMIN_IDS"
echo "🚀 Run: python3 bot.py"
echo ""
