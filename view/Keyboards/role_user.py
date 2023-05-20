from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_role_user = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_admin = KeyboardButton(text='admin')
btn_oper = KeyboardButton(text='operator')
btn_deac = KeyboardButton(text='deactivated')

kb_role_user.add(btn_admin, btn_oper)
kb_role_user.add(btn_deac)
