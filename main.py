from loader import bot
from loguru import logger
from telebot.types import Message, CallbackQuery
import handlers
from telebot.custom_filters import StateFilter, IsDigitFilter
from utils.set_bot_commands import set_default_commands
from database import connect_database

''' Запуск бота '''

if __name__ == '__main__':
    connect_database()                          # подключение к БД
    bot.add_custom_filter(StateFilter(bot))     # загрузка фильтра для проверки состояния
    set_default_commands(bot)                   # добавление команд в выпадающий список
    bot.infinity_polling(skip_pending=True)     # выключение обработки апдейтов(кроме последнего)










