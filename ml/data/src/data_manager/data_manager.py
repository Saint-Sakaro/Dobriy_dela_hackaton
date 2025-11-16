import os
import shutil
import pickle
from typing import List, Dict, Tuple
import numpy as np

from embedding.embedder import TextEmbedder
from retrieval.retriever import VectorRetriever, Action_info
from preprocess.chunker import TextPreprocessor

class DatabaseManager:
    def __init__(self, data_path: str = "ml/data", dim: int = 768):
        os.makedirs(data_path, exist_ok=True)
        self.texts_path = os.path.join(data_path, "actions_info.pkl")
        self.index_path = os.path.join(data_path, "actions.index")

        self.embedder = TextEmbedder()
        self.retriever = None
        self.texts: List[Action_info] = []

        test_emb = self.embedder.encode(["тест"])
        real_dim = test_emb.shape[1]

        if os.path.exists(self.index_path) and os.path.exists(self.texts_path):
            self.retriever = VectorRetriever.load(self.index_path, self.texts_path)
            self.texts = self.retriever.collector
        else:
            self.retriever = VectorRetriever(dim=real_dim)

    def add_action(self, action: Action_info):
        preprocessor = TextPreprocessor(use_lemmatization=True)
        raw_text = action.text
        processed_sentences = preprocessor.process(raw_text)
        processed_text = " ".join(processed_sentences)
        embedding = self.embedder.encode([processed_text])
        self.retriever.add_embedding(embedding, action)
        self.save_all()

    def save_all(self):
        self.retriever.save(self.index_path, self.texts_path)
    def get_data(self):
        return self.retriever.index
    def query(self, query_text: str,city: str = "", NKO: str = "",) -> List[Dict]:
        preprocessor = TextPreprocessor()
        sentences = preprocessor.process(query_text)
        processed_text = " ".join(sentences)
        query_vector = self.embedder.encode([processed_text])

        results = self.retriever.search(query_vector,city,NKO)
        return results
