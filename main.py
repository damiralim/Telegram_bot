import requests, telebot, os
from dotenv import load_dotenv

env_path = os.path.join('template.env')
load_dotenv(env_path)
token = os.getenv('TOKEN')


shelty_bot = telebot.TeleBot(token)

@shelty_bot.message_handler(commands=['hello-world'])
def start_message(message):
    shelty_bot.send_message(message.chat.id,'Привет, юзер')

@shelty_bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == 'Привет':
        shelty_bot.send_message(message.from_user.id, 'Привет, как тебя зовут?')
    elif message.text == 'Пока':
      shelty_bot.send_message(message.from_user.id, 'Привет, как тебя зовут?')


shelty_bot.infinity_polling()