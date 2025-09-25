
###############################################################################
# File       : memoryManager.py
# Module     : helper
# Role       : Memory Manager
# Date       : 23/08/2025
#
# Description:
#    
#
# Author     : dalhor
###############################################################################
from collections import deque
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
from datetime import datetime

import faiss
import numpy as np
import json


short_memory_limit = 12


@dataclass
class MemoryEntry:
    """
    Functionnality:
        Define a precise method to manipulate data
        user: str
        agent: str
        embedding: np.ndarray
        timestamp: str
    """
    user: str
    agent: str
    embedding: np.ndarray
    timestamp: str

    def to_dict(self):
        return {
            "user": self.user,
            "agent": self.agent,
            "embedding": self.embedding.tolist(),
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return MemoryEntry(
            user=data["user"],
            agent=data["agent"],
            embedding=np.array(data["embedding"], dtype="float32"),
            timestamp=data["timestamp"]
        )

    def pretty_print(self):
        return f"[{self.timestamp}] User: {self.user} | Agent: {self.agent}"

class MemoryManager:
    def __init__(self, limit=short_memory_limit):
        self.short_memory = deque(maxlen=limit)
    
    def save_memory(self, user_input, agent_answer):
        self.short_memory.append(
            {
            "user": user_input,
            "agent": agent_answer
        })

    def get_recent(self, n=None):
        if n is None:
            return list(self.short_memory)
        else:
            return list(self.short_memory)[-n:]

    def clear(self):
        self.short_memory.clear()

class LongTermMemoryManager(MemoryManager):
    def __init__(self):
        super().__init__(limit=None)
        self.sentence_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

        try:
            self.index = faiss.read_index("long_term_memory.faiss")
            with open("long_memory.json", "r") as f:
                data = json.load(f)
                self.long_memory = [
                    MemoryEntry(
                        user=entry["user"],
                        agent=entry["agent"],
                        embedding=np.array(entry["embedding"], dtype="float32"),
                        timestamp=entry["timestamp"]
                    )
                    for entry in data
                ]

            print("Mémoire longue chargée depuis le disque")
        except:
            self.index = faiss.IndexFlatL2(384)
            self.long_memory = []
            print("Pas de mémoire trouvée, nouvelle mémoire initialisée")

    def add_memory(self, user_input, decision):
        embeddings = self.sentence_model.encode(user_input).astype("float32")
        self.index.add(np.array([embeddings]))
        entry = MemoryEntry(
            user=user_input,
            agent=decision,
            embedding=embeddings,
            timestamp=datetime.now().isoformat()
        )
        self.long_memory.append(entry)

    def search_memory(self, user_input, k=5):
        user_embedding = self.sentence_model.encode(user_input).astype("float32")
        _, indices = self.index.search(np.array([user_embedding]), k)

        results = [
            self.long_memory[i] 
            for i in indices[0] 
            if i >= 0 and i < len(self.long_memory)
        ]
        return results


    def save_memory(self):
        faiss.write_index(self.index, "long_term_memory.faiss")
        with open("long_memory.json", "w") as f:
            json.dump([entry.to_dict() for entry in self.long_memory], f)


    def load_memory(self):
        self.index = faiss.read_index("long_term_memory.faiss")
        with open("long_memory.json", "r") as f:
            data = json.load(f)
            self.long_memory = [MemoryEntry.from_dict(d) for d in data]
