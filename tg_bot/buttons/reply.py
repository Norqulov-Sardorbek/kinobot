from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from tg_bot.buttons.text import *
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def admin_btn():
    keyboard1 = KeyboardButton(text = movies_text)
    keyboard2 = KeyboardButton(text = chanels)
    keyboard3 = KeyboardButton(text=message_to_bot)
    keyboard4 = KeyboardButton(text=magic_word)

    design = [[keyboard1, keyboard2],
              [keyboard3, keyboard4]]
    return ReplyKeyboardMarkup(keyboard=design ,
                               resize_keyboard=True)
def movies():
    keyboard1 = KeyboardButton(text = create)
    keyboard2 = KeyboardButton(text = delete)
    design = [[keyboard1, keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design,resize_keyboard=True)
def chanels_btn():
    keyboard1 = KeyboardButton(text = create_chan)
    keyboard2 = KeyboardButton(text = delete_chan)
    design = [[keyboard1, keyboard2]]
    return ReplyKeyboardMarkup(keyboard=design,resize_keyboard=True)

def menu_back():
    keyboard3=KeyboardButton(text=menuga)
    design=[[keyboard3]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)

def back():
    keyboard1 = KeyboardButton(text = ortga)
    design = [[keyboard1]]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)

