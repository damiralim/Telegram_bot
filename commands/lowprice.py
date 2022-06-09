import requests, json, re
from telebot.types import Message
from loader import bot

@bot.message_handler(commands=['lowprice'])
def bot_lowprice(message: Message):
    bot.send_message(message.chat.id,'Сейчас я выведу самые дешевые отели в выбранном городе')

# city = input('Пожалуйста, введите ваш город: ')
# num_of_hotels = int(input('Введите количество отелей(не более 5): '))
# photo = input('Хотите ли вы посмотреть фотографии отелей? Да/Нет ')
# if photo == 'Да':
#     num_of_photo = int(input('Введите количество фотографий(не более 5): '))

# Информация об отеле:
# название отеля,
# адрес,
# как далеко расположен от центра,
# цена,
# N фотографий отеля

# запрашивать у пользователя информацию о том, с какого по какое число
# считать стоимость гостиницы;
# выводить не только стоимость за ночь, но и суммарную стоимость.
# В выводе каждого отеля должна быть ссылка на страницу с отелем.


# url = "https://hotels4.p.rapidapi.com/locations/v2/search"
#
# querystring = {"query":"new york","locale":"en_US","currency":"USD"}
#
# headers = {
# 	"X-RapidAPI-Host": "hotels4.p.rapidapi.com",
# 	"X-RapidAPI-Key": "57717e5754msh90ed16a4180cf6ap124e1bjsn51827540f8fa"
# }
#
# response = requests.request("GET", url, headers=headers, params=querystring)
#
# print(response.text)
#
# pattern = r'(?<="CITY_GROUP",).+?[\]]'
# find = re.search(pattern, response.text)
# if find:
#     json.loads(f"{{{find[0]}}}")


