""" Клавиатура для отправки и отмены сообщения. """
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

_button_send = KeyboardButton('/send')
_button_cancel = KeyboardButton('/cancel')
markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

markup.add(_button_send).add(_button_cancel)
