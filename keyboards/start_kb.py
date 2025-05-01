# keyboards/start_kb.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🚀 Старт", callback_data="start")],
    [InlineKeyboardButton(text="📝 Регистрация", callback_data="register")]
])
