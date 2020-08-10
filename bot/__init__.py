from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import ujson
from defs import get_from_config


API_TOKEN = get_from_config('apikey')

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

db_path = get_from_config('db_path')


from bot import modules
