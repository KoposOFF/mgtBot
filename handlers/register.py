# handlers/register.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.register import Register

router = Router()

@router.message(F.text.lower() == "регистрация")
async def start_register(message: Message, state: FSMContext):
    await message.answer("Введите ваше имя:")
    await state.set_state(Register.name)

@router.message(Register.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш табельный номер:")
    await state.set_state(Register.employee_id)

@router.message(Register.employee_id)
async def process_employee_id(message: Message, state: FSMContext):
    await state.update_data(employee_id=message.text)
    data = await state.get_data()
    await message.answer(
        f"✅ Регистрация завершена!\n\n"
        f"👤 Имя: {data['name']}\n"
        f"🆔 Табельный номер: {data['employee_id']}"
    )
    await state.clear()
