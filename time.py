from bot import is_message_text
import datetime


def send_time(message):
    if is_message_text(message):
        city = message.text.lower().strip()
        weather_info = execute_weather_request(city)
        if check_weather_existing(message, weather_info):
            bot.send_message(message.chat.id, get_time(message, weather_info).strftime('%H:%M'))


def send_difference(message):
    if not ('#' in message.text):
        bot.send_message(message.chat.id, "You have entered cities in the wrong format. Reselect function")
    else:
        city_1 = message.text.split('#')[0].lower().strip()
        city_2 = message.text.split('#')[1].lower().strip()
        weather_info_1 = execute_weather_request(city_1)
        weather_info_2 = execute_weather_request(city_2)
        if check_weather_existing(message, weather_info_1) and check_weather_existing(message, weather_info_2):
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

