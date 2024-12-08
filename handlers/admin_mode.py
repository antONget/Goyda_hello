from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from filters.admin_filter import IsSuperAdmin
from config_data.config import Config, load_config
from utils.error_handling import error_handler
from keyboards.admin_mode_keyboard import keyboard_main_button, main_admin_mode, delete_add_key_word
from database.requests_key_words import add_key_word, select_key_words, delete_key_word, add_emodji, add_time, select_emodji

import logging
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.schedulers.background import BackgroundScheduler

config: Config = load_config()
router = Router()
router.message.filter(F.chat.type == "private")


class Word(StatesGroup):
    add_word = State()
    delete_word = State()
    emodji = State()
    time_state = State()


@router.message(IsSuperAdmin(), CommandStart())
@error_handler
async def admin_mode(message: Message, bot: Bot):
    logging.info(f'admin_mode')
    await message.answer(text='Выберите раздел',
                         reply_markup=keyboard_main_button())


@router.message(IsSuperAdmin(), F.text == 'Реакции')
@error_handler
async def process_reaction(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'process_reaction')
    await message.answer(text='Выберите раздел',
                         reply_markup=main_admin_mode())


@router.callback_query(F.data == 'key_word')
@error_handler
async def admin_mode(callback: CallbackQuery, bot: Bot):
    logging.info(f'admin_mode')
    await callback.message.edit_text(text='Добавить или  удалить ключевое слово?',
                                     reply_markup=delete_add_key_word())


@router.callback_query(F.data.startswith('word'))
@error_handler
async def process_word(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info(f'process_word {callback.message.chat.id}')
    answer = callback.data.split('_')[-1]
    if answer == 'add':
        await callback.message.edit_text(text='Пришлите слово для добавления в список слов на которые бот будет'
                                              ' ставить реакции',
                                         reply_markup=None)
        await state.set_state(Word.add_word)
    elif answer == 'delete':
        list_key_word = await select_key_words()
        text = '<b>Список ключевых слов:</b>\n\n'
        for i, word in enumerate(list_key_word):
            text += f'{i+1}. {word.word}\n'
        await callback.message.edit_text(text=f'Пришлите номер ключевого слова для удаления\n\n {text}')
        await state.set_state(Word.delete_word)
    await callback.answer()


@router.message(IsSuperAdmin(), StateFilter(Word.add_word), F.text)
@error_handler
async def add_word(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'add_word')
    if message.text in ['Реакции', 'Частота отправки сообщений в чат']:
        await message.answer(text='Операция прервана...')
        return
    dict_data = {'word': message.text}
    await add_key_word(data=dict_data)
    await message.answer(text=f'Ключевое слово <i>{message.text}</i> успешно добавлено в список')
    await state.set_state(state=None)


@router.message(IsSuperAdmin(), StateFilter(Word.delete_word), F.text)
@error_handler
async def delete_word(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'delete_word')
    if message.text in ['Реакции', 'Частота отправки сообщений в чат']:
        await message.answer(text='Операция прервана...')
        return
    if message.text.isdigit():
        list_key_word = await select_key_words()
        for i, word in enumerate(list_key_word):
            if int(message.text) == i + 1:
                await delete_key_word(id_word=i)
                await message.answer(text=f'Ключевое слово <i>{word.word}</i> успешно удалено')
                break
        await state.set_state(state=None)
    else:
        await message.answer(text='Некорректно указано число')


@router.callback_query(F.data == 'emodji')
@error_handler
async def admin_mode_emodji(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logging.info(f'admin_mode_emodji')
    await callback.message.edit_text(text='Пришлите эмодзи для реакций')
    await state.set_state(Word.emodji)


@router.message(IsSuperAdmin(), StateFilter(Word.emodji), F.text)
@error_handler
async def delete_word(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'delete_word')
    if message.text in ['Реакции', 'Частота отправки сообщений в чат']:
        await message.answer(text='Операция прервана...')
        return
    data = {'emodji': message.text}
    await add_emodji(data=data)
    await message.answer(text=f'Эмодзи {message.text} успешно добавлен')


@router.message(IsSuperAdmin(), F.text == 'Частота отправки сообщений в чат')
@error_handler
async def process_reaction(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'process_time')
    await message.answer(text='Раздел в разработке')
    return
    # await message.answer(text='Пришлите время для отправки сообщения, в минутах')
    # await state.set_state(Word.time_state)


@router.message(IsSuperAdmin(), StateFilter(Word.time_state), F.text)
@error_handler
async def delete_word(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'delete_word')
    if message.text in ['Реакции', 'Частота отправки сообщений в чат']:
        await message.answer(text='Операция прервана...')
        return
    if message.text.isdigit():
        data_time = {'time': int(message.text)}
        await add_time(data=data_time)
        await message.answer(text=f'Время таймера успешно изменено на {message.text} минут')
        interval: str = f'*/{int(message.text)}'
        scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
        scheduler.reschedule_job(job_id='my_job_id', trigger='cron', minute=interval)
        await state.set_state(state=None)
    else:
        await message.answer(text='Некорректно указано число')


async def alert_user_sub(bot: Bot, time_interval: int = 15):
    while True:
        await asyncio.sleep(time_interval * 60)
        msg = await bot.send_message(chat_id=config.tg_bot.group_id,
                                     text='Гойда')
        emodji = await select_emodji()
        await bot.set_message_reaction(chat_id=msg.chat.id,
                                       message_id=msg.message_id,
                                       reaction=[{"type": "emoji", "emoji": emodji.emodji}])