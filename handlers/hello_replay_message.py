from aiogram import Router, Bot, F
from aiogram.types import Message
from filters.groups_chat import IsGroup
from config_data.config import Config, load_config
from utils.error_handling import error_handler
from database.requests_key_words import select_key_words, select_emodji

import logging


config: Config = load_config()
router = Router()


@router.message(IsGroup(), F.text)
@error_handler
async def check_messages(message: Message, bot: Bot):
    logging.info(f'check_messages {message.message_thread_id} {message.chat.id}')
    if message.text.lower() == 'гойда':
        msg = await message.answer(text='Гойда')
        emodji = await select_emodji()
        await bot.set_message_reaction(chat_id=message.chat.id,
                                       message_id=msg.message_id,
                                       reaction=[{"type": "emoji", "emoji": emodji.emodji}])
    list_key_words = await select_key_words()
    list_key_lower = [word.word.lower() for word in list_key_words]
    if message.text.lower() in list_key_lower:
        emodji = await select_emodji()
        await bot.set_message_reaction(chat_id=message.chat.id,
                                       message_id=message.message_id,
                                       reaction=[{"type": "emoji", "emoji": emodji.emodji}])


@error_handler
async def scheduler_messages(bot: Bot):
    logging.info(f'scheduler_messages')
    msg = await bot.send_message(chat_id=config.tg_bot.group_id,
                                 text='Гойда')
    emodji = await select_emodji()
    await bot.set_message_reaction(chat_id=msg.chat.id,
                                   message_id=msg.message_id,
                                   reaction=[{"type": "emoji", "emoji": emodji.emodji}])
