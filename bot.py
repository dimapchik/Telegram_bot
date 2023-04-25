import telebot
from telebot import types
import requests
import json
token = "6296134575:AAHFBzHRCKymKXzuD7LKVsCPDCFr9xSEsIU"
bot = telebot.TeleBot(token)
weather_api = "041a995e39ea3d7536ed0d43eab777c7"


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет, хочешь узнать погоду?")


@bot.message_handler()
def request(message):
    city = message.text.lower().strip()
    data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric')
    weather_info = json.loads(data.text)
    temp = weather_info["main"]["temp"]
    lat = weather_info["coord"]["lat"]
    lon = weather_info["coord"]["lon"]
    bot.send_message(message.chat.id, f'Погода в городе {city}: {temp}')
    bot.send_location(message.chat.id, lat, lon)


bot.polling(none_stop=True)
