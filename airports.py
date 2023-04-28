import json
import requests


def send_airport(message):
    if is_message_text(message):
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


def execute_airport_request(city):
    data = requests.get(airport_url + city, headers={'X-Api-Key': airport_api})
    return json.loads(data.text)


def check_airport_existing(message, airport_info):
    if len(airport_info) == 0:
        bot.send_message(message.chat.id, "I do not know if there is an airport in this city, select the function"
                                          "again")
        return False
    return True
