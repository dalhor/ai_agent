
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

import faiss
import numpy as np
import json


short_memory_limit = 12

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
                self.long_memory = json.load(f)
            print("Mémoire longue chargée depuis le disque")
        except:
            self.index = faiss.IndexFlatL2(384)
            self.long_memory = []
            print("Pas de mémoire trouvée, nouvelle mémoire initialisée")

    def add_memory(self, text, metadata):
        embeddings = self.sentence_model.encode(text).astype("float32")
        self.index.add(np.array([embeddings]))
        self.long_memory.append({
            "text": text,
            "metadata": metadata
        })

    def search_memory(self, user_input, k=5):
        user_embedding = self.sentence_model.encode(user_input).astype("float32")
        _, indices = self.index.search(np.array([user_embedding]), k)

        results = [self.long_memory[i] for i in indices[0] if i < len(self.long_memory)]
        return results
    
    def save_memory(self):
        faiss.write_index(self.index, "long_term_memory.faiss")
        with open("long_memory.json", "w") as f:
            json.dump(self.long_memory, f)
    
    def load_memory(self):
        self.index = faiss.read_index('long_term_memory.faiss')
        with open("long_memory.json", "r") as f:
            self.long_memory = json.load(f)