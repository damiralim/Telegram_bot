from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

''' Вывод клавиатуры для выбора конкретной локации '''

def city_markup(response) -> InlineKeyboardMarkup:
    destinations: InlineKeyboardMarkup = InlineKeyboardMarkup()
    for city, id in response.items():
        destinations.add(InlineKeyboardButton(text=city, callback_data=id))
    return destinations
