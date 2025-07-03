import json
import os

FILTERS_FILE = "filters.json"

def load_filters():
    if os.path.exists(FILTERS_FILE):
        with open(FILTERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "departure_city": "Варшава",
        "max_price": 1000,
        "min_days": 5,
        "max_days": 10
    }

def save_filters(filters):
    with open(FILTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(filters, f, ensure_ascii=False, indent=2)
