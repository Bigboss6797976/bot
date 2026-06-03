const express = require('express');
const TelegramBot = require('node-telegram-bot-api');

const TOKEN = process.env.BOT_TOKEN || '8942563997:AAF96376-_N-Lk57R6XvIUwDw0_ZB_5qfzA';
const PORT = process.env.PORT || 3000;

const app = express();
app.use(express.json());

const bot = new TelegramBot(TOKEN, { webHook: { port: PORT } });

app.post(`/bot${TOKEN}`, (req, res) => {
  bot.processUpdate(req.body);
  res.sendStatus(200);
});

app.get('/', (req, res) => {
  res.send('✅ Telegram Game Bot is running!');
});

app.listen(PORT, () => {
  console.log(`🚀 Bot on port ${PORT}`);
});

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
