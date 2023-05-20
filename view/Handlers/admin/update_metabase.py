from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message, ContentTypes, Document, CallbackQuery
from datetime import datetime

import os
from loader import dp
from controller import writing_went_on_shift
from view.Keyboards import kb_cancel_fsm, create_kb_name_files, filenames_data



class NewMeta(StatesGroup):
    upload_file = State()


@dp.callback_query_handler(filenames_data.filter(files_name='metaF'), state=None)
async def call_catch(callback: CallbackQuery, state: FSMContext):
    chat_id = callback.from_user.id
    await dp.bot.send_message(chat_id, text='Загрузите файл metabase', reply_markup=kb_cancel_fsm)
    await NewMeta.next()

@dp.message_handler(state=NewMeta.upload_file, content_types=ContentTypes.ANY)
async def call_record(message: Message, state: FSMContext):
    if document := message.document:
        await state.update_data({'upload_file': True})
        await document.download(destination_file=f'./cred/{document.file_name}')
        try:
            os.rename(f'./cred/{document.file_name}', './cred/metabase.csv')
        except:
            os.remove('./cred/metabase.csv')
            os.rename(f'./cred/{document.file_name}', './cred/metabase.csv')
        finally:
            try:
                writing_went_on_shift()
            except Exception as err:
                await message.answer(text=f'Ошибка загрузки данных. Проверьте файл:'
                                          f'расширение, кодировку, формат данных. \n'
                                          f'Или передайте данные об ошибке: {err}')
                await state.reset_data()
                await state.finish()
            else:
                await message.answer(text='Данные загружены', reply_markup=kb_cancel_fsm)
            finally:
                try:
                    os.remove('./cred/metabase.csv')
                    await state.reset_data()
                    await state.finish()
                except Exception as err:
                    await message.answer(text=f'Ошибка удаления файлов: {err}')
                    await state.reset_data()
                    await state.finish()



