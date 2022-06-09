import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    print('Файл с переменными окружения не обнаружен')
else:
    load_dotenv()

TOKEN = os.getenv('TOKEN')
RapidAPI = os.getenv('RapidAPI')