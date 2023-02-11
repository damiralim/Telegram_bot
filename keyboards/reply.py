from telebot.types import ReplyKeyboardMarkup

''' Вывод клавиатуры для уточнения, требуется ли загрузка фото '''

def yes_no_markup() -> ReplyKeyboardMarkup:
    yes_no: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
    yes_no.row('Да', 'Нет')
    return yes_no

''' Вывод клавиатуры для подтверждения введенных данных '''

def data_check_markup() -> ReplyKeyboardMarkup:
    data_check: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
    data_check.row('Переход к выводу', 'Возврат к началу')
    return data_check

''' Вывод клавиатуры для уточнения количества отелей '''

def hotels_markup() -> ReplyKeyboardMarkup:
    hotels: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
    hotels.row('1', '2', '3', '4', '5')
    return hotels

''' Вывод клавиатуры для уточнения количества фото '''

def photo_markup() -> ReplyKeyboardMarkup:
    photo: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
    photo.row('1', '2', '3', '4', '5', '6', '7', '8', '9', '10')
    return photo