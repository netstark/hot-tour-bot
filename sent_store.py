
import json

class SentStore:
    def __init__(self, filename):
        self.filename = filename
        try:
            with open(filename, 'r') as f:
                self.sent = set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            self.sent = set()

    def is_sent(self, tour):
        return tour in self.sent

    def mark_as_sent(self, tour):
        self.sent.add(tour)
        with open(self.filename, 'w') as f:
            json.dump(list(self.sent), f)
