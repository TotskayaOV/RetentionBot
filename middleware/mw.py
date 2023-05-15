from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import user_db

class AddUserRole(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        try:
            user_set = user_db.get_the_contact(tg_id=message.from_user.id)
            next_user_set = user_db.get_the_user(id=user_set[0])
            user_role = list(next_user_set)[2]
            if user_role == 'admin':
                data['admin'] = True
            else:
                data['admin'] = False
            if user_role == 'coordinator':
                data['coordinator'] = True
            else:
                data['coordinator'] = False
        except:
            data['guest'] = True
            data['admin'] = False
            data['coordinator'] = False

    async def on_process_callback_query(self, call: CallbackQuery, data: dict):
        try:
            user_set = user_db.get_the_contact(tg_id=call.message.chat.id)
            next_user_set = user_db.get_the_user(id=user_set[0])
            user_role = list(next_user_set)[2]
            if user_role == 'admin':
                data['admin'] = True
            else:
                data['admin'] = False
            if user_role == 'coordinator':
                data['coordinator'] = True
            else:
                data['coordinator'] = False
        except:
            data['guest'] = True
            data['admin'] = False
            data['coordinator'] = False
        