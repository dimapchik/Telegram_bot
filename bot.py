import telebot
from telebot import types
import requests
import json
token = "6296134575:AAHFBzHRCKymKXzuD7LKVsCPDCFr9xSEsIU"
bot = telebot.TeleBot(token)
weather_api = "041a995e39ea3d7536ed0d43eab777c7"


@bot.message_handler(commands=['help', 'start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    location = types.KeyboardButton('location')
    temperature = types.KeyboardButton('temperature')
    markup.add(location, temperature)
    bot.send_message(message.chat.id, "Привет, я бот, который умеет говорить температуру в конкретном городе и показывать где он находится", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def request(message):
    if message.text == "location":
        bot.send_message(message.chat.id, "Введите название города")
        bot.register_next_step_handler(message, send_location)
    elif message.text == "temperature":
        bot.send_message(message.chat.id, "Введите название города")
        bot.register_next_step_handler(message, send_temperature)

def execute_request(message):
    city = message.text.lower().strip()
    data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric')
    return json.loads(data.text)


def send_location(message):
    weather_info = execute_request(message)
    if check_existing(message, weather_info):
        lat = weather_info["coord"]["lat"]
        lon = weather_info["coord"]["lon"]
        bot.send_location(message.chat.id, lat, lon)


def send_temperature(message):
    weather_info = execute_request(message)
    if check_existing(message, weather_info):
        temp = weather_info["main"]["temp"]
        bot.send_message(message.chat.id, f'Текущая температура в городе {message.text}: {temp}')


def check_existing(message, weather_info):
    if weather_info["cod"] != 200:
        bot.send_message(message.chat.id, "Я не знаю такого города, выберите функцию заново")
        return False
    return True


bot.polling(none_stop=True)
