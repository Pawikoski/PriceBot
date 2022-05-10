import argparse
import datetime

import requests
from bs4 import BeautifulSoup
import json
import re
from prices_fetch import product_price
from availability import check_availability
from app import send_message
import datetime
import random
import time

parser = argparse.ArgumentParser()
parser.add_argument("-lowest_price_alert_delay", type=int)
# parser.add_argument("lowest_price_minutes_delay", type=int)

args = parser.parse_args()
lowest_price_alert_delay = args.lowest_price_alert_delay


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
    'cache-control': 'no-cache',
    'cookie': 'trackingPermissionConsentsValue={%22cookies_analytics%22:true%2C%22cookies_personalization%22:true%2C%22cookies_advertisement%22:true}; recently_viewed=[%22514938%22%2C%22647718%22]; breakpointName=xs',
    'pragma': 'no-cache',
    'referer': 'https://www.google.com/',
    'sec-ch-ua': '''" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"''',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
}

with open("data.json") as d:
    data = json.load(d)

sent = []

start_time = datetime.datetime.now()
lowest_price = None
lowest_price_url = None

while True:
    for shop_name in data:
        shop_data = data[shop_name]

        if 'urls' not in shop_data.keys():
            break

        for url in shop_data['urls']:
            response = requests.get(url, headers=HEADERS)
            if response.status_code == 404:
                print("Wrong url!", url)
                continue
            soup = BeautifulSoup(response.text, 'html.parser')

            try:
                is_available = check_availability(soup, shop_name, url)
            except Exception:
                continue

            if not is_available:
                continue

            try:
                price = product_price(soup, shop_name)
            except Exception as e:
                print(e)
                continue

            if price:
                print(price, url)
                if lowest_price:
                    if price < lowest_price:
                        lowest_price = price
                        lowest_price_url = url
                else:
                    lowest_price = price
                    lowest_price_url = url

            if price and type(price) == int and price < 250:
                text = f"!! {price} !!\n\n{url}"
                if text not in sent:
                    sent.append(text)
                    send_message(text)

    sleeping_time = random.randint(10, 60)
    print(f"Sleeping {sleeping_time}...")
    time.sleep(sleeping_time)

    _time = datetime.datetime.now() - start_time

    if (_time.seconds / 60) >= lowest_price_alert_delay:
        start_time = datetime.datetime.now()
        send_message(f"Lowest: {lowest_price}\n\n{lowest_price_url}")
        sent = []
        lowest_price = None
        lowest_price_url = None
