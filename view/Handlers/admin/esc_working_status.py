from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

from loader import dp, call_db
from view.Keyboards import kb_cancel_fsm, kb_activ_deactiv
from controller import check_work_in_data
from view.sting_building import string_all_result


class EscResult(StatesGroup):
    general_date = State()
    num_worker = State()
    new_status = State()


@dp.message_handler(commands=['esc_user'], state=None)
async def esc_date(message: Message, admin: bool):
    if admin:
        await message.answer(text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
        await EscResult.next()
    else:
        await message.answer('У вас нет доступа к этой функции')

@dp.message_handler(state=EscResult.general_date, content_types=ContentTypes.ANY)
async def general_date_record(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        date_update = datetime.strptime(data_obj, '%Y-%m-%d').date()
        await state.update_data({'general_date': date_update})
        await message.answer(text=check_work_in_data(date_update))
        await message.answer(text='Введите номер оператора, для которого нужно изменить статус')
        await EscResult.num_worker.set()
    except Exception as err:
        await message.answer(text=f'Ошибка ввода даты: {err}')

@dp.message_handler(state=EscResult.num_worker, content_types=ContentTypes.ANY)
async def general_date_record(message: Message, state: FSMContext):
    try:
        num_oper = message.text
        await state.update_data({'num_worker': num_oper})
        await message.answer(text='Выберите статус:', reply_markup=kb_activ_deactiv)
        await EscResult.new_status.set()
    except Exception as err:
        await message.answer(text=f'Ошибка: {err}')



@dp.message_handler(state=EscResult.new_status, content_types=ContentTypes.ANY)
async def update_status_record(message: Message, state: FSMContext):
    try:
        if message.text == 'inactive':
            data = await state.get_data()
            call_db.update_working_day_user({'activ_user': 1, 'user_fk': data.get('num_worker'),
                                         'date': data.get('general_date')})
        else:
            data = await state.get_data()
            call_db.update_working_day_user({'activ_user': 0, 'user_fk': data.get('num_worker'),
                                             'date': data.get('general_date')})
        await state.reset_data()
        await state.finish()
    except Exception as err:
        await message.answer(text=f'{err}')
        await state.reset_data()
        await state.finish()
