#!/usr/bin/env python3
"""
UU-Style Telegram 推广导航 Bot
部署: Render (Web Service)
"""
import os
import logging
import asyncio
from datetime import datetime
from flask import Flask, request, jsonify
import threading
import json

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# ========== 配置 ==========
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
ADMIN_IDS = [int(x.strip()) for x in os.environ.get("ADMIN_IDS", "").split(",") if x.strip()]
WEBAPP_URL = os.environ.get("WEBAPP_URL", "")

# 推广链接配置
PROMO_LINKS = {
    "official_website": os.environ.get("OFFICIAL_URL", "https://example.com"),
    "download_app": os.environ.get("APP_URL", "https://example.com/app"),
    "mini_app": os.environ.get("MINI_APP_URL", "https://t.me/your_bot/app"),
    "customer_service": os.environ.get("CS_URL", "https://t.me/your_support"),
    "promotion_agent": os.environ.get("AGENT_URL", "https://t.me/your_agent"),
    "group_link": os.environ.get("GROUP_URL", "https://t.me/your_group"),
    "channel_link": os.environ.get("CHANNEL_URL", "https://t.me/your_channel"),
}

# 横幅图片
BANNER_IMAGE = os.environ.get("BANNER_IMAGE", "")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ========== 数据存储 ==========
users_db = {}
stats = {"total_users": 0, "total_clicks": 0, "start_time": datetime.now().isoformat()}

# ========== Flask 后端 ==========
flask_app = Flask(__name__)
flask_app.secret_key = os.environ.get("SECRET_KEY", "uu-bot-secret-key")

@flask_app.route('/')
def home():
    return "✅ UU-Style Promo Bot is running!"

@flask_app.route('/health')
def health():
    return jsonify({
        "status": "running",
        "users": len(users_db),
        "stats": stats,
        "time": datetime.now().isoformat()
    })

# ========== Bot 命令处理器 ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """启动命令 - 发送精美推广消息"""
    user = update.effective_user
    chat = update.effective_chat

    # 记录用户
    uid = str(user.id)
    if uid not in users_db:
        users_db[uid] = {
            "user_id": user.id,
            "username": user.username or "",
            "first_name": user.first_name or "",
            "last_name": user.last_name or "",
            "joined_at": datetime.now().isoformat(),
            "clicks": 0
        }
        stats["total_users"] = len(users_db)

    # 推广文案
    welcome_text = (
        f"🎰 <b>UU娱乐 6A.COM</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 <b>2026 美·加·墨 世界杯</b>\n"
        f"✅ 官网指定投注平台\n\n"
        f"🎖️ <b>澳门热门 · 全球风靡 · WG线上首发</b>\n\n"
        f"💥 自进入澳门市场以来，【龙之连环】系列凭借创新连环彩金玩法、"
        f"丰富Bonus奖励及超高人气，迅速风靡全球实体赌场，"
        f"并广受美国、韩国、欧洲及东南亚玩家争相体验。\n\n"
        f"🔥 <b>热门游戏推荐：</b>\n"
        f"  🎰 喜悦富足（第一代经典）\n"
        f"  🎰 熊猫魔力\n"
        f"  🎰 新春佳节\n"
        f"  🎰 黄金盛世（第二代爆款）\n"
        f"  🎰 中秋明月\n\n"
        f"💎 <b>立即夺取百万超级奖金池！</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )

    # 按钮布局
    keyboard = [
        [
            InlineKeyboardButton("✅ 官方网址", url=PROMO_LINKS["official_website"]),
            InlineKeyboardButton("📱 下载APP", url=PROMO_LINKS["download_app"]),
        ],
        [
            InlineKeyboardButton("🚀 飞投小程序", url=PROMO_LINKS["mini_app"]),
        ],
        [
            InlineKeyboardButton("💬 官方客服", url=PROMO_LINKS["customer_service"]),
            InlineKeyboardButton("🎀 推广代理", url=PROMO_LINKS["promotion_agent"]),
        ],
        [
            InlineKeyboardButton("👥 加入群组", url=PROMO_LINKS["group_link"]),
            InlineKeyboardButton("📢 订阅频道", url=PROMO_LINKS["channel_link"]),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # 发送带图片或纯文本
    if BANNER_IMAGE:
        try:
            await context.bot.send_photo(
                chat_id=chat.id,
                photo=BANNER_IMAGE,
                caption=welcome_text,
                reply_markup=reply_markup,
                parse_mode="HTML"
            )
            return
        except Exception as e:
            logger.warning(f"发送图片失败: {e}")

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📖 <b>使用帮助</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "/start - 显示主推广页面\n"
        "/menu - 显示菜单\n"
        "/help - 显示帮助\n"
        "/stats - 查看统计（管理员）\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(help_text, parse_mode="HTML")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ 无权访问")
        return

    stats_text = (
        f"📊 <b>数据统计</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 总用户数: {stats['total_users']}\n"
        f"👆 总点击量: {stats['total_clicks']}\n"
        f"⏱️ 运行时间: {stats['start_time'][:10]}\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    await update.message.reply_text(stats_text, parse_mode="HTML")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ 无权访问")
        return

    if not context.args:
        await update.message.reply_text("用法: /broadcast <消息内容>")
        return

    message = " ".join(context.args)
    sent = 0
    failed = 0

    for uid in list(users_db.keys()):
        try:
            await context.bot.send_message(
                chat_id=int(uid),
                text=message,
                parse_mode="HTML"
            )
            sent += 1
        except Exception:
            failed += 1

    await update.message.reply_text(
        f"✅ 广播完成\n发送成功: {sent}\n发送失败: {failed}"
    )

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    stats["total_clicks"] += 1
    user_id = str(update.effective_user.id)
    if user_id in users_db:
        users_db[user_id]["clicks"] = users_db[user_id].get("clicks", 0) + 1

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} caused error {context.error}")

# ========== 启动 ==========
def run_flask():
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

async def main():
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN 未设置！请在环境变量中设置 BOT_TOKEN")
        return

    # 启动 Flask
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("Flask server started on port %s", os.environ.get("PORT", 5000))

    # 创建 Bot
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", menu_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CallbackQueryHandler(callback_handler))
    application.add_error_handler(error_handler)

    logger.info("Starting bot...")

    # 使用 Webhook 或 Polling
    webhook_url = os.environ.get("WEBHOOK_URL", "")
    if webhook_url:
        await application.bot.set_webhook(webhook_url)
        await application.start()
        logger.info(f"Webhook set to {webhook_url}")
        # 保持运行
        await asyncio.Event().wait()
    else:
        await application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
