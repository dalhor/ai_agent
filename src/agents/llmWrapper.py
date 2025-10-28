###############################################################################
# File       : llmWrapper.py
# Module     : agents
# Role       : Description du rôle / fonctionnalité
# Date       : 25/09/2025
#
# Description:
#    Détails supplémentaires si nécessaire
#
# Author     : dalhor
###############################################################################

from llama_cpp import Llama

class LLMWrapper:
    def __init__(self, model_path):
        self.model = Llama(model_path=model_path)

    def generate(self, prompt, max_tokens=128):
        response = self.model(prompt, max_tokens=max_tokens)
        return response['choices'][0]['text']