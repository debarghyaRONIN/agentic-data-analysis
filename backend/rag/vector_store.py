from sentence_transformers import SentenceTransformer
import faiss

class VectorStore:
    def __init__(self, kb_path):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = open(kb_path).read().split("\n")
        self.index = self._build_index()

    def _build_index(self):
        embeddings = self.model.encode(self.texts)
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
        self.embeddings = embeddings
        return index

    def retrieve(self, query, k=2):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, k)
        return [self.texts[i] for i in indices[0]]
