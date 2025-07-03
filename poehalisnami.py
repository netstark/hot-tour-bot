import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Фільтри за замовчуванням
DEPARTURE_CITY = "warszawa"
MAX_PRICE = 1000  # $ на двох
WARM_COUNTRIES = ["єгипет", "туреччина", "оае", "туніс", "греція", "іспанія", "чорногорія", "албанія"]


def parse_price(text):
    try:
        price = text.replace(" ", "").replace("zł", "").replace("PLN", "")
        return int(price) / 4.0  # приблизна конверсія в долари
    except:
        return None


def get_poehalisnami_tours():
    url = f"https://poehalisnami.ua/tours?departure={DEPARTURE_CITY}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    cards = soup.find_all("div", class_="tour-card")

    for card in cards:
        try:
            title = card.find("div", class_="hotel-name").text.strip()
            country = card.find("div", class_="country").text.strip().lower()
            if not any(warm in country for warm in WARM_COUNTRIES):
                continue

            rating_tag = card.find("div", class_="rating")
            rating = rating_tag.text.strip() if rating_tag else "-"

            nights = card.find("div", class_="nights").text.strip()
            link = "https://poehalisnami.ua" + card.find("a")["href"]
            img_tag = card.find("img")
            img = img_tag["src"] if img_tag and "src" in img_tag.attrs else None

            price_text = card.find("div", class_="price").text
            price = parse_price(price_text)
            if not price or price > MAX_PRICE:
                continue

            result = f"\n🧳 <b>{title}</b> (⭐ {rating})"
            result += f"\n📍 {country.title()} | Виліт з Варшави"
            result += f"\n📆 {nights} ночей"
            result += f"\n💵 ${int(price)} за двох"
            result += f"\n<a href=\"{link}\">🔗 Переглянути</a>"
            if img:
                result += f"\nФото: {img}"

            results.append(result)

        except Exception as e:
            continue

    return results