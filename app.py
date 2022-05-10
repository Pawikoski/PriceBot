import telegram

with open("telegram_api_key.txt", "r") as t:
    api_key = t.readline()

user_id = '958907461'


def send_message(text):
    bot = telegram.Bot(token=api_key)
    bot.send_message(chat_id=user_id, text=text)


