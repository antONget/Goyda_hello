from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from filters.admin_filter import IsSuperAdmin
from config_data.config import Config, load_config
from utils.error_handling import error_handler
from keyboards.admin_mode_keyboard import main_admin_mode, delete_add_key_word
from database.requests_key_words import add_key_word, select_key_words, delete_key_word

import logging


config: Config = load_config()
router = Router()
router.message.filter(F.chat.type == "private")


class Word(StatesGroup):
    add_word = State()
    delete_word = State()


@router.message(IsSuperAdmin(), CommandStart)
@error_handler
async def admin_mode(message: Message, bot: Bot):
    logging.info(f'admin_mode')
    await message.answer(text='Выберите раздел',
                         reply_markup=main_admin_mode())


@router.message(IsSuperAdmin(), F.text == 'Ключевые слова')
@error_handler
async def admin_mode(message: Message, bot: Bot):
    logging.info(f'admin_mode')
    await message.answer(text='Добавить или  удалить ключевое слово?',
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
            text += f'{i+1}. {word}\n'
        await callback.message.edit_text(text='Пришлите номер ключевого слова для удаления')
        await state.set_state(Word.delete_word)
    await callback.answer()


@router.message(IsSuperAdmin(), StateFilter(Word.add_word), F.text)
@error_handler
async def add_word(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'add_word')
    if message.text in ['Ключевые слова', 'Выбор эмодзи для реакций']:
        await message.answer(text='Операция прервана...')
        return
    await add_key_word(word=message.text)
    await message.answer(text=f'Ключевое слово {message.text} успешно добавлено в список')
    await state.set_state(state=None)


@router.message(IsSuperAdmin(), StateFilter(Word.delete_word), F.text)
@error_handler
async def delete_word(message: Message, state: FSMContext, bot: Bot):
    logging.info(f'delete_word')
    if message.text in ['Ключевые слова', 'Выбор эмодзи для реакций']:
        await message.answer(text='Операция прервана...')
        return
    if message.text.isdigit():
        list_key_word = await select_key_words()
        for i, word in enumerate(list_key_word):
            if int(message.text) == i + 1:
                await delete_key_word(id_word=i)
                await message.answer(text=f'Ключевое слово {word.word} успешно удалено')
                break
        await state.set_state(state=None)
    else:
        await message.answer(text='Некорректно указано число')
