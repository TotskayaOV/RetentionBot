import sqlite3

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from loader import dp, user_db, admin_id
from aiogram.types import Message
from view.Keyboards import kb_cancel_fsm


class UpdContact(StatesGroup):
    user_name = State()
    user_update = State()



@dp.message_handler(commands=['upd_contact'], state=None)
async def upd_user(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        await message.answer(text='Введите Фамилию)', reply_markup=kb_cancel_fsm)
        await UpdContact.user_name.set()
    else:
        await message.answer('У вас нет доступа к этой функции')


@dp.message_handler(state=UpdContact.user_name)
async def user_id_up_catch(message: Message, state: FSMContext):
    user_name = message.text
    await state.update_data({'user_name': user_name})
    check = user_db.get_the_user(name=user_name)
    if check:
        user_id = check[0]
        check_contacts = user_db.get_the_contact(fk_users=user_id)
        if check_contacts:
            await message.answer(text=f'У данного пользователя уже записаны контакты')
            data = await state.get_data()
            await state.reset_data()
            await state.finish()
        else:
            await state.update_data({'user_name': user_id})
            await message.answer(text='Введите tg id (только цифры)', reply_markup=kb_cancel_fsm)
            await UpdContact.user_update.set()
    else:
        await message.answer(text='Такой пользователь не записан в Базу данных.'
                                  ' Зарегистрируйте пользователя /upd_user')
        data = await state.get_data()
        await state.reset_data()
        await state.finish()


@dp.message_handler(state=UpdContact.user_update)
async def name_catch(message: Message, state: FSMContext):
    await state.update_data({'user_update': message.text})
    data = await state.get_data()
    try:
        user_db.add_contacts({'fk_users': data.get('user_name'), 'tg_id': data.get('user_update')})
        await message.answer(f"tg id добавлен")
    except sqlite3.OperationalError:
        await message.answer("Ошибка добавления роли пользователю! Проверьте правильность вводимых данных",
                             reply_markup=kb_cancel_fsm)
    await state.reset_data()
    await state.finish()



