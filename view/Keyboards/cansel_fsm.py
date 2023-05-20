from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_cancel_fsm = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_cancel = KeyboardButton(text='Отмена')

kb_cancel_fsm.add(btn_cancel)
