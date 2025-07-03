
import json

def load_filters():
    try:
        with open("filters.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_filters(data):
    with open("filters.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
