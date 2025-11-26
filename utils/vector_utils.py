import math

class vector_item:
    def __init__(self, embedding, text):
        self.embedding = embedding
        self.text = text

class vector_store:
    def __init__(self):
        self.vector_store: list[vector_item] = []

    def add_embedding(self, embedding: list[float], text: str):
        self.vector_store.append(vector_item(embedding, text))

    def search(self, query: list[float], top_k: int = 5) -> list[str]:
        score_list = sorted(self.vector_store, key=lambda item: self.cosine_similarity(query, item.embedding), reverse=True)
        return [item.text for item in score_list[:top_k]]

    def cosine_similarity(self, v1: list[float], v2: list[float]) -> float:
        dot_product = sum(a * b for a, b in zip(v1, v2))
        magnitude_v1 = math.sqrt(sum(a * a for a in v1))
        magnitude_v2 = math.sqrt(sum(b * b for b in v2))
        return dot_product / (magnitude_v1 * magnitude_v2)