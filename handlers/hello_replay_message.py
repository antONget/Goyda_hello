from aiogram import Router, Bot
from aiogram.types import Message
from filters.groups_chat import IsGroup
from config_data.config import Config, load_config
from utils.error_handling import error_handler

import logging


config: Config = load_config()
router = Router()


@router.message(IsGroup())
@error_handler
async def check_messages(message: Message, bot: Bot):
    logging.info(f'check_messages {message.message_thread_id} {message.chat.id}')
    if message.text == 'Гойда':
        await message.answer(text='Гойда')


@error_handler
async def scheduler_messages(bot: Bot):
    logging.info(f'scheduler_messages')
    await bot.send_message(chat_id=config.tg_bot.group_id,
                           text='Гойда')
