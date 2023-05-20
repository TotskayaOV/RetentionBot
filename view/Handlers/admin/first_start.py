import os
from datetime import datetime
from loader import dp, comm_db, admin_id, air_db
from aiogram.types import Message, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
class FirstStart(StatesGroup):
    files_one = State()
@dp.message_handler(commands=['ferst_start'], state=None)
async def mes_start(message: Message, admin: bool):
    if admin or int(admin_id) == message.from_user.id:
        list_comments = ['Не выходит на связь более 3 дней', 'Нашел постоянную работу', 'Болезнь',
                         'Отказался озвучить причину', 'Было мало заказов', 'Взял перерыв больше месяца',
                         'Не хочет доставлять заказы (только сборка)', 'Поломка авто', 'Не было доступных слотов',
                         'Низкая оплата за заказ/позицию', 'Нет потребности', 'Не успевает подрабатывать из-за учебы',
                         'Не успевает подрабатывать из-за основной работы', 'Не хочет собирать заказы (только доставка)',
                         'Нет ЛМК', 'Далеко добираться', 'Отпала необходимость в подработке', 'Не устраивает функционал',
                         'Временный переезд в другой город', 'Не устраивают условия тарифа', 'Нет Android',
                         'Мобилизация', 'Большой радиус доставки', 'Не мог выйти в короткие смены', 'Штрафы',
                         'Большой вес заказов', 'Нашел работу по специальности', 'Конфликт с супервайзером', 'Отпуск',
                         'Не справляется с функционалом']
        list_results = ['Направлен на обучение впервые', 'Записан на смену впервые', 'Направлен на обучение',
                        'Записан на смену', 'Перезвонить авто', 'Нет потребности', 'Отказ', 'НДЗ авто',
                        'Перезвонить вручную', 'НДЗ вручную', 'Вышел', 'Внешний', 'Самоотказ',
                        'Не прекращал сотрудничество']
        for i in range(0, len(list_comments)):
            comm_db.add_comments(list_comments[i])
        for y in range(0, len(list_results)):
            comm_db.add_results(list_results[y])
        set_comm = comm_db.get_comments()
        str_comm = ''
        for elem in set_comm:
            str_comm += f"{elem[0]} - {elem[1]}"
        await message.answer(text=str_comm)
        set_result = comm_db.get_results()
        str_res = ''
        for elem in set_result:
            str_res += f"{elem[0]} - {elem[1]}\n"
        await message.answer(text=str_res)
        await message.answer(text='Загрузите файл')
        await FirstStart.files_one.set()

@dp.message_handler(state=FirstStart.files_one, content_types=ContentTypes.ANY)
async def work_record(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'files_one': True})
        await message.answer(text='Файл загружен')
        await document.download(destination_file=f'./cred/{document.file_name}')
        os.rename(f'./cred/{document.file_name}', './cred/upd.csv')
        try:
            path = './cred/upd.csv'
            with open(path, 'r', encoding='UTF-8') as file:
                my_list = file.readlines()
                working_list = []
                for line in range(1, len(my_list)):
                    temp_string = my_list[line]
                    temp_string2 = temp_string.rstrip("\n")
                    working_list.append(temp_string2.split(';'))
                date_update = datetime.strptime('2023-05-10', '%Y-%m-%d').date()
                for elem in working_list:
                    if elem[1] != 'Самотказ' and elem[1] != 'Отказ' and elem[1] != 'Вышел':
                        air_db.add_recorded_leads({'date': date_update, 'phone_number': elem[0]})
        except Exception as err:
            await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                      f'расширение, кодировку, формат данных. \n'
                                      f'Или передайте данные об ошибке: {err}')
            await state.reset_data()
            await state.finish()
        else:
            await message.answer(text='Данные Airtable загружены')
        finally:
            try:
                os.remove('./cred/upd.csv')
                await state.reset_data()
                await state.finish()
            except Exception as err:
                await message.answer(text=f'Ошибка удаления файлов: {err}')
                await state.reset_data()
                await state.finish()
