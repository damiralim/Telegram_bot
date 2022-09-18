from telebot.types import Message
from loader import bot
from pathlib import Path
from loguru import logger

help_path = Path('handlers', 'default', 'help.txt')

@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    with open(help_path, 'r', encoding='utf-8') as file:
        bot.send_message(message.from_user.id, file.read(), parse_mode='markdown')
    logger.info(f'Пользователь {message.from_user.id} запросил справку')
