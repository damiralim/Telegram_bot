from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardRemove
from loader import bot
from rapid_api import urls, headers, city_request
from states import UserDataState
from loguru import logger
from keyboards import city_markup
from utils import calendar, calendar_1_callback, calendar_2_callback
import datetime as dt


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
def bot_commands(message: Message):
    bot.set_state(message.from_user.id, UserDataState.commands, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if message.text == '/lowprice':
            data['commands'] = 'lowprice'
        elif message.text == '/highprice':
            data['commands'] = 'highprice'
        elif message.text == '/bestdeal':
            data['commands'] = 'bestdeal'
        # data['commands'] = message.text
    logger.info(f"Выбрана команда {data['commands']}")
    bot.send_message(message.from_user.id, 'Пожалуйста, выбери город. '
                                           '!!!Внимание!!! Поиск по городам Российской Федерации не работает!!!')

@bot.message_handler(state=UserDataState.commands)
def get_city_name(message: Message):
    user_city = message.text.lower().capitalize()
    url, querystring = urls['locations'], {'query': user_city, 'locale': 'ru_RU'}
    user_response = city_request(url=url, headers=headers, params=querystring, timeout=15)
    if isinstance(user_response, dict):
        bot.set_state(message.from_user.id, UserDataState.city_name, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city_name'] = user_city
        logger.info(f'Выбран город {user_city}')
        bot.send_message(message.from_user.id, 'Уточни, пожалуйста', reply_markup=city_markup(user_response))
    else:
        bot.send_message(message.from_user.id, user_response)

@bot.callback_query_handler(func=lambda call: call.data, state=UserDataState.city_name)
def city_inline(call: CallbackQuery):
    call.data = call.data.split(':')
    if call.message:
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            data['location'], data['location_id'] = call.data[0], call.data[1]
        logger.info(f"Выбрана локация: {data['location']}, id: {data['location_id']}")
        bot.send_message(call.from_user.id, 'Введи количество отелей(не более 5)')

@bot.message_handler(state=UserDataState.city_name)
def hotels_quantity(message: Message):
    num_hotels = message.text
    bot.set_state(message.from_user.id, UserDataState.get_num_hotels, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['num_hotels'] = num_hotels
    logger.info(f"Введено количество отелей {data['num_hotels']}")
    bot.send_message(message.from_user.id, 'Нужно ли загрузить фото? Да/Нет')

@bot.message_handler(state = UserDataState.get_num_hotels)
def get_photo(message: Message):
    if message.text.lower() == 'да':
        bot.set_state(message.from_user.id, UserDataState.get_num_photo, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['get_photo'] = 'Yes'
        logger.info("Запрошена загрузка фото")
        bot.send_message(message.from_user.id, 'Какое количество фото выгрузить к каждому отелю?')

    elif message.text.lower() == 'нет':
        bot.set_state(message.from_user.id, UserDataState.refine_command, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['get_photo'] = 'No'
        logger.info("Загрузка фото отклонена")
        bot.send_message(message.from_user.id, 'Выбери дату заезда',
                         reply_markup=calendar.create_calendar(
                             name=calendar_1_callback.prefix,
                             year=dt.datetime.now().year,
                             month=dt.datetime.now().month))

    else:
        bot.reply_to(message, "Введена некорректная команда")
        logger.info(f'Пользователь {message.from_user.id} ввел нераспознаваемую команду')


@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_1_callback.prefix))
def callback_check_in(call: CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_1_callback.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action,
                                           year=year, month=month, day=day)
    if action == "DAY":
        if date.strftime('%d.%m.%Y') < dt.date.today().strftime('%d.%m.%Y'):
            bot.send_message(call.message.chat.id, 'Ошибка!')
            logger.info(f"Пользователь ввел некорректную дату")
        else:
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                data['date_in'] = date.strftime('%d.%m.%Y')
            bot.send_message(call.from_user.id, f"Выбрана дата заезда {date.strftime('%d.%m.%Y')}",
                             reply_markup=ReplyKeyboardRemove())
            bot.send_message(call.message.chat.id, 'Теперь выбери дату выезда',
                         reply_markup=calendar.create_calendar(
                                 name=calendar_2_callback.prefix,
                                 year=dt.datetime.now().year,
                                 month=dt.datetime.now().month))
            logger.info(f"Выбрана дата заезда: {date.strftime('%d.%m.%Y')}")
    elif action == "CANCEL":
        bot.send_message(call.from_user.id, "Отмена выбора даты заезда", reply_markup=ReplyKeyboardRemove())
        logger.info(f"Ввод даты отменен")

@bot.callback_query_handler(func=lambda call: call.data.startswith(calendar_2_callback.prefix))
def callback_check_out(call: CallbackQuery):
    name, action, year, month, day = call.data.split(calendar_2_callback.sep)
    date = calendar.calendar_query_handler(bot=bot, call=call, name=name, action=action,
                                           year=year, month=month, day=day)
    if action == "DAY":
        with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
            if date.strftime('%d.%m.%Y') < data['date_in']:
                bot.send_message(call.message.chat.id, 'Ошибка!')
                logger.info(f"Пользователь ввел некорректную дату")
            else:
                data['date_out'] = date.strftime('%d.%m.%Y')
                bot.send_message(call.from_user.id, f"Выбрана дата выезда {date.strftime('%d.%m.%Y')}",
                                     reply_markup=ReplyKeyboardRemove())
                logger.info(f"Выбрана дата выезда: {date.strftime('%d.%m.%Y')}")
    elif action == "CANCEL":
        bot.send_message(call.from_user.id, "Отмена выбора даты выезда", reply_markup=ReplyKeyboardRemove())
        logger.info(f"Ввод даты отменен")


# @bot.message_handler(stat=UserDataState.get_num_photo)
# def get_num_photo(message: Message):
#     num_photos = message.text
#     bot.set_state(message.from_user.id, UserDataState.refine_command, message.chat.id)
#     with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
#         data['num_photos'] = num_photos
#     logger.info(f"Введено количество фото {data['num_photos']}")
#     bot.send_message(message.from_user.id, 'Выбери дату заезда',
#                      reply_markup=calendar.create_calendar(
#                              name=calendar_1_callback.prefix,
#                              year=dt.datetime.now().year,
#                              month=dt.datetime.now().month))

@bot.message_handler(state=UserDataState.refine_command)
def refine_command(message: Message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['commands'] == 'bestdeal':
            bot.set_state(message.from_user.id, UserDataState.min_price, message.chat.id)
            bot.send_message(message.from_user.id, 'Введи минимальную цену бронирования')
        if data['commands'] == ('lowprice' or 'highprice'):
            bot.set_state(message.from_user.id, UserDataState.data_check, message.chat.id)
            bot.send_message(message.from_user.id, 'Давайте проверим введенные данные')


@bot.message_handler(state = UserDataState.min_price)
def min_price(message: Message):
    min_price = message.text
    bot.set_state(message.from_user.id, UserDataState.max_price, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['min_price'] = min_price
    bot.send_message(message.from_user.id, 'Введи максимальную цену бронирования')

@bot.message_handler(state = UserDataState.max_price)
def max_price(message: Message):
    max_price = message.text
    bot.set_state(message.from_user.id, UserDataState.distance, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['max_price'] = max_price
    bot.send_message(message.from_user.id, 'Введи желаемое расстояние от отеля до центра')

@bot.message_handler(state = UserDataState.distance)
def distance(message: Message):
    distance = message.text
    bot.set_state(message.from_user.id, UserDataState.data_check, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['distance'] = distance
    bot.send_message(message.from_user.id, 'Давайте проверим введенные данные')

@bot.message_handler(state = UserDataState.data_check)
def data_check(message: Message):
    bot.set_state(message.from_user.id, UserDataState.result, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['commands'] == ('lowprice' or 'highprice'):
            pass
        if data['commands'] == 'bestdeal':
            pass

# Вывод всех данных, затем вывод кнопок "Подтверждаю"(->UserDataState.result),
# "Отмена"(уточнить, что изменить, отталкиваясь от команды, исп-я клав-ру, затем перейти в необходимый state)
# if message == 'Отмена':
#     set_state(...)

@bot.message_handler(state=UserDataState.result)
def output(message: Message):
    url = urls['properties']
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        if data['commands'] == 'lowprice':
            sort_method = 'PRICE'
        elif data['commands'] == 'highprice':
            sort_method = 'PRICE_HIGHEST_FIRST'
        elif data['commands'] == 'bestdeal':
            sort_method = 'DISTANCE_FROM_LANDMARK'

    landmarkIds = 'Центр города'
    querystring =  {'destinationId': data['location_id'], 'pageNumber': '1', 'pageSize': '25',
                    'checkIn': data['date_in'], 'checkOut': data['date_out'],
                    'adults1': '1', 'priceMin': data['min_price'], 'priceMax': data['max_price'],
                    'sortOrder': sort_method, 'locale': 'ru_RU', 'currency': 'RUB',
                    'landmarkIds': landmarkIds}

    # user_response = hotel_request(url=url, headers=headers, params=querystring, timeout=15)












