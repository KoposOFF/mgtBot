# handlers/register.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from states.register import RegisterState
from database.db import add_user, get_user_dict
from keyboards.start_kb import start_kb, menu_kb  # кнопка с "Регистрация"

router = Router()

@router.message(CommandStart())
async def str_cmd(message: Message):
    await message.answer("<b>Привет!</b>\nЗдесь ты можешь проверить свой автобус\nТакже вносить измения,если что-то изменилось 😊",
                         parse_mode="HTML", reply_markup=start_kb)


@router.message(F.text == "Регистрация")
async def start_register(message: Message, state: FSMContext):
    user_data = await get_user_dict(message.from_user.id)

    if user_data:
        await message.answer(
            "📝 Вы уже зарегистрированы!\n"
            f"Имя: {user_data['name']}\n"
            f"Табельный номер: {user_data['table_id']}",
            reply_markup=menu_kb
            )                  # Здесь докинуть клавиатуру
        return
    
    await message.answer("Введите ваше имя:")
    await state.set_state(RegisterState.name)

@router.message(RegisterState.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш табельный номер (последние 4 цифры):")
    await state.set_state(RegisterState.table_id)

@router.message(RegisterState.table_id)
async def process_employee_id(message: Message, state: FSMContext):
    if not message.text.isdigit() and len(message.text) != 4:
        return await message.answer("Табельный номер должен быть числом. Попробуйте снова.")
    
    data = await state.get_data()
    name = data["name"]
    table_id = int("1910" + message.text)
    telegram_id = message.from_user.id

    await add_user(telegram_id, name, table_id)


    await message.answer(f"✅ Регистрация завершена!\nИмя: {name}\nТабельный: {table_id}",
                         reply_markup=menu_kb)
    await state.clear()
