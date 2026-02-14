import os
import json
from datetime import datetime


class DocumentRegistry:

    def __init__(self, path="memory_store/registry.json"):
        self.path = path

        os.makedirs(os.path.dirname(path), exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    # ---------------- LOAD ----------------

    def _load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    # ---------------- SAVE ----------------

    def _save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    # ---------------- ADD DOCUMENT ----------------

    def add_document(self, filename: str, char_count: int):

        data = self._load()

        data.append({
            "filename": filename,
            "char_count": char_count,
            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        self._save(data)

    # ---------------- LIST ----------------

    def list_documents(self):
        return self._load()

    # ---------------- LAST ----------------

    def last_document(self):
        data = self._load()
        return data[-1] if data else None
