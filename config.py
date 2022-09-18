import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    print('Файл с переменными окружения не обнаружен')
else:
    load_dotenv()

TOKEN = os.getenv('TOKEN')
RapidAPI = os.getenv('RapidAPI')

DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Помощь"),
    ('lowprice', "Самые дешевые отели"),
    ('highprice', "Самые дорогие отели"),
    ('bestdeal', "Лучшие отели по цене и расположению от центра"),
    ('history', "История поиска"),
)

