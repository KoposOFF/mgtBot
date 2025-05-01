# states/register.py
from aiogram.fsm.state import StatesGroup, State

class Register(StatesGroup):
    name = State()
    employee_id = State()
