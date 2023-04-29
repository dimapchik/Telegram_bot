import json
import requests
import datetime


def add_secs(time, secs):
    fulldate = datetime.datetime(100, 1, 1, time.hour, time.minute, time.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()


class ApiExec:
    def __init__(self, bot):
        self.airport_api = "ZbKpv6j7r/SFc9pHBVyNzA==rvuihQ9TgbexYCIW"
        self.airport_url = "https://api.api-ninjas.com/v1/airports?city="
        self.weather_api = "041a995e39ea3d7536ed0d43eab777c7"
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather?q="
        self.bot = bot

    def execute_airport_request(self, city):
        data = requests.get(self.airport_url + str(city), headers={'X-Api-Key': self.airport_api})
        return json.loads(data.text)

    def check_airport_existing(self, message, airport_info):
        if len(airport_info) == 0:
            self.bot.send_message(message.chat.id, "I do not know if there is an airport in this city, select the "
                                                   "function again")
            return False
        return True

    def execute_weather_request(self, city):
        data = requests.get(self.weather_url + city + "&appid=" + self.weather_api + "&units=metric" + "&lang=en")
        return json.loads(data.text)

    def check_weather_existing(self, message, weather_info):
        if weather_info["cod"] != 200:
            self.bot.send_message(message.chat.id, "I do not know such a city, please select the function again")
            return False
        return True

    def get_time(self, message, weather_info):
        if self.check_weather_existing(message, weather_info):
            timezone = weather_info["timezone"]
            now = datetime.datetime.now().utcnow()
            return add_secs(now, timezone)

    def is_message_text(self, message):
        if len(message.text) == 0:
            self.bot.send_message(message.chat.id, "You didn't enter any letters? Select function again")
            return False
        return True
