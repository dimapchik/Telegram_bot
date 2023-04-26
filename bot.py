import telebot
from telebot import types
import requests
import json
token = "6296134575:AAHFBzHRCKymKXzuD7LKVsCPDCFr9xSEsIU"
bot = telebot.TeleBot(token)
weather_api = "041a995e39ea3d7536ed0d43eab777c7"
weather_url = "https://api.openweathermap.org/data/2.5/weather?q="
airport_api = "ZbKpv6j7r/SFc9pHBVyNzA==rvuihQ9TgbexYCIW"
airport_url = "https://api.api-ninjas.com/v1/airports?city="


@bot.message_handler(commands=['help', 'start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    location = types.KeyboardButton('location')
    temperature = types.KeyboardButton('temperature')
    airport = types.KeyboardButton('airport')
    markup.add(location, temperature, airport)
    bot.send_message(message.chat.id, "Привет, я бот, который умеет говорить температуру в конкретном городе, "
                                      "показывать где он находится и вывести названия всех аэропортов в этом городе."
                                      "Чтобы получить локацию введите 'location', чтобы получить текущую температуру "
                                      "введите 'temperature'. Чтобы узнать какие аэропорты есть в городе, введите "
                                      "'airport'",
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def request(message):
    if message.text == "location":
        bot.send_message(message.chat.id, "Введите название города")
        bot.register_next_step_handler(message, send_location)
    elif message.text == "temperature":
        bot.send_message(message.chat.id, "Введите название города")
        bot.register_next_step_handler(message, send_temperature)
    elif message.text == "airport":
        bot.send_message(message.chat.id, "Введите название города на английском языке с большой буквы и сокращённое"
                                          " название страны (например GB - Great Britain или BR - Brazil)")
        bot.register_next_step_handler(message, send_airport)


def send_location(message):
    weather_info = execute_weather_request(message)
    if check_weather_existing(message, weather_info):
        lat = weather_info["coord"]["lat"]
        lon = weather_info["coord"]["lon"]
        bot.send_location(message.chat.id, lat, lon)


def send_temperature(message):
    weather_info = execute_weather_request(message)
    if check_weather_existing(message, weather_info):
        temp = weather_info["main"]["temp"]
        bot.send_message(message.chat.id, f'Текущая температура в городе {message.text}: {temp} градусов Цельсия')


def send_airport(message):
    airport_info = execute_airport_request(message)
    city = message.text.split()[0]
    user_country = message.text.split()[1]
    if check_airport_existing(message, airport_info):
        airports = ''
        for airport in airport_info:
            country = airport["country"]
            if country == user_country:
                name = airport["name"]
                region = airport["region"]
                airports += f'Название аэропорта в {country}, {region}, {city}: {name}\n'
        if airports == '':
            airports = "В указанной стране либо нет такого города, либо в нём нет аэропортов."
        bot.send_message(message.chat.id, airports)


def execute_weather_request(message):
    city = message.text.lower().strip()
    data = requests.get(weather_url + city + "&appid=" + weather_api + "&units=metric")
    return json.loads(data.text)


def execute_airport_request(message):
    city = message.text.lower().strip().split()[0]
    data = requests.get(airport_url + city, headers={'X-Api-Key': airport_api})
    return json.loads(data.text)


def check_weather_existing(message, weather_info):
    if weather_info["cod"] != 200:
        bot.send_message(message.chat.id, "Я не знаю такого города, выберите функцию заново")
        return False
    return True


def check_airport_existing(message, airport_info):
    if len(airport_info) == 0:
        bot.send_message(message.chat.id, "Я не знаю есть ли в этом городе аэропорт, выберите функцию заново")
        return False
    return True


bot.polling(none_stop=True)
