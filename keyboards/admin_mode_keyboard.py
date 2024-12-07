from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


def main_admin_mode() -> ReplyKeyboardMarkup:
    button_1 = KeyboardButton(text='Ключевые слова')
    button_2 = KeyboardButton(text='Выбор эмодзи для реакций')
    keyboard = ReplyKeyboardMarkup(keyboard=[[button_1], [button_2]],
                                   resize_keyboard=True)
    return keyboard


def delete_add_key_word() -> InlineKeyboardMarkup:
    button_1 = InlineKeyboardButton(text='Удалить', callback_data='word_delete')
    button_2 = InlineKeyboardButton(text='Добавить', callback_data='word_add')
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button_1, button_2]])
    return keyboard
