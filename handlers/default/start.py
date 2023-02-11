from loader import bot
from telebot.types import Message
from loguru import logger

''' Вывод приветствия по команде start '''

cmd_descr: str = '/help - помощь по командам\n' \
                 '/lowprice - самые дешёвые отели в выбранном городе\n' \
                 '/highprice - самые дорогие отели в выбранном городе\n' \
                 '/bestdeal -  лучшие отели по цене и расположению от центра\n' \
                 '/history — история поиска\n'\
                 '\nВыбери интересующую тебя команду'

@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    bot.send_message(message.from_user.id, f'Привет👋, {message.from_user.full_name}! '
                                           f'Я помогу тебе выбрать наилучшее место для отдыха! Смотри, что я умею:')
    logger.info(f'Пользователь {message.from_user.id} запустил бота')
    bot.send_message(message.from_user.id, text=cmd_descr)




