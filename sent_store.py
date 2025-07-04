import json
import os

class SentStore:
    def __init__(self, path):
        self.path = path
        self.sent = set()
        if os.path.exists(path):
            try:
                with open(path, 'r') as f:
                    self.sent = set(json.load(f))
            except:
                self.sent = set()

    def is_sent(self, item_id):
        return item_id in self.sent

    def mark_as_sent(self, item_id):
        self.sent.add(item_id)
        with open(self.path, 'w') as f:
            json.dump(list(self.sent), f)