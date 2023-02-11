from telebot import TeleBot, StateMemoryStorage
from config import TOKEN
from loguru import logger

''' Запуск логирования и инициализация бота '''

logger.add('debug.log', format='{time} {level} {message}', level='DEBUG')
storage = StateMemoryStorage()
bot = TeleBot(token=TOKEN, state_storage=storage)
