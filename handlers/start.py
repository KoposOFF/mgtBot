# handlers/start.py
from aiogram import Router, F, types
from aiogram.types import CallbackQuery, Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.start_kb import start_kb

from keyboards.start_kb import get_register_kb
from database.db import get_user  # функция для получения пользователя


router = Router()

# @router.message(CommandStart())
# async def cmd_start(message: types.Message):
#         await message.answer(text="Привет! Я бот. 😊", reply_markup=start_kb)

@router.callback_query(F.data == "start")
async def handle_start_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=start_kb)  # Удаляем старую клавиатуру

    user_id = callback.from_user.id
    user = await get_user(user_id)

    if user:
        text = f"👤 Вы уже зарегистрированы:\n\n" \
               f"Имя: {user['name']}\n" \
               f"Табельный номер: {user['employee_id']}"
        await callback.message.answer(text)
    else:
        await callback.message.answer(
            "Добро пожаловать! 👋\nВы не зарегистрированы.",
            reply_markup=get_register_kb()
        )
