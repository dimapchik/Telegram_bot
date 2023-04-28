import datetime
from api_requests import ApiExec, add_secs


class SendExec:
    def __init__(self, bot):
        self.my_api = ApiExec(bot)

    def send_location(self, message):
        if self.my_api.is_message_text(message):
            city = message.text.lower().strip()
            weather_info = self.my_api.execute_weather_request(city)
            if self.my_api.check_weather_existing(message, weather_info):
                lat = weather_info["coord"]["lat"]
                lon = weather_info["coord"]["lon"]
                self.my_api.bot.send_location(message.chat.id, lat, lon)

    def send_weather(self, message):
        if self.my_api.is_message_text(message):
            city = message.text.lower().strip()
            weather_info = self.my_api.execute_weather_request(city)
            if self.my_api.check_weather_existing(message, weather_info):
                temp = weather_info["main"]["temp"]
                description = weather_info["weather"][0]["description"]
                path_to_image = weather_info["weather"][0]["icon"]
                icon = open(f'./img/{path_to_image}.png', 'rb')
                self.my_api.bot.send_message(message.chat.id, f'Current weather in {message.text}: \n {temp} degrees'
                                                              f'Celsius \n {description}')
                self.my_api.bot.send_photo(message.chat.id, icon)

    def send_airport(self, message):
        if self.my_api.is_message_text(message):
            city = message.text.lower().strip().split()[0]
            airport_info = self.my_api.execute_airport_request(city)
            user_country = message.text.split()[1]
            if self.my_api.check_airport_existing(message, airport_info):
                airports = ''
                for airport in airport_info:
                    country = airport["country"]
                    if country == user_country:
                        name = airport["name"]
                        region = airport["region"]
                        airports += f'Name airports in {country}, {region}, {city}: {name}\n'
                if airports == '':
                    airports = "Either there is no such city in the specified country, or there are no airports in " \
                               "it.Reselect function"
                self.my_api.bot.send_message(message.chat.id, airports)

    def send_time(self, message):
        if self.my_api.is_message_text(message):
            city = message.text.lower().strip()
            weather_info = self.my_api.execute_weather_request(city)
            if self.my_api.check_weather_existing(message, weather_info):
                self.my_api.bot.send_message(message.chat.id, self.my_api.get_time(message,
                                                                                   weather_info).strftime('%H:%M'))

    def send_difference(self, message):
        if not ('#' in message.text):
            self.my_api.bot.send_message(message.chat.id, "You have entered cities in the wrong format. "
                                                          "Reselect function")
        else:
            city_1 = message.text.split('#')[0].lower().strip()
            city_2 = message.text.split('#')[1].lower().strip()
            weather_info_1 = self.my_api.execute_weather_request(city_1)
            weather_info_2 = self.my_api.execute_weather_request(city_2)
            if self.my_api.check_weather_existing(message, weather_info_1) and \
                    self.my_api.check_weather_existing(message, weather_info_2):
                timezone_1 = weather_info_1["timezone"]
                timezone_2 = weather_info_2["timezone"]
                sec_difference = abs(timezone_1 - timezone_2)
                fake_date = datetime.time(0, 0, 0)
                diff_time = add_secs(fake_date, sec_difference).strftime('%H:%M')
                self.my_api.bot.send_message(message.chat.id, f'Difference between cities {city_1} and '
                                                              f'{city_2} is {diff_time}')
