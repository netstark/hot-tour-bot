
import json
import os

class SentStore:
    def __init__(self, path):
        self.path = path
        self.sent = set()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.sent = set(json.load(f))

    def is_sent(self, item):
        return item in self.sent

    def mark_as_sent(self, item):
        self.sent.add(item)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(list(self.sent), f, ensure_ascii=False)
