from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

from loader import dp
from view.Keyboards import kb_cancel_fsm, create_kb_name_files




class NewFiles(StatesGroup):
    general_date = State()


@dp.message_handler(commands=['update_data'], state=None)
async def add_date(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await NewFiles.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=NewFiles.general_date, content_types=ContentTypes.ANY)
async def general_date_record(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        date_update = datetime.strptime(data_obj, '%Y-%m-%d')
        await message.answer(text=f'Для загрузки файлов задана дата: {data_obj}.\nВыберите файл для загрузки',
                             reply_markup=create_kb_name_files((date_update)))
        await state.reset_data()
        await state.finish()
    except:
        await message.answer(text='Ошибка ввода даты')
        await state.reset_data()
        await state.finish()
