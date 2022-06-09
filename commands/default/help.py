from telebot.types import Message
from loader import bot

@bot.message_handler(commands=['help'])
def bot_help(message: Message):
    with open('Readme.md', 'r', encoding='utf-8') as file:
        bot.send_message(message.chat.id, file.read())