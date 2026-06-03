import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from config import BOT_TOKEN
from handlers import start, menu

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# 注册命令
dp.register_message_handler(start.cmd_start, commands=['start'])

# 注册回调查询
dp.register_callback_query_handler(menu.handle_callbacks, lambda c: True)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
