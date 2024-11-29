import time
from config_data.config import Config, load_config
from aiogram import Bot
import logging
from utils.error_handling import error_handler

config: Config = load_config()


# Уведомление администраторам бота о том что Бот запущен
@error_handler
async def on_startup_notify(bot: Bot):
    logging.info('on_startup_notify')
    date_now = time.strftime("%Y-%m-%d", time.localtime())
    time_now = time.strftime("%H:%M:%S", time.localtime())
    text = (f"✅Бот запущен и готов к работе!✅\n"
            f"📅Дата: {date_now}\n"
            f"⏰Время: {time_now}")
    await bot.send_message(chat_id=config.tg_bot.support_id, text=text)
