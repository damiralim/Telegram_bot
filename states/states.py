from telebot.handler_backends import State, StatesGroup

class UserDataState(StatesGroup):
    commands = State()
    city_name = State()
    get_num_hotels = State()
    get_photo = State()
    get_num_photo = State()
    refine_command = State()
    min_price = State()
    max_price = State()
    distance = State()
    data_check = State()
    result = State()



