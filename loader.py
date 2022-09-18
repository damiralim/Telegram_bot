from telebot import TeleBot
from config import TOKEN
from telebot.storage import StateMemoryStorage
from loguru import logger

logger.add('debug.log', format='{time} {level} {message}', level='DEBUG')
storage = StateMemoryStorage()
bot = TeleBot(token=TOKEN, state_storage=storage)
