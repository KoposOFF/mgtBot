# states/register_state.py
from aiogram.fsm.state import State, StatesGroup

class RegisterState(StatesGroup):
    name = State()
    employee_id = State()
