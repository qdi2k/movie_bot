from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, KeyboardButton)


find_movie = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Найти')]
], resize_keyboard=True, input_field_placeholder='Найти интересующий фильм')

choice = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Сериал', callback_data='series'),
     InlineKeyboardButton(text='Фильм', callback_data='film')]
])
