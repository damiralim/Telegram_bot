from loader import bot
from telebot.types import Message
from loguru import logger
from database import show_history
from typing import List

''' Формирование и вывод истории поиска из БД(столбец с типом json) '''

@bot.message_handler(commands=['history'])
def bot_history(message: Message) -> None:
    history: List[dict] = show_history(message.from_user.id) # функция запроса к БД

    ''' Проверка наличия истории поиска '''

    if isinstance(history, list):
        for entry in history:
            hotel_info: List[str] = [
                                     f'{head}: {value}\n' for param in entry[7].values()
                                     for head, value in param.items() if head != 'Фото'
                                    ]
            output: str = f'Введенная команда: <b>{entry[2]}</b>\n' \
                          f'Дата и время ввода команды: <b>{entry[3].strftime("%Y-%m-%d %H:%M")}</b>\n' \
                          f'{"".join(hotel_info)}\n'
            bot.send_message(message.from_user.id, f'{output}', parse_mode='HTML')
        logger.info(f'Произведен вывод истории поиска пользователя {message.from_user.id}')
    else:
        bot.send_message(message.from_user.id, history)
        logger.info(f'Для пользователя {message.from_user.id} истории поиска не найдено')
