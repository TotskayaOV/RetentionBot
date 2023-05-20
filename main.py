from aiogram import executor
from view import dp
from loader import user_db, call_db, air_db, comm_db
import middleware


async def on_start(_):
    try:
        user_db.create_table_users()
        user_db.create_table_users_contacts()
        call_db.create_table_call()
        call_db.create_table_working_day()
        air_db.create_table_airtable_status()
        air_db.create_table_airtable_comments()
        air_db.create_table_recorded_leads()
        comm_db.create_table_comments()
        comm_db.create_table_results()
        print('DB connection.. OK')
    except IOError:
        print('DB connection... FAILURE!!!')
    print('Бот запущен!')


if __name__ == '__main__':
    middleware.setup(dp)
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_start)
