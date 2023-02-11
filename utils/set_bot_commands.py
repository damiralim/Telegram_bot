from telebot.types import BotCommand
from config import DEFAULT_COMMANDS

''' Формирование выпадающего меню с командами бота '''

def set_default_commands(bot) -> None:
    bot.set_my_commands(
                        [BotCommand(*i) for i in DEFAULT_COMMANDS]
                       )
