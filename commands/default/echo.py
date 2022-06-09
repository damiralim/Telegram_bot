from telebot.types import Message
from loader import bot

keywords = {'Привет': 'Привеет!', 'Как дела?': 'Зашибись', 'Пока': 'До свидания!',
            'Спасибо': 'Всегда рад помочь)', 'Помощь': 'Введи, пожалуйста, команду help',
            'Старт': 'Погнали!', 'Стоп': 'В смысле?', 'Hi': 'Hi!', 'Hello': 'Hello!',
            'Help': 'Please enter /help', 'Bye': 'Hasta la vista', 'Start': "let's go!",
            'Stop': 'What?'}


@bot.message_handler(content_types=['text'])
def get_text_messages(message: Message):
    if message.text.title() in keywords.keys():
        bot.send_message(message.from_user.id, keywords[message.text.title()])
    else:
        bot.reply_to(message, "Упс! Я тебя не понял, но ты можешь ознакомиться "
                              "с тем, что я умею по команде /help")
