import re
import requests
import bs4
import json


def product_price(soup: bs4.BeautifulSoup, store: str):
    if store == "x-kom.pl":
        price_tag = soup.find("div", attrs={"class": "sc-1a0r5e5-0"}).find("div")
        result = price_tag.findAll("", text=re.compile(r"(?:\d+\s*\d+[,]\d+\s*zł|\d+[,]\d+\s*zł)"), )
        price = float(result[-1].replace("zł", "").replace(",", ".").replace(" ", "").strip())
        return price

    if store == "zadowolenie.pl":
        price_tag = soup.find("div", attrs={"class": "m-priceBox_price m-priceBox_promo"})
        result = price_tag.findAll("", text=re.compile(r"(?:\d+\s*\d+[,]\d+\s*PLN|\d+[,]\d+\s*PLN)"), )
        price = float(result[-1].replace("PLN", "").replace(",", ".").replace(" ", "").strip())
        return price

    if store == "net-s.pl":
        price_tag = soup.find("div", attrs={"class": "current-price"}).find("span", {"itemprop": "price"})
        price = float(price_tag['content'])
        return price

    if store == "buy-it.pl":
        price_tag = soup.find("div", {"class": "price n-price"}).find("span", {"class", "value"}).text
        price = float(price_tag.replace("PLN", "").replace(",", ".").replace(" ", "").strip())
        return price

    if store == "beststore.pl":
        price_tag = soup.find("div", {"class": "single-product"}).find("div", {"class": "product-price"})
        promo_price = price_tag.find("span", {"class": "color-promo"})
        if promo_price:
            result = promo_price.text
        else:
            price_tag.i.decompose()
            result = price_tag.text
        price = float(result.replace("zł", "").replace(",", ".").replace(" ", "").strip())
        return price

    if store == "fatbat.pl":
        price_tag = soup.find("span", {"id": "ProductPrice"}).text.lower()
        price = float(price_tag.replace("zl", "").replace(",", ".").replace(" ", "").strip())
        return price

    if store == "proshop.pl":
        try:
            price_tag = soup.find("span", {"class": "site-currency-wrapper"})\
                .find("div", {"class": "site-currency-attention"}).text
        except AttributeError:
            price_tag = soup.find("span", {"class": "site-currency-wrapper"}) \
                .find("span", {"class": "site-currency-attention"}).text
        price = float(price_tag.replace("zł", "").replace(",", ".").replace(" ", "").strip())
        return price

    if store == "alo.com.pl":
        price = float(soup.find("span", {"class": "price-special"})
                          .find("span", {"class": "core_priceFormat core_cardPriceSpecial"})['data-price'])
        return price

    if store == "empik.com":
        lowest_price = None
        price_tags = soup.findAll("button", {"class": "addToCart"})
        for price_tag in price_tags:
            price = float(price_tag["data-promotional-price"])
            if lowest_price:
                if price < lowest_price:
                    lowest_price = price
            else:
                lowest_price = price

        return lowest_price

    if store == "komputronik.pl":
        price_tag = soup.find("span", {"class": "price"}).find("span", {"class": "proper"}).text
        price = float(price_tag.replace("zł", "").replace(",", ".").replace(" ", "").replace(u"\xa0", "").strip())
        return price

    if store == "hanzo.com.pl":
        price = float(
            soup.find("div", {"class": "price"}).find("em", {"main-price"}).text
                .replace("zł", "").replace(u"\xa0", "").replace(",", ".").strip()
        )
        return price

    if store == "whitemarket.pl":
        price = float(soup.find("span", {"class": "core_cardPriceSpecial"})['data-price'])
        return price

    if store == "visunext.pl":
        product_id = soup.find("div", {"class": "product-essential"}).find("div", {"class": "no-display"}).find("input", {"name": "product"})['value']
        response = requests.get(f"https://www.visunext.at/pricecheck/7/{product_id}").json()
        if int(response['qty']) <= 0:
            print("Product unavailable")
            return False

        return float(response['price'].replace("zł", "").replace(",", ".").replace(" ", "").strip())

    if store == "123drukuj.pl":
        return float(soup.find("meta", {"itemprop": "price"})['content'])

    if store == "rk-technology.com.pl":
        return float(soup.find("input", {"id": "options_products_price_brutto"})['value'])

    if store == "morele.net":
        return float(soup.find("div", {"id": "product_price_brutto"})['content'])

    if store == "mediaexpert.pl":
        return float(soup.find("meta", {"property": "product:price:amount"})['content'])

    if store == "euro.com.pl":
        data = json.loads(soup.find("script", {"type": "application/ld+json"}).text)
        price = float(data['offers']['price'])
        return price

    if store == "sferis.pl":
        price_tag = soup.find("main").find("section", {"class": "top"}).find("section").findAll("div")[1]
        price = float(price_tag.text.replace("zł", "").replace(",", ".").replace(" ", "").strip())
        return price

    if store == "oleole.pl":
        data = json.loads(soup.findAll("script", {"type": "application/ld+json"})[1].text)
        price = float(data['offers']['price'])
        return price

    if store == "mediamarkt.pl":
        try:
            return float(soup.find("meta", {"property": "product:sale_price:amount"})['content'])
        except AttributeError:
            return float(soup.find("meta", {"property": "product:price:amount"})['content'])
