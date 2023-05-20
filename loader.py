import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from modul import User, Call, Airtable, Comment
# from sending_messages import notify


memory = MemoryStorage()

bot = Bot(os.getenv('TOKEN'))
admin_id = (os.getenv('ADMIN_ID'))
dp = Dispatcher(bot, storage=memory)
user_db = User()
call_db = Call()
air_db = Airtable()
comm_db = Comment()
# log_id = os.getenv('LOG_ID')
# admin_id = os.getenv('ADMIN_ID')


