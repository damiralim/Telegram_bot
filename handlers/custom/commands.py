import json, datetime as dt
from telebot.types import Message, CallbackQuery, ReplyKeyboardRemove, InputMediaPhoto
from loader import bot
from config import check_data
from rapid_api import urls, headers, city_request, hotel_request
from states import UserDataState
from loguru import logger
from keyboards import city_markup, hotels_markup, photo_markup, yes_no_markup, data_check_markup
from utils import calendar, calendar_1_callback, is_alpha, is_correct
from database import insert_values
from pathlib import Path
from typing import Dict, Tuple, List, Callable
from requests.models import Response

''' Запрос названия города (для команд "lowprice","highprice", "bestdeal") '''

@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def bot_commands(message: Message) -> None:
    bot.set_state(message.from_user.id, UserDataState.city_name, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['command_enter_dt']: dt.datetime = dt.datetime.now() # фиксация даты ввода команды
        data['commands'] = message.text.lstrip('/') \
                           if message.text in ('/lowprice', '/highprice', '/bestdeal') else None

    logger.info(f"Выбрана команда {data['commands']}")
    bot.send_message(message.from_user.id, 'Пожалуйста, введите название города.\n'
                                           '\nP.S. Поиск по городам Российской '
                                           '\nФедерации не работает')

''' Запрос к API для уточнения конкретной локации '''

@bot.message_handler(state=UserDataState.city_name)
def get_city_name(message: Message) -> None:
    user_city: str = message.text.lower().capitalize()

    ''' Проверка корректности названия города '''

    if city_err_message := is_alpha(user_city):
        bot.send_message(message.from_user.id, f'{city_err_message}')
        logger.info(f'Введено название города, содержащее цифры или символы')

    else:
        querystring: Dict[str, str] = {
                                       "q": user_city, "locale": "ru_RU",
                                       "langid": "1033", "siteid": "300000001"
                                      }
        city_response: Response = city_request('GET', urls['locations'],
                                               headers, querystring) # запрос к API

        ''' Проверка наличия ответа от API.
            Выбор локации '''

        if isinstance(city_response, dict):
            bot.set_state(message.from_user.id, UserDataState.get_num_hotels, message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['city_name']: str = user_city
            logger.info(f'Выбран город {user_city}')
            bot.send_message(message.from_user.id, 'Уточните, пожалуйста',
                             reply_markup=city_markup(city_response))
        else:
            bot.send_message(message.from_user.id, city_response)
            bot.delete_state(message.from_user.id, message.chat.id)

''' Запрос количества отелей '''

@bot.callback_query_handler(func=lambda call: call.data, state=UserDataState.get_num_hotels)
def city_inline(call: CallbackQuery) -> None:
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['location_id']: str = call.data
        logger.info(f"Выбрана локация(id): {data['location_id']}")
        bot.send_message(call.from_user.id, f'Выберите количество отелей(не более 5)',
                         reply_markup=hotels_markup())

''' Запрос необходимости загрузки фото '''

@bot.message_handler(state=UserDataState.get_num_hotels)
def hotels_quantity(message: Message) -> None:
    num_hotels: str = message.text

    ''' Проверка корректности введенного числа - количества отелей '''

    if (num_err_message := is_correct(num_hotels)) or int(num_hotels) > 5:
        bot.send_message(message.from_user.id, f'{num_err_message}')
        logger.info(f'Введена строка вместо числа, либо оно превышает лимит')

    else:
        bot.set_state(message.from_user.id, UserDataState.get_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['num_hotels']: int = int(num_hotels)
        logger.info(f"Введено количество отелей {data['num_hotels']}")
        bot.send_message(message.from_user.id, 'Нужно ли загрузить фото?',
                         reply_markup=yes_no_markup())

''' Запрос у пользователя количества фото либо переход к выбору даты заезда/выезда '''

@bot.message_handler(state=UserDataState.get_photo)
def get_photo(message: Message):
    if message.text.lower() == 'да':
        bot.set_state(message.from_user.id, UserDataState.get_num_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['get_photo']: str = 'Yes'
        logger.info("Запрошена загрузка фото")
        bot.send_message(message.from_user.id,
                         'Какое количество фото выгрузить к каждому отелю(не более 10)?',
                         reply_markup=photo_markup())

    elif message.text.lower() == 'нет':
        bot.set_state(message.from_user.id, UserDataState.data_check, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['get_photo']: str = 'No'
        logger.info("Загрузка фото отклонена")
        bot.send_message(message.from_user.id, 'Переходим к выбору даты',
                         reply_markup=ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, 'Выберите дату заезда',
                         reply_markup=calendar.create_calendar(
                             name=calendar_1_callback.prefix,
                             year=dt.datetime.now().year,
                             month=dt.datetime.now().month))

    else:
        bot.send_message(message.from_user.id, 'Вы ввели некорректный ответ. '
                                               'Пожалуйста, напечатайте на клавиатуре "Да" либо "Нет"')
        logger.info(f'Введено некорректное значение')

''' Переход к выбору даты '''

@bot.message_handler(state=UserDataState.get_num_photo)
def get_num_photo(message: Message) -> None:
    num_photo: str = message.text

    ''' Проверка корректности введенного числа - количества фото '''

    if is_correct(num_photo) or int(num_photo) > 10:
        bot.send_message(message.from_user.id, 'Вы ввели некорректное количество фото')
        logger.info(f'Введено некорректное значение')

    else:
        bot.set_state(message.from_user.id, UserDataState.data_check, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['num_photo']: int = int(num_photo)
        logger.info(f"Введено количество фото: {data['num_photo']}")
        bot.send_message(message.from_user.id, 'Переходим к выбору даты',
                         reply_markup=ReplyKeyboardRemove())
        bot.send_message(message.from_user.id, 'Выберите дату заезда',
                         reply_markup=calendar.create_calendar(
                         name=calendar_1_callback.prefix,
                         year=dt.datetime.now().year,
                         month=dt.datetime.now().month))

''' Запрос даты заезда/выезда и минимальной цены бронирования(при выборе команды bestdeal) '''

@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_callback.prefix))
def callendar_using(call: CallbackQuery) -> None:
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date: dt.date = calendar.calendar_query_handler(
                                                    bot=bot, call=call, name=name, action=action,
                                                    year=year, month=month, day=day
                                                   )

    with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
        if action == "DAY":

            ''' Если даты заезда нет в data, нужно ввести ее, если есть - 
                - можно переходить к вводу даты заезда. 
                При отмене выбора любой из дат состояние удаляется '''

            if data.get('date_in', None):

                ''' Проверка корректности выбранной даты выезда '''

                if date.date() < data['date_in']:
                    bot.send_message(call.message.chat.id, 'Дата выезда не может быть раньше даты заезда!')
                    logger.info(f"Пользователь ввел некорректную дату")
                else:
                    data['date_out']: dt.date = date.date()
                    bot.send_message(call.from_user.id, f"Выбрана дата выезда {data['date_out']}",
                                     reply_markup=ReplyKeyboardRemove())
                    logger.info(f"Выбрана дата выезда: {data['date_out']}")

                    ''' В зависимости от выбранной команды происходит 
                        переход к соответствующему новому состоянию '''

                    if data['commands'] == 'bestdeal':
                        bot.set_state(call.from_user.id, UserDataState.min_price, call.message.chat.id)
                        bot.send_message(call.from_user.id, 'Введите минимальную цену бронирования')

                    elif data['commands'] in ('lowprice', 'highprice'):
                        bot.set_state(call.from_user.id, UserDataState.data_check, call.message.chat.id)
                        output: List[str, str] = [
                                                  f'{check_data[k]} - <b>{data[elem]}</b>\n'
                                                  for elem in data for k, v in check_data.items() if k == elem
                                                 ]
                        output[3]: str = output[3].replace('No', 'Нет') if 'No' in output[3] \
                                                                        else output[3].replace('Yes', 'Да')
                        bot.send_message(call.from_user.id, 'Переходим к проверке данных')
                        bot.send_message(call.from_user.id, ''.join(output), parse_mode='HTML',
                                         reply_markup=data_check_markup())
            else:

                ''' Проверка корректности выбранной даты заезда '''

                if date.date() < dt.date.today():
                    bot.send_message(call.message.chat.id, 'Дата заезда не может быть раньше сегодняшней!')
                    logger.info(f"Пользователь ввел некорректную дату")
                else:
                    data['date_in']: dt.date = date.date()
                    bot.send_message(call.from_user.id, f"Выбрана дата заезда {data['date_in']}",
                                     reply_markup=ReplyKeyboardRemove())
                    logger.info(f"Выбрана дата заезда: {data['date_in']}")
                    bot.send_message(call.message.chat.id, 'Теперь выберите дату выезда',
                                     reply_markup=calendar.create_calendar(
                                     name=calendar_1_callback.prefix,
                                     year=dt.datetime.now().year,
                                     month=dt.datetime.now().month))

        elif action == "CANCEL":
            if data.get('date_in', None):
                bot.send_message(call.from_user.id, "Отмена выбора даты выезда",
                                 reply_markup=ReplyKeyboardRemove())
                logger.info(f"Ввод даты выезда отменен")
            else:
                bot.send_message(call.from_user.id, "Отмена выбора даты заезда",
                                 reply_markup=ReplyKeyboardRemove())
                logger.info(f"Ввод даты заезда отменен")

            bot.delete_state(call.from_user.id, call.message.chat.id)

''' Запрос максимальной цены бронирования '''

@bot.message_handler(state=UserDataState.min_price)
def min_price(message: Message) -> None:
    min_price: str = message.text

    ''' Проверка корректности введенного числа - мин. цены бронирования '''

    if is_correct(min_price) or int(min_price) <= 0:
        bot.send_message(message.from_user.id, 'Вы ввели некорректную цену')
        logger.info(f'Введено некорректное число')
    else:
        bot.set_state(message.from_user.id, UserDataState.max_price, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min_price']: int = int(min_price)
        logger.info(f"Введена минимальная цена брони: {data['min_price']}")
        bot.send_message(message.from_user.id, 'Введите максимальную цену бронирования')

''' Запрос расстояния от отеля до центра города '''

@bot.message_handler(state=UserDataState.max_price)
def max_price(message: Message) -> None:
    max_price: str = message.text

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

        ''' Проверка корректности введенного числа - макс. цены бронирования '''

        if is_correct(max_price) or int(max_price) <= 0 or int(max_price) <= data['min_price']:
            bot.send_message(message.from_user.id, 'Вы ввели некорректную цену')
            logger.info(f'Введено некорректное число')
        else:
            bot.set_state(message.from_user.id, UserDataState.distance, message.chat.id)
            data['max_price']: int = int(max_price)
            logger.info(f"Введена максимальная цена брони: {data['max_price']}")
            bot.send_message(message.from_user.id, 'Введите желаемое расстояние от отеля до центра')

''' Переход к подтверждению введенных данных '''

@bot.message_handler(state=UserDataState.distance)
def distance(message: Message) -> None:
    distance: str = message.text

    ''' Проверка корректности введенного числа - расстояния от отеля до центра '''

    if is_correct(distance) or int(distance) <= 0:
        bot.send_message(message.from_user.id, 'Вы ввели букву/символ вместо числа, либо оно меньше ноля')
        logger.info(f'Введено некорректное расстояние')
    else:
        bot.set_state(message.from_user.id, UserDataState.data_check, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['distance']: int = int(distance)
        logger.info(f"Введено расстояние от отеля до центра: {data['distance']}")
        output: List[str] = [
                             f'{check_data[k]} - <b>{data[elem]}</b>\n'
                             for elem in data for k, v in check_data.items() if k == elem
                            ]
        output[3]: str = output[3].replace('No', 'Нет') if 'No' in output[3] \
                                                        else output[3].replace('Yes', 'Да')
        bot.send_message(message.from_user.id, 'Переходим к проверке данных')
        bot.send_message(message.from_user.id, ''.join(output), parse_mode='HTML',
                         reply_markup=data_check_markup())

''' Функция возвращает полученную от API информацию '''

@bot.message_handler(state=UserDataState.result)
def output(message: Message) -> Callable:
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        min_price, max_price = '', ''
        photo: str = data['num_photo'] if data['get_photo'] == 'Yes' else 0         # кол-во фото
        timedelta: dt.timedelta = data['date_out'] - data['date_in']                # кол-во дней брони
        add_params: Tuple[int, str] = (photo, timedelta.days, data['commands'])     # кортеж доп-х параметров

        ''' Выбор метода сортировки отелей в зависимости от команды '''

        if data['commands'] in ('lowprice', 'highprice'):
            sort_method: str = 'PRICE_LOW_TO_HIGH'
        elif data['commands'] == 'bestdeal':
            sort_method: str = 'DISTANCE'
            min_price, max_price = data['min_price'], data['max_price']

        ''' Параметры для запроса к API '''

        payload: Dict[str, str, int] = {
            "currency": "USD",
            "eapid": 1,
            "locale": "ru_RU",
            "siteId": 300000001,
            "destination": {"regionId": data['location_id']},
            "checkInDate": {
                "day": data['date_in'].day,
                "month": data['date_in'].month,
                "year": data['date_in'].year
            },
            "checkOutDate": {
                "day": data['date_out'].day,
                "month": data['date_out'].month,
                "year": data['date_out'].year
            },
            "rooms": [
                {
                    "adults": 2,
                }
            ],
            "resultsStartingIndex": 0,
            "resultsSize": data['num_hotels'],
            "sort": sort_method,
            "filters": {
                "price": {
                    "max": max_price,
                    "min": min_price
                }
            }
        }

    hotels_response: Response = hotel_request('POST', urls['properties'],
                                              headers, payload, add_params) # запрос к API

    ''' Проверка наличия выходных данных от API '''

    if isinstance(hotels_response, dict):

        ''' Вывод сообщений юзеру с информацией и фото по отелям(из данных от API) '''

        for id, hotel in hotels_response.items():
            output: List[str] = [
                                 f'{entry}: {value}\n'
                                 for entry, value in hotel.items() if entry != 'Фото'
                                ]
            bot.send_message(message.from_user.id, ''.join(output), parse_mode='HTML')
            if isinstance(hotels_response[id].get('Фото', None), list):
                medias: List[str] = [InputMediaPhoto(photo) for photo in hotels_response[id]['Фото']]
                bot.send_media_group(message.from_user.id, medias)
            if data[id].get('Фото', None) == 0:
                bot.send_message(message.from_user.id, 'Фото не найдены для данного отеля')

        ''' Сохранение полученных данных в БД '''

        values_to_db: Tuple[str, int, dict, dt.datetime] = (
                                                            message.from_user.id, data['commands'],
                                                            data['command_enter_dt'], data['city_name'],
                                                            int(data['location_id']), data['get_photo'],
                                                            json.dumps(hotels_response, ensure_ascii=False)
                                                           )
        insert_values(values_to_db)

    else:
        bot.send_message(message.from_user.id, hotels_response)
        bot.delete_state(message.from_user.id, message.chat.id)
    return

''' Запрос подтверждения введенных данных и вывод информации по отелям 
    либо переход к началу '''

@bot.message_handler(state = UserDataState.data_check)
def data_check(message: Message) -> None:
    if message.text == 'Переход к выводу':
        bot.set_state(message.from_user.id, UserDataState.result, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['data_check']: str = 'result'
        logger.info("Пользователь подтвердил корректность данных: запрос вывода")

        ''' Загрузка анимации ожидания '''

        with open(Path('handlers', 'default', 'loading.gif'), 'rb') as load_gif:
            bot.send_animation(message.chat.id, load_gif, reply_markup=ReplyKeyboardRemove())
        output(message)
        bot.delete_state(message.from_user.id, message.chat.id)

    elif message.text == 'Возврат к началу':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['data_check']: str = 'to_start'
        logger.info("Пользователь хочет изменить данные: возврат к началу")
        bot.send_message(message.from_user.id, 'Хорошо, можете переходить к началу по команде /start',
                         reply_markup=ReplyKeyboardRemove())
        bot.delete_state(message.from_user.id, message.chat.id)

    else:
        bot.send_message(message.from_user.id, 'Вы ввели некорректную команду')
        logger.info(f'Введена некорректная команда')





