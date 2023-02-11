from telebot_calendar import Calendar, CallbackData, RUSSIAN_LANGUAGE

''' Вывод календаря для выбора даты заезда/выезда '''

calendar: Calendar = Calendar(language=RUSSIAN_LANGUAGE)
calendar_1_callback: CallbackData = CallbackData("calendar_1", "action", "year", "month", "day")
calendar_2_callback: CallbackData = CallbackData("calendar_2", "action", "year", "month", "day")

