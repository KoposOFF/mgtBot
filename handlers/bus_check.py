# handlers/bus_check.py
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from database.db import get_bus_by_number, get_bus_reports

router = Router()

# Состояния FSM
class ViewBusFSM(StatesGroup):
    waiting_for_bus_number = State()

# Команда "Посмотреть автобус"
@router.message(F.text == "Посмотреть автобус")
async def ask_bus_number(message: Message, state: FSMContext):
    await message.answer("Введите последние 4 цифры номера автобуса:")
    await state.set_state(ViewBusFSM.waiting_for_bus_number)

# Обработка номера
@router.message(ViewBusFSM.waiting_for_bus_number)
async def show_bus_info(message: Message, state: FSMContext):
    if not message.text.isdigit() or len(message.text) != 4:
        return await message.answer("Номер должен состоять из 4 цифр.")
 
    bus_number = f"19{message.text}"

    bus = await get_bus_by_number(bus_number)
    if not bus:
        return await message.answer(f"Автобус с номером {bus_number} не найден.")

    reports = await get_bus_reports(bus["id"])
    if not reports:
        return await message.answer(f"По автобусу {bus_number} пока нет записей.")

    text = f"🚍 Автобус {bus_number}\n\n"
    for report in reports:
        date = report["datetime"]
        problems = report["problems"].replace(",", "\n- ") if report["problems"] else "-"
        pluses = report["pluses"].replace(",", "\n- ") if report["pluses"] else "-"

        text += f"📅 {date}\n"
        text += f"❌ Проблемы:\n- {problems}\n"
        text += f"✅ Плюсы:\n- {pluses}\n\n"

    await message.answer(text.strip())
    await state.clear()

