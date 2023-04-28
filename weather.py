import json
import requests
from bot import is_message_text


def send_location(message):
    if is_message_text(message):
        city = message.text.lower().strip()
        weather_info = execute_weather_request(city)
        if check_weather_existing(message, weather_info):
            lat = weather_info["coord"]["lat"]
            lon = weather_info["coord"]["lon"]
            bot.send_location(message.chat.id, lat, lon)


def send_weather(message):
    if is_message_text(message):
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


def execute_weather_request(city):
    data = requests.get(weather_url + city + "&appid=" + weather_api + "&units=metric" + "&lang=en")
    return json.loads(data.text)


def check_weather_existing(message, weather_info):
    if weather_info["cod"] != 200:
        bot.send_message(message.chat.id, "I do not know such a city, please select the function again")
        return False
    return True

