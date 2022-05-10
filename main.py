import requests, telebot, os

os.environ['TOKEN'] = '5384137466:AAFWagd9CXO-oX9jyntG898s1Cf4G5yE5UM'
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