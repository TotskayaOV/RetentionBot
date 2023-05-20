from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import call_db, air_db
from view.Keyboards.inline import filenames_data


def create_kb_name_files(date_update):
    kb_name_files = InlineKeyboardMarkup(row_width=2)
    airtable_check = air_db.get_airtable_status(date=date_update)
    call_check = call_db.get_call(date=date_update)
    work_check = call_db.get_working_day(date=date_update)
    btn_airtable = InlineKeyboardButton(text='Airtable', callback_data=filenames_data.new(files_name='airF'))
    btn_call = InlineKeyboardButton(text='История звонков', callback_data=filenames_data.new(files_name='callF'))
    btn_work = InlineKeyboardButton(text='Рабочий день', callback_data=filenames_data.new(files_name='workF'))
    btn_metabase = InlineKeyboardButton(text='Metabase', callback_data=filenames_data.new(files_name='metaF'))
    if len(airtable_check) == 0:
        kb_name_files.add(btn_airtable)
    if len(call_check) == 0:
        kb_name_files.add(btn_call)
    if len(work_check) == 0:
        kb_name_files.add(btn_work)
    kb_name_files.add(btn_metabase)
    return kb_name_files


