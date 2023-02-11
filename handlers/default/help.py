from loader import bot
from telebot.types import Message
from pathlib import Path
from loguru import logger
from typing import Union

''' Вывод ответа(текст из файла help.txt) по команде help '''

help_path: Union[str, Path] = Path('handlers', 'default', 'help.txt') # путь к файлу help.txt

@bot.message_handler(commands=['help'])
def bot_help(message: Message) -> None:
    with open(help_path, 'r', encoding='utf-8') as file:
        bot.send_message(message.from_user.id, file.read(), parse_mode='markdown')
    logger.info(f'Пользователь {message.from_user.id} запросил справку')
