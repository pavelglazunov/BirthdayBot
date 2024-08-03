from aiogram.fsm.state import State, StatesGroup


class BirthdayState(StatesGroup):
    data = State()
