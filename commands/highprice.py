from telebot.types import Message
from loader import bot

@bot.message_handler(commands=['highprice'])
def start_message(message: Message):
    bot.send_message(message.chat.id,'Сейчас я выведу самые элитные отели в выбранном тобой городе')