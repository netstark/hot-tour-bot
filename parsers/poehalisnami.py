import requests
from bs4 import BeautifulSoup
import json

# Завантаження фільтрів
with open("filters.json", encoding="utf-8") as f:
    filters = json.load(f)

DEPARTURE_CITY = filters["departure_city"]
MAX_PRICE = filters["max_price"]
MIN_DAYS = filters["min_days"]
MAX_DAYS = filters["max_days"]

WARM_COUNTRIES = ["єгипет", "туреччина", "оае", "греція", "іспанія", "італія", "тайланд", "індія", "шрі-ланка", "черногорія"]

def parse_price(price_text):
    price_text = price_text.replace(" ", "").replace("грн", "").strip()
    try:
        return int(price_text)
    except:
        return None

def get_poehalisnami_tours():
    url = f"https://poehalisnami.ua/tours?departure={DEPARTURE_CITY}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []

    # 🔥 Тестовий тур
    test_tour = "\n".join([
        "🔥 Тестовий тур",
        "🏨 Тестовий готель (⭐5⭐)",
        "📍 Testland (Testville) | Виліт з Варшави",
        "🛌 7 ночей",
        "💵 999$ на двох",
        "🔗 [Посилання](https://example.com/test-tour)",
        "🖼 Фото: https://example.com/photo.jpg"
    ])
    results.append(test_tour)

    # Додаємо справжні тури
    cards = soup.find_all("div", class_="tour-card")

    for card in cards:
        try:
            title = card.find("div", class_="hotel-name").text.strip()
            country = card.find("div", class_="country").text.strip().lower()
            if not any(warm in country for warm in WARM_COUNTRIES):
                continue

            rating_tag = card.find("div", class_="rating")
            rating = rating_tag.text.strip() if rating_tag else "-"

            nights_tag = card.find("div", class_="nights")
            nights = int(nights_tag.text.strip()) if nights_tag else 0
            if nights < MIN_DAYS or nights > MAX_DAYS:
                continue

            link = "https://poehalisnami.ua" + card.find("a")["href"]

            img_tag = card.find("img")
            img = img_tag["src"] if img_tag and "src" in img_tag.attrs else None

            price_text = card.find("div", class_="price").text
            price = parse_price(price_text)
            if not price or price > MAX_PRICE:
                continue

            result = f"🏨 {title} ({rating}⭐)\n"
            result += f"📍 {country.title()} | Виліт з {DEPARTURE_CITY}\n"
            result += f"🛌 {nights} ночей\n"
            result += f"💵 {price}$ на двох\n"
            result += f"🔗 [Посилання]({link})\n"
            if img:
                result += f"🖼 Фото: {img}\n"

            results.append(result)
        except Exception:
            continue

    return results
