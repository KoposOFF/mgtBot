# handlers/bus_list.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from database.db import get_bus
from keyboards.start_kb import menu_kb

router = Router()

# Шаги FSM
class BusForm(StatesGroup):
    waiting_for_bus_number = State()

@router.message(F.text == "Сделать запись")
async def ask_bus_number(message: Message, state: FSMContext):
    await message.answer("Введите номер автобуса (последние 4 цифры): ")
    await state.set_state(BusForm.waiting_for_bus_number)

@router.message(BusForm.waiting_for_bus_number)
async def process_bus_number(message: Message, state: FSMContext):
    if not message.text.isdigit() and len(message.text) != 4:
        return await message.answer("Номер должен состоять из 4 цифр. Попробуйте снова.")

    bus_number = int("19" + message.text)
    
    await get_bus(bus_number)
    await message.answer(f"Автобус : {bus_number} внесен в список")
    
    await state.clear()