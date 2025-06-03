# rag/retriever.py
import chromadb
from chromadb.utils import embedding_functions

class Retriever:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection(
            name="brd_sections",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        )
    
    def add_document(self, id, text, metadata):
        self.collection.add(
            documents=[text],
            ids=[id],
            metadatas=[metadata]
        )
    
    def query(self, query_text, n_results=3):
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )