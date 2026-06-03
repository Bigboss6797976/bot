const express = require('express');
const TelegramBot = require('node-telegram-bot-api');

const TOKEN = process.env.BOT_TOKEN;
const PORT = process.env.PORT || 3000;

if (!TOKEN) {
  console.error('ERROR: BOT_TOKEN not set!');
  process.exit(1);
}

const app = express();
app.use(express.json());

// Bot Webhook 模式
const bot = new TelegramBot(TOKEN, { webHook: { port: PORT } });

// Webhook 路由
app.post(`/bot${TOKEN}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

// 健康检查
app.get('/', (req, res) => {
  res.send('✅ Telegram Game Bot is running!');
});

// 启动
app.listen(PORT, () => {
  console.log(`🚀 Bot server running on port ${PORT}`);
});

// ========== Bot 命令 ==========
bot.onText(/\/start/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, '🎮 欢迎来到游戏Bot！\n\n可用命令：\n/start - 开始\n/game - 开始游戏\n/help - 帮助');
});

bot.onText(/\/game/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, '🎯 游戏功能开发中...\n敬请期待！');
});

bot.onText(/\/help/, (msg) => {
  const chatId = msg.chat.id;
  bot.sendMessage(chatId, '📖 帮助文档\n\n/start - 开始使用\n/game - 游戏\n/help - 显示帮助');
});

console.log('🤖 Bot initialized');
