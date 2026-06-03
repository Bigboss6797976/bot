const express = require('express');
const TelegramBot = require('node-telegram-bot-api');

const TOKEN = process.env.BOT_TOKEN || '8481386791:AAEpHMmQqlnP6laT06rpF2LDItoQzxRE76w';
const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.json());

// 创建 Bot（不用 webHook 端口，后面手动绑定）
const bot = new TelegramBot(TOKEN);

// 手动设置 webhook 路由，绑定到 Express
app.post(`/bot${TOKEN}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

// 健康检查
app.get('/', (req, res) => {
  res.send('✅ Telegram Game Bot is running!');
});

// 只让 Express 监听端口
app.listen(PORT, () => {
  console.log(`🚀 Bot server running on port ${PORT}`);
});

// 设置 Telegram Webhook（部署后手动执行或用 API）
bot.setWebHook(`https://bottelegram-game-bot.onrender.com/bot${TOKEN}`).catch(console.error);

// Bot 命令
bot.onText(/\/start/, (msg) => {
  bot.sendMessage(msg.chat.id, '🎮 欢迎来到游戏Bot！\n/start - 开始\n/game - 游戏\n/help - 帮助');
});

bot.onText(/\/game/, (msg) => {
  bot.sendMessage(msg.chat.id, '🎯 游戏功能开发中...');
});

bot.onText(/\/help/, (msg) => {
  bot.sendMessage(msg.chat.id, '📖 /start 开始 | /game 游戏 | /help 帮助');
});

console.log('🤖 Bot initialized');
