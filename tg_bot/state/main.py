from aiogram.fsm.state import StatesGroup, State



class MenuState(StatesGroup):
    menu = State()

class Subscribe(StatesGroup):
    subscribe = State()

class Meassage(StatesGroup):
    create_chan_ha = State()
    delete_chan_ha = State()
    delete_vid_ha = State()
    new_word = State()
    caption = State()
    video = State()
    code = State()


