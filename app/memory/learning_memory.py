import json
import os
from app.config.settings import settings


class LearningMemory:

    def __init__(self):
        self.path = settings.MEMORY_PATH
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def add_learning(self, content: str):
        data = self.get_all()
        data.append({"content": content})

        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def get_all(self):
        with open(self.path, "r") as f:
            return json.load(f)
