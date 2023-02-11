from os import getenv
from dotenv import load_dotenv, find_dotenv
from typing import Dict, Tuple

''' Получение токена бота, ключа к API и пароля для подключения к БД '''

if not find_dotenv():
    print('Файл с переменными окружения не обнаружен')
else:
    load_dotenv()

TOKEN: str = getenv('TOKEN')
RapidAPI: str = getenv('RapidAPI')
PostgreSQL: str = getenv('PostgreSQL')

''' Кортеж кортежей с описанием команд бота в выпадающем меню '''

DEFAULT_COMMANDS: Tuple[Tuple[str]] = (
                                       ('start', "Запустить бота"),
                                       ('help', "Помощь"),
                                       ('lowprice', "Самые дешевые отели"),
                                       ('highprice', "Самые дорогие отели"),
                                       ('bestdeal', "Лучшие отели по цене и расположению от центра"),
                                       ('history', "История поиска"),
                                      )

''' Словарь для вывода отформатированного сообщения с введенными пользователем параметрами '''

check_data: Dict[str, str] = {
                              'commands': '&#128203; Команда',
                              'city_name': '\U0001F3D9 Город',
                              'num_hotels': '\U0001F3E8 Кол-во отелей',
                              'get_photo': '\U0001F4F7 Загрузка фото', '\U0001F522\U0001F4F7 num_photo': 'Кол-во фото',
                              'date_in': '\U0001F4C5 Дата заезда', 'date_out': '\U0001F4C6 Дата выезда',
                              'min_price': '&#11015; Мин цена брони', 'max_price': '&#11014; Макс цена брони',
                              'distance': '\U0001F6E3 Расстояние до центра'
                             }


