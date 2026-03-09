from rag.vector_store import VectorStore
import os


class DecisionAgent:

    def __init__(self, kb_path: str = None):
        if kb_path is None:
            # Default knowledge base location
            kb_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "rag",
                "knowledge_base.txt"
            )

        self.vector_store = VectorStore(kb_path)

    def retrieve_context(self, query: str):

        return self.vector_store.retrieve(query)