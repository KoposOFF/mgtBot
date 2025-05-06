# handlers/register.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.register import RegisterState
from database.db import add_user
from keyboards.start_kb import start_kb  # кнопка с "Регистрация"

router = Router()

@router.message(F.text == "Регистрация")
async def start_register(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш табельный номер (число):")
    await state.set_state(RegisterState.employee_id)

@router.message(RegisterState.employee_id)
async def process_employee_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Табельный номер должен быть числом. Попробуйте снова.")
    
    data = await state.get_data()
    name = data["name"]
    employee_id = int(message.text)
    telegram_id = message.from_user.id

    await add_user(telegram_id, name, employee_id)

    await message.answer(f"✅ Регистрация завершена!\nИмя: {name}\nТабельный: {employee_id}",
                         reply_markup=None)
    await state.clear()
