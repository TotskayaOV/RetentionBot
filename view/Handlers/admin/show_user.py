from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

from loader import dp, user_db
from view.Keyboards import kb_cancel_fsm
from view.sting_building import string_all_result
from controller import show_full_data_db


class ShowUserS(StatesGroup):
    general_date = State()


@dp.message_handler(commands=['show_us'], state=None)
async def add_date(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите', reply_markup=kb_cancel_fsm)
        await ShowUserS.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=ShowUserS.general_date, content_types=ContentTypes.ANY)
async def general_date_record(message: Message, state: FSMContext):
    # try:
        await message.answer(text=f'Пользователи:')
        text = show_full_data_db(user_db.get_user)
        await message.answer(text=text)
        await state.reset_data()
        await state.finish()