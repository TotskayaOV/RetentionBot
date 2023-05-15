from aiogram import executor
from view import dp
from loader import user_db, call_db
import middleware


async def on_start(_):
    try:
        user_db.create_table_users()
        user_db.create_table_users_contacts()
        call_db.create_table_call()
        call_db.create_table_working_day()
        print('DB connection.. OK')
    except IOError:
        print('DB connection... FAILURE!!!')
    print('Бот запущен!')


if __name__ == '__main__':
    middleware.setup(dp)
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_start)
