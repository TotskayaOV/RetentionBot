import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, admin_id, user_db
from aiogram.types import Message
from view.Keyboards import kb_role_user, kb_cancel_fsm


class UpdUser(StatesGroup):
    user_name = State()
    user_update = State()
    user_role = State()


@dp.message_handler(commands=['upd_user'], state=None)
async def upd_user(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Введите Фамилию)', reply_markup=kb_cancel_fsm)
        await UpdUser.user_name.set()
    else:
        await message.answer('У вас нет доступа к этой функции')


@dp.message_handler(state=UpdUser.user_name)
async def user_id_up_catch(message: Message, state: FSMContext):
    user_name = message.text
    await state.update_data({'user_name': user_name})
    check = user_db.get_the_user(name=user_name)
    if check:
        await message.answer(text=f'Такой пользователь уже записан в роли {check[2]}. Выберите новый статус',
                             reply_markup=kb_role_user)
        await UpdUser.user_update.set()
    else:
        await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)
        await UpdUser.user_role.set()

@dp.message_handler(state=UpdUser.user_update)
async def name_catch(message: Message, state: FSMContext):
    if message.text in ['admin', 'operator', 'deactivated']:
        await state.update_data({'user_role': message.text})
        data = await state.get_data()
        check = user_db.get_the_user(name=data.get('user_name'))
        try:
            user_db.update_user_status({'id': check[0], 'status': data.get('user_role')})
            await message.answer(f"Пользователь {data.get('user_name')} обновлен в роли {data.get('user_role')}")
        except sqlite3.OperationalError:
            await message.answer("Ошибка добавления роли пользователю! Проверьте правильность вводимых данных",
                                 reply_markup=kb_cancel_fsm)
        await state.reset_data()
        await state.finish()
    else:
        await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)


@dp.message_handler(state=UpdUser.user_role)
async def name_catch(message: Message, state: FSMContext):
    if message.text in ['admin', 'operator', 'deactivated']:
        await state.update_data({'user_role': message.text})
        data = await state.get_data()
        try:
            user_db.add_user({'name': data.get('user_name'), 'status': data.get('user_role')})
            await message.answer(f"Пользователь {data.get('user_name')} добавлен в роли {data.get('user_role')}")
        except sqlite3.OperationalError:
            await message.answer("Ошибка добавления роли пользователю! Проверьте правильность вводимых данных",
                                 reply_markup=kb_cancel_fsm)
        await state.reset_data()
        await state.finish()
    else:
        await message.answer(text='Выберите роль пользователя', reply_markup=kb_role_user)
