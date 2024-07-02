from aiogram.fsm.state import StatesGroup, State


class FsmStates(StatesGroup):
    TECH_PROB = State()
    COLLAB_PROB = State()
    COMPLAINT_PROB = State()