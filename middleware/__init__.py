from aiogram import Dispatcher
from .mw import AddUserRole


def setup(dp: Dispatcher):
    dp.middleware.setup(AddUserRole())
