from bot import bot


def is_message_text(message):
    if len(message.text) == 0:
        bot.send_message(message.chat.id, "You didn't enter any letters? Select function again")
        return False
    return True


def add_secs(time, secs):
    fulldate = datetime.datetime(100, 1, 1, time.hour, time.minute, time.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

