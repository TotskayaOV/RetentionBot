import os
import sqlite3

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from modul import User, Call
# from sending_messages import notify


memory = MemoryStorage()

bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=memory)
user_db = User()
call_db = Call()
# log_id = os.getenv('LOG_ID')
# admin_id = os.getenv('ADMIN_ID')


