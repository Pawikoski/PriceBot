import bs4
import json


def check_availability(soup: bs4.BeautifulSoup, store: str, url: str = None):
    if store == "x-kom.pl":
        if soup.find("button", {"title": "Dodaj do koszyka"}):
            return True
        return False
    if store == "zadowolenie.pl":
        if soup.find("div", {"class": "b-offer_unavailable"}):
            return False
        return True
    if store == "net-s.pl":
        if soup.find("div", {"class": "product-add-to-cart"}):
            return True
        return False
    if store == "buy-it.pl":
        if soup.find("div", {"class": "buy"}).find("a")['title'] == "Brak":
            return False
        return True
    if store == "beststore.pl":
        if soup.find("button", {"id": "add_to_cart"}):
            return True
        return False
    if store == "fatbat.pl":
        if 'disabled' in soup.find("button", {"id": "AddToCart"}).attrs.keys():
            return False
        return True
    if store == "proshop.pl":
        if soup.find("button", {"data-form-action": "addToBasket"}):
            return True
        return False
    if store == "alo.com.pl":
        if int(soup.find("span", {"data-parameter-value": "availability_amount_number"}).text) > 0:
            return True
        return False
    if store == "empik.com":
        if soup.find("button", {"class": "addToCart"}):
            return True
        return False
    if store == "komputronik.pl":
        if '"sum_available":0' in soup.find("ktr-product-availability")['availability']:
            return False
        return True
    if store == "hanzo.com.pl":
        if "none" in soup.find("fieldset", {"class": "addtobasket-container"})['class']\
                and "none" not in soup.find("fieldset", {"class": "availability-notifier-container"})['class']:
            return False
        return True
    if store == "whitemarket.pl":
        if soup.find("button", {"class": "add-to-cart"}):
            return True
        return False
    if store == "visunext.pl":
        return True
    if store == "123drukuj.pl":
        if soup.find("meta", {"itemprop": "availability"})['content'] == "InStock":
            return True
        return False
    if store == "rk-technology.com.pl":
        if soup.find("div", {"class": "view_stock_info_text_ok"}) and "dostępny" \
                in soup.find("div", {"class": "view_stock_info_text_ok"}).text:
            return True
        return False
    if store == "morele.net":
        if not soup.find("a", {"class": "btn-add-to-basket"}):
            return False
        return True
    if store == "mediaexpert.pl":
        if soup.find("button", {"class": "add-to-cart"}):
            return True
        return False
    if store == "euro.com.pl":
        if not soup.find("script", {"type": "application/ld+json"}):
            return False
        if json.loads(soup.find("script", {"type": "application/ld+json"}).text)['offers']['price'] == '0.00':
            return False
        return True
    if store == "sferis.pl":
        if soup.find("a", {"class": "jsCartAddHref"}):
            return True
        return False
    if store == "oleole.pl":
        return True
    if store == "mediamarkt.pl":
        if soup.find("button", {"id": "show-price-add-to-cart-btn"}):
            return True
        return False
