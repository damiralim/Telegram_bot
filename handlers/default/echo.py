from loader import bot
from telebot.types import Message
from loguru import logger

''' Вывод шаблона ответа при нераспознаваемой команде '''

@bot.message_handler(content_types=['text'])
def bot_echo(message: Message) -> None:
    bot.reply_to(message, "Упс! Я тебя не понял, но ты можешь ознакомиться "
                          "с тем, что я умею по команде /help")
    logger.info(f'Пользователь {message.from_user.id} ввел нераспознаваемую команду')
