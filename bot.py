import telebot
from telebot import types
import requests
import json
token = "6296134575:AAHFBzHRCKymKXzuD7LKVsCPDCFr9xSEsIU"
bot = telebot.TeleBot(token)
weather_api = "041a995e39ea3d7536ed0d43eab777c7"


@bot.message_handler(commands=['help'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    location = types.KeyboardButton('location')
    temperature = types.KeyboardButton('temperature')
    photo = types.KeyboardButton('photo location')
    markup.add(location, temperature, photo)
    bot.send_message(message.chat.id, "HEEEEEEEEEEELP", reply_markup=markup)


@bot.message_handler(commands=['weather'])
def weather(message):
    bot.send_message(message.chat.id, "Введите название города.")


@bot.message_handler(content_types=['text'])
def request(message):
    if message.text == "location" or message.text == "temperature":
        bot.send_message(message.chat.id, "Введите название города")
        return
    city = message.text.lower().strip()
    data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api}&units=metric')
    weather_info = json.loads(data.text)
    if weather_info["cod"] != 200:
        bot.send_message(message.chat.id, "Я не знаю такого города")
    else:
        lat = weather_info["coord"]["lat"]
        lon = weather_info["coord"]["lon"]
        temp = weather_info["main"]["temp"]
        if message.text == "location":
            bot.send_location(message.chat.id, lat, lon)
        if message.text == "temperature":
            bot.send_message(message.chat.id, f'Текущая температора в городе {city} : {temp}')



bot.polling(none_stop=True)
