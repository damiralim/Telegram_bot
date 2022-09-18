from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

def city_markup(response):
    destinations = InlineKeyboardMarkup()
    for city, id in response.items():
        destinations.add(InlineKeyboardButton(text=city,
                                              callback_data=f'{city}:{id}'))
    return destinations

# @bot.callback_query_handler(func=lambda call: call.data)
# def query_handler(call):
#     start = InlineKeyboardMarkup()
#     for command in commands:
#         start.add(InlineKeyboardButton(text=command,
#                                        callback_data=command))
#     bot.answer_callback_query(callback_query_id=call.id)
#     answer = 'Выбирай)'
#     if call.data == '1':
#         bot.send_message(call.message.chat.id, answer, reply_markup=start)
#     elif call.data == '2':
#         help.bot_help(call.message)
#
#     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
#
# @bot.callback_query_handler(func=lambda call: call.data=='1')
# def query_handler(call):
#     bot.send_message(call.message.from_user.id, '', reply_markup=start_markup())
#
# @bot.callback_query_handler(func=lambda call: call.data == '2')
# def query_handler(call):
#     help.bot_help(message=call.message)
#     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)