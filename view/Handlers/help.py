from loader import dp
from aiogram.types import Message


@dp.message_handler(commands=['help'])
async def mes_start(message: Message, admin: bool):
    if admin:
        await message.answer(f'Привет:\nДля загрузки новых файлов нажми /update_data\n'
                             f'Для получния сводных данных нажми /show_res\n'
                             f'Для добавления нового пользователя нажми /upd_user\n'
                             f'Для добавления tg id пользователю /upd_contact')