from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def keyboard_main_button() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='Реакции')
    button_2 = KeyboardButton(text='Частота отправки сообщений в чат')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2]],
                                   resize_keyboard=True)
    return keyboard


def main_admin_mode() -> ReplyKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Ключевые слова', callback_data='key_word')
    button_2 = InlineKeyboardButton(text='Выбор эмодзи для реакций', callback_data='emodji')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1], [button_2]])
    return keyboard


def delete_add_key_word() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Удалить', callback_data='word_delete')
    button_2 = InlineKeyboardButton(text='Добавить', callback_data='word_add')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]])
    return keyboard
