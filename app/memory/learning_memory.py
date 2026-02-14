import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle


class LearningMemory:

    def __init__(self, path="memory_store"):
        self.path = path
        os.makedirs(path, exist_ok=True)

        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

        self.index_file = os.path.join(path, "faiss.index")
        self.text_file = os.path.join(path, "texts.pkl")

        self.index = None
        self.texts = []

        self._load()

    # ---------------- LOAD EXISTING MEMORY ----------------

    def _load(self):
        if os.path.exists(self.index_file) and os.path.exists(self.text_file):
            self.index = faiss.read_index(self.index_file)
            with open(self.text_file, "rb") as f:
                self.texts = pickle.load(f)

    # ---------------- SAVE MEMORY ----------------

    def _save(self):
        if self.index is not None:
            faiss.write_index(self.index, self.index_file)
            with open(self.text_file, "wb") as f:
                pickle.dump(self.texts, f)

    # ---------------- TEXT CHUNKING ----------------

    def _chunk(self, text, size=500):
        words = text.split()
        chunks = []

        for i in range(0, len(words), size):
            chunk = " ".join(words[i:i + size])
            chunks.append(chunk)

        return chunks

    # ---------------- LEARN DOCUMENT ----------------

    def learn(self, text: str):

        # Ignore empty / bad docs
        if not text or len(text.strip()) < 50:
            print("Skipped learning: empty or unreadable document")
            return

        chunks = self._chunk(text)

        # remove useless chunks
        chunks = [c.strip() for c in chunks if len(c.strip()) > 40]

        if not chunks:
            print("Skipped learning: no valid chunks extracted")
            return

        embeddings = self.model.encode(chunks)

        embeddings = np.array(embeddings, dtype="float32")

        # ensure 2D for FAISS
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        if self.index is None:
            self.index = faiss.IndexFlatL2(embeddings.shape[1])

        self.index.add(embeddings)
        self.texts.extend(chunks)

        self._save()
        print(f"Learned {len(chunks)} chunks")

    # ---------------- SEARCH MEMORY ----------------

    def search(self, query: str, k: int = 5):

        if self.index is None or len(self.texts) == 0:
            return ""

        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding, dtype="float32")

        distances, indices = self.index.search(query_embedding, k)

        results = []
        for idx in indices[0]:
            if 0 <= idx < len(self.texts):
                results.append(self.texts[idx])

        return "\n".join(results)
