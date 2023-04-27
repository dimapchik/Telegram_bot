import telebot
from telebot import types
import requests
import json
import datetime
token = "6296134575:AAHFBzHRCKymKXzuD7LKVsCPDCFr9xSEsIU"
bot = telebot.TeleBot(token)
weather_api = "041a995e39ea3d7536ed0d43eab777c7"
weather_url = "https://api.openweathermap.org/data/2.5/weather?q="
airport_api = "ZbKpv6j7r/SFc9pHBVyNzA==rvuihQ9TgbexYCIW"
airport_url = "https://api.api-ninjas.com/v1/airports?city="


@bot.callback_query_handler(func=lambda call_back: call_back.data == "time in a particular city")
def send_particular_time(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, "Write name of city")
    bot.register_next_step_handler(callback_query.message, send_time)


@bot.callback_query_handler(func=lambda call_back: call_back.data == "time difference between two cities")
def send_particular_time(callback_query):
    bot.answer_callback_query(callback_query.id)
    bot.send_message(callback_query.from_user.id, "Write the name of the cities through the sign # "
                                                  "(ex. Moscow # Berlin)")
    bot.register_next_step_handler(callback_query.message, send_difference)


@bot.message_handler(commands=['help', 'start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    location_button = types.KeyboardButton('location')
    weather_button = types.KeyboardButton('weather')
    airport_button = types.KeyboardButton('airport')
    time_button = types.KeyboardButton('time')
    markup.add(location_button, weather_button, airport_button, time_button)
    bot.send_message(message.chat.id, "Hi, I'm GeoTimingBot. I can send location by name of city (for it you need "
                                      "write 'location'), send particular weather in city (write 'weather'), "
                                      "also I can send you list of airports in your city (write 'airports'), also send "
                                      "you current time in city or difference time in cities",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def request(message):
    if message.text == "location":
        bot.send_message(message.chat.id, "Write name of city")
        bot.register_next_step_handler(message, send_location)
    elif message.text == "weather":
        bot.send_message(message.chat.id, "Write name of city")
        bot.register_next_step_handler(message, send_weather)
    elif message.text == "airport":
        bot.send_message(message.chat.id, "Write name of city and short name of country (ex. London GB,"
                                          " or San Francisco US)")
        bot.register_next_step_handler(message, send_airport)
    elif message.text == "time":
        markup = types.InlineKeyboardMarkup()
        time_in_city_button = types.InlineKeyboardButton("time in a particular city",
                                                         callback_data="time in a particular city")
        time_difference_button = types.InlineKeyboardButton("time difference between two cities",
                                                            callback_data="time difference between two cities")
        markup.add(time_in_city_button, time_difference_button)
        bot.send_message(message.chat.id, "What kind of time option do you want?", reply_markup=markup)


def send_location(message):
    city = message.text.lower().strip()
    weather_info = execute_weather_request(city)
    if check_weather_existing(message, weather_info):
        lat = weather_info["coord"]["lat"]
        lon = weather_info["coord"]["lon"]
        bot.send_location(message.chat.id, lat, lon)


def send_weather(message):
    city = message.text.lower().strip()
    weather_info = execute_weather_request(city)
    if check_weather_existing(message, weather_info):
        temp = weather_info["main"]["temp"]
        description = weather_info["weather"][0]["description"]
        path_to_image = weather_info["weather"][0]["icon"]
        icon = open(f'./img/{path_to_image}.png', 'rb')
        bot.send_message(message.chat.id, f'Current weather in {message.text}: \n {temp} degrees Celcius \n'
                                          f'{description}')
        bot.send_photo(message.chat.id, icon)


def send_airport(message):
    city = message.text.lower().strip().split()[0]
    airport_info = execute_airport_request(city)
    user_country = message.text.split()[1]
    if check_airport_existing(message, airport_info):
        airports = ''
        for airport in airport_info:
            country = airport["country"]
            if country == user_country:
                name = airport["name"]
                region = airport["region"]
                airports += f'Name airports in {country}, {region}, {city}: {name}\n'
        if airports == '':
            airports = "Either there is no such city in the specified country, or there are no airports in it." \
                       "Reselect function"
        bot.send_message(message.chat.id, airports)


def send_time(message):
    city = message.text.lower().strip()
    weather_info = execute_weather_request(city)
    bot.send_message(message.chat.id, get_time(message, weather_info).strftime('%H:%M'))


def send_difference(message):
    if not ('#' in message.text):
        bot.send_message(message.chat.id, "You have entered cities in the wrong format. Reselect function")
    else:
        city_1 = message.text.split('#')[0].lower().strip()
        city_2 = message.text.split('#')[1].lower().strip()
        weather_info_1 = execute_weather_request(city_1)
        weather_info_2 = execute_weather_request(city_2)
        timezone_1 = weather_info_1["timezone"]
        timezone_2 = weather_info_2["timezone"]
        sec_difference = abs(timezone_1 - timezone_2)
        fake_date = datetime.time(0, 0, 0)
        diff_time = add_secs(fake_date, sec_difference).strftime('%H:%M')
        bot.send_message(message.chat.id, f'Difference between cities {city_1} and {city_2} is {diff_time}')


def get_time(message, weather_info):
    if check_weather_existing(message, weather_info):
        timezone = weather_info["timezone"]
        now = datetime.datetime.now().utcnow()
        return add_secs(now, timezone)


def execute_weather_request(city):
    data = requests.get(weather_url + city + "&appid=" + weather_api + "&units=metric" + "&lang=en")
    return json.loads(data.text)


def execute_airport_request(city):
    data = requests.get(airport_url + city, headers={'X-Api-Key': airport_api})
    return json.loads(data.text)


def check_weather_existing(message, weather_info):
    if weather_info["cod"] != 200:
        bot.send_message(message.chat.id, "I do not know such a city, please select the function again")
        return False
    return True


def check_airport_existing(message, airport_info):
    if len(airport_info) == 0:
        bot.send_message(message.chat.id, "I do not know if there is an airport in this city, select the function"
                                          "again")
        return False
    return True


def add_secs(time, secs):
    fulldate = datetime.datetime(100, 1, 1, time.hour, time.minute, time.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()


bot.polling(none_stop=True)
