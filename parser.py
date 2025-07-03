import json
import os
from parsers.poehalisnami import get_poehalisnami_tours

CACHE_FILE = "sent_tours.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(list(cache), f, ensure_ascii=False, indent=2)

async def check_new_tours():
    all_tours = get_poehalisnami_tours()
    cache = load_cache()
    new_tours = []

    for tour in all_tours:
        tour_id = tour.strip()[-100:]  # можна брати link, якщо буде зручніше
        if tour_id not in cache:
            new_tours.append(tour)
            cache.add(tour_id)

    if new_tours:
        save_cache(cache)

    return new_tours
