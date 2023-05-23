from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

from loader import dp, air_db, call_db
from view.Keyboards import kb_cancel_fsm, create_kb_name_files




class KillFiles(StatesGroup):
    general_date = State()


@dp.message_handler(commands=['kill_data'], state=None)
async def add_date(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await KillFiles.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=KillFiles.general_date, content_types=ContentTypes.ANY)
async def general_date_record(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        date_update = datetime.strptime(data_obj, '%Y-%m-%d').date()
        await message.answer(text=f'Для удаления данных задана дата: {data_obj}.')
        check_raise = air_db.get_airtable_status(date=date_update)
        print(check_raise)
        air_db.remove_airtable_status(date_update)
        air_db.remove_airtable_comment(date_update)
        air_db.remove_recorded_leads(date_update)
        call_db.remove_call(date_update)
        call_db.remove_working_day(date_update)
        await message.answer(text=f'Данные за {data_obj} удалены.')
        await state.reset_data()
        await state.finish()
    except:
        await message.answer(text='Ошибка ввода даты')
        await state.reset_data()
        await state.finish()
