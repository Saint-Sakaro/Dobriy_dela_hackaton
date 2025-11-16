from typing import List
import json
import faiss
from faiss import IndexFlatL2
import numpy as np
import pickle
from datetime import datetime
from dateutil import parser

class Action_info:
    def __init__(self, text: str, start: str, end: str, NKO: str, city: str,link: str):
        self.text = text
        self.start = parser.parse(start)
        self.end = parser.parse(end)
        self.NKO = NKO
        self.city=city
        self.link=link

    def to_dict(self):
        return {
            "text": self.text,
            "start": self.start,
            "end":self.end,
            "NKO":self.NKO,
            "city":self.city,
            "link":self.link
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            text=data["text"],
            start=data["start"],
            end=data["end"],
            NKO=data["NKO"],
            city=data["city"],
            link=data.get("link", "")
        )

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls.from_dict(data)

class VectorRetriever:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = IndexFlatL2(dim)
        self.collector: List[Action_info] = []

    def add_embedding(self, embedding: np.ndarray, action: Action_info):
        assert embedding.ndim == 2 and embedding.shape[1] == self.dim, "Неверная размерность эмбеддинга!"
        self.index.add(embedding.astype("float32"))
        self.collector.append(action)

        
    def save(self, index_path: str, collector_path: str):
        faiss.write_index(self.index, index_path)
        with open(collector_path, "wb") as f:
            pickle.dump(self.collector, f)
        print(f"[+] Индекс сохранён: {index_path}")
        print(f"[+] Collector сохранён: {collector_path}")


    def search(self,
               query_vector: np.ndarray,
               city: str = "",
               NKO: str = "",
               type_of_action: str = "Текущее",
               time: datetime = None,
               relevants: int = 5):
        if time is None:
            time = datetime.now()
        else: time = parser.parse(time)
        if query_vector.ndim == 1:
            query_vector = query_vector.astype("float32").reshape(1, -1)

        collected = []
        distances, indices = self.index.search(query_vector.astype("float32"), len(self.collector))
        for i in range(len(self.collector)):

            distance = distances[0][i]
            ind = indices[0][i]

            action = self.collector[ind]

            if city and action.city != city:
                continue
            if NKO and action.NKO != NKO:
                continue
            
            match type_of_action:
                case("Текущее"):
                    if not(action.start < time < action.end):
                        continue

                case("Запланированное"):
                    if not(action.start > time):
                        continue

                case("Прошедшее"):
                    if not(time > action.end):
                        continue
            
            collected.append({
                **action.to_dict(),
                "distance": float(distance)
            })
            relevants-=1
            if relevants==0:
                break
        return collected

    @classmethod
    def load(cls, index_path: str, collector_path: str):
        index = faiss.read_index(index_path)
        with open(collector_path, "rb") as f:
            collector = pickle.load(f)

        dim = index.d
        retriever = cls(dim=dim)
        retriever.index = index
        retriever.collector = collector

        print(f"[+] Индекс загружен: {index_path}")
        print(f"[+] Collector загружен ({len(collector)} элементов)")
        return retriever
