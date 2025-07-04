
import json

def load_filters():
    with open("filters.json", "r", encoding="utf-8") as f:
        return json.load(f)
