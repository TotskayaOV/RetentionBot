from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_activ_deactiv = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_activ = KeyboardButton(text='active')
btn_deactiv = KeyboardButton(text='inactive')


kb_activ_deactiv.add(btn_activ, btn_deactiv)
