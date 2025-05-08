from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Регистрация")]
    ],
    resize_keyboard=True
)

menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Посмотреть автобус")],
        [KeyboardButton(text="Сделать запись")],
    ],
    resize_keyboard=True
)

