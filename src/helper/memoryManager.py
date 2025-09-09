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