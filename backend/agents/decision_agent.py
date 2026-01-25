from rag.vector_store import VectorStore
import os


class DecisionAgent:
    """
    DecisionAgent is responsible ONLY for retrieval (RAG).
    It loads a knowledge base and returns relevant context.
    """

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
        """
        Retrieve relevant historical or business context
        for the decision process.
        """
        return self.vector_store.retrieve(query)