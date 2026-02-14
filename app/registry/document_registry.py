import json
import os
from datetime import datetime

REGISTRY_PATH = "memory_store/document_registry.json"


class DocumentRegistry:

    def __init__(self):
        os.makedirs("memory_store", exist_ok=True)
        if not os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH, "w") as f:
                json.dump([], f)

    # -------- add new document --------
    def add_document(self, filename: str, char_count: int):

        with open(REGISTRY_PATH, "r") as f:
            data = json.load(f)

        entry = {
            "filename": filename,
            "characters": char_count,
            "uploaded_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        data.append(entry)

        with open(REGISTRY_PATH, "w") as f:
            json.dump(data, f, indent=2)

    # -------- list documents --------
    def list_documents(self):
        with open(REGISTRY_PATH, "r") as f:
            return json.load(f)

    # -------- last uploaded --------
    def last_document(self):
        docs = self.list_documents()
        if not docs:
            return None
        return docs[-1]
