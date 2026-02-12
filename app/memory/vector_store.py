import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:

    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection("legal_memory")
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

    def add_documents(self, texts):
        embeddings = self.embedder.encode(texts).tolist()
        ids = [f"id_{i}" for i in range(len(texts))]

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            ids=ids
        )

    def search(self, query, k=5):
        emb = self.embedder.encode([query]).tolist()[0]
        results = self.collection.query(query_embeddings=[emb], n_results=k)
        return results["documents"][0]
