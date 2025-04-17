from aiogram.fsm.state import StatesGroup, State



class MenuState(StatesGroup):
    menu = State()

class Subscribe(StatesGroup):
    subscribe = State()

class Meassage(StatesGroup):
    new_word = State()
    caption = State()
    video = State()
    code = State()


