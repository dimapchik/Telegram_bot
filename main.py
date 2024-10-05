import telebot
from telebot import types
from src.send_requests import SendExec

token = <our_token>
bot = telebot.TeleBot(token)
my_send = SendExec(bot)


@bot.callback_query_handler(func=lambda call_back: call_back.data == "time in a particular city")
def send_particular_time(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, "Write name of city")
    bot.register_next_step_handler(callback_query.message, my_send.send_time)


@bot.callback_query_handler(func=lambda call_back: call_back.data == "time difference between two cities")
def send_particular_time(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, "Write the name of the cities through the sign # "
                                                  "(ex. Moscow # Berlin)")
    bot.register_next_step_handler(callback_query.message, my_send.send_difference)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    location_button = types.KeyboardButton('/location')
    weather_button = types.KeyboardButton('/weather')
    airport_button = types.KeyboardButton('/airports')
    time_button = types.KeyboardButton('/time')
    markup.add(location_button, weather_button, airport_button, time_button)
    bot.send_message(message.chat.id, "Hi, I'm GeoTimingBot. I can send location by name of city (for it you need "
                                      "write /location), send particular weather in city (write /weather), "
                                      "also I can send you list of airports in your city (write /airports), also send "
                                      "you current time in city or difference time in cities (write /time). "
                                      "For squalor you can use buttons",
                     reply_markup=markup)


@bot.message_handler(commands=['help'])
def help_request(message):
    bot.send_message(message.chat.id, "/help - this message \n"
                                      "/start - starting message and reset buttons \n"
                                      "/location - get location by name of city \n"
                                      "/weather - get particular weather by name of city \n"
                                      "/airports - get list of airports in city \n"
                                      "/time - get current time by name of city or get absolute time difference "
                                      "between two cities")


@bot.message_handler(commands=['location', 'weather', 'airports', 'time'])
def request(message):
    if message.text == "/location":
        bot.send_message(message.chat.id, "Write name of city")
        bot.register_next_step_handler(message, my_send.send_location)
    elif message.text == "/weather":
        bot.send_message(message.chat.id, "Write name of city")
        bot.register_next_step_handler(message, my_send.send_weather)
    elif message.text == "/airports":
        bot.send_message(message.chat.id, "Write name of city and short name of country (ex. London GB,"
                                          " or San Francisco US)")
        bot.register_next_step_handler(message, my_send.send_airport)
    elif message.text == "/time":
        markup = types.InlineKeyboardMarkup()
        time_in_city_button = types.InlineKeyboardButton("time in a particular city",
                                                         callback_data="time in a particular city")
        time_difference_button = types.InlineKeyboardButton("time difference between two cities",
                                                            callback_data="time difference between two cities")
        markup.add(time_in_city_button, time_difference_button)
        bot.send_message(message.chat.id, "What kind of time option do you want?", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def request(message):
    bot.send_message(message.chat.id, "I don't know this command.\nYou can write /help or use buttons")


@bot.message_handler(content_types=['photo'])
def request(message):
    bot.send_message(message.chat.id, "Nice photo but i can't execute it(.\nYou can write /help or use buttons")


@bot.message_handler(content_types=['video'])
def request(message):
    bot.send_message(message.chat.id, "Nice video but i can't execute it(.\nYou can write /help or use buttons")


@bot.message_handler(content_types=['voice', 'audio'])
def request(message):
    bot.send_message(message.chat.id, "Nice voice but i can't execute it(.\nYou can write /help or use buttons")


@bot.message_handler(content_types=['document'])
def request(message):
    bot.send_message(message.chat.id, "Nice file but i can't execute it(.\nYou can write /help or use buttons")


@bot.message_handler(content_types=['animation'])
def request(message):
    bot.send_message(message.chat.id, "Nice animation but i can't execute it(.\nYou can write /help or use buttons")


bot.polling(none_stop=True)
