from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

from loader import dp, call_db
from view.Keyboards import kb_cancel_fsm
from view.sting_building import string_all_result
from controller import show_date_data_db


class ShowWork(StatesGroup):
    general_date = State()


@dp.message_handler(commands=['show_work'], state=None)
async def add_date(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await ShowWork.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=ShowWork.general_date, content_types=ContentTypes.ANY)
async def general_date_record(message: Message, state: FSMContext):
    # try:
        data_obj = message.text
        date_update = datetime.strptime(data_obj, '%Y-%m-%d').date()
        await message.answer(text=f'Данные за: {data_obj}.')
        text = show_date_data_db(call_db.get_working_day, date_update)
        await message.answer(text=text)
        await state.reset_data()
        await state.finish()