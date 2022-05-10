import telegram


with open("telegram_api_key.txt", "r") as t:
    api_key = t.readline()

with open("telegram_user_id.txt", "r") as uid:
    user_id = uid.readline()


def send_message(text):
    bot = telegram.Bot(token=api_key)
    bot.send_message(chat_id=user_id, text=text)


