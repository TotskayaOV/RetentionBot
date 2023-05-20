from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

import os
from loader import dp
from controller import writing_work_data
from view.Keyboards import kb_cancel_fsm, create_kb_name_files, filenames_data



class NewWork(StatesGroup):
    general_date = State()
    upload_file = State()



@dp.callback_query_handler(filenames_data.filter(files_name='workF'), state=None)
async def work_catch(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    await dp.bot.send_message(chat_id, text='Напишите дату в формате 2023-01-31', reply_markup=kb_cancel_fsm)
    await NewWork.next()

@dp.message_handler(state=NewWork.general_date, content_types=ContentTypes.ANY)
async def work_date_record(message: Message, state: FSMContext):
    try:
        data_obj = message.text
        date_update = datetime.strptime(data_obj, '%Y-%m-%d').date()
        await state.update_data({'general_date': date_update})
        await message.answer(text=f'Для загрузки файлов задана дата: {data_obj}.\nЗагрузите файл с рабочими данными')
        await NewWork.next()
    except:
        await message.answer(text='Ошибка ввода даты')


@dp.message_handler(state=NewWork.upload_file, content_types=ContentTypes.ANY)
async def work_record(message: Message, state: FSMContext):
    if document := message.document:
        data_update = await state.get_data()
        date_update = data_update.get('general_date')
        await state.update_data({'upload_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/work_time.csv')
        except:
            os.remove('./cred/work_time.csv')
            os.rename(f'./cred/{document.file_name}', './cred/work_time.csv')
        finally:
            try:
                writing_work_data(date_update)
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                await message.answer(text='Рабочие данные загружены', reply_markup=create_kb_name_files(date_update))
            finally:
                try:
                    os.remove('./cred/work_time.csv')
                    await state.reset_data()
                    await state.finish()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()
