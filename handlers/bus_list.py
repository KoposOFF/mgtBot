# handlers/bus_list.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from datetime import datetime

from database.db import get_bus, insert_bus_report
from keyboards.start_kb import menu_kb

router = Router()

# Шаги FSM
class BusForm(StatesGroup):
    waiting_for_bus_number = State()
    problem = State()
    advantages = State()

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
    await state.update_data(bus_number=bus_number)
    await message.answer("Опишите неисправности (через запятую):")
    await state.set_state(BusForm.problem)
    
@router.message(BusForm.problem)
async def enter_problem(message: Message, state: FSMContext):
    await state.update_data(problem=message.text)
    await message.answer("Укажите плюсы (через запятую):")
    await state.set_state(BusForm.advantages)


@router.message(BusForm.advantages)
async def enter_advantages(message: Message, state: FSMContext):
    data = await state.get_data()
    bus_number = data['bus_number']
    problem = data['problem']
    advantages = message.text
    created_at = datetime.now().isoformat(sep=' ', timespec='seconds')
    
    await insert_bus_report(
        bus_number=bus_number,
        problems=problem,
        pluses=advantages,
        datetime_str=created_at,
        submitted_by=message.from_user.id
    )


    await message.answer("Запись успешно добавлена ✅", reply_markup=menu_kb)
 
    await state.clear()