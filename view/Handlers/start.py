from loader import dp
from aiogram.types import Message
from controller import writing_call_data
from datetime import datetime, date

@dp.message_handler(commands=['start'])
async def mes_start(message: Message):
    user_id = message.from_user.id
    data_obj = '13.05.2023'
    up_data = datetime.strptime(data_obj, '%d.%m.%Y').date()
    print(up_data)
    writing_call_data(up_data)
    await message.answer(f'Привет, твой id {user_id}.'
                         f' Передай его администратору для дальнейшей работы с ботом 😇')
