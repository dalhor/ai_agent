###############################################################################
# File       : reactiveAgent.py
# Module     : agents
# Role       : Chat Agent
# Date       : 09/09/2025
#
# Description:
#    Détails supplémentaires si nécessaire
#
# Author     : dalhor
###############################################################################

from helper.memoryManager import MemoryManager, LongTermMemoryManager, MemoryEntry

class ReactiveAgent:
    def __init__(self, name="Agent", llm_model_path=None):
        self.name = name
        self.short_memory = MemoryManager()
        self.long_memory = LongTermMemoryManager()

        if llm_model_path:
            from .llmWrapper import LLMWrapper
            self.llm = LLMWrapper(llm_model_path)
        else:
            self.llm = None

    def entryInput(self, input: str) -> str:
        """Prend une entrée utilisateur et renvoie une action/réponse."""
        return input.lower()

    def decide(self, received_input: str) -> str:
        lower_input = received_input.lower()
        if "bonjour" in lower_input:
            return "Bonjour à toi !"
        elif "au revoir" in lower_input:
            return "Au revoir, à bientôt !"
        elif "aide" in lower_input:
            return "Je peux répondre à 'bonjour', 'au revoir', et 'aide'."
        context_short = "\n".join(
            [f"User: {m['user']} | Agent: {m['agent']}" 
            for m in self.short_memory.get_recent(5)]
        )
        context_long = "\n".join(
            [m.pretty_print() for m in self.long_memory.search_memory(received_input, k=3)]
        )
        prompt = f"{context_short}\n{context_long}\nUser: {received_input}\nAgent:"
        if self.llm:
            return self.llm.generate(prompt, max_tokens=128)
        return "Je ne comprends pas encore cette requête."


    def act(self, user_input: str, decision: str) -> str:
        self.short_memory.save_memory(user_input, decision)
        if user_input.lower() not in ["souviens", "contexte", "aide"] and "je me souviens" not in decision.lower():
            self.long_memory.add_memory(user_input, decision)
        return decision


    def perceive_and_act(self, user_input: str) -> str:
        perceived = self.entryInput(user_input)
        decision = self.decide(perceived)
        return self.act(user_input, decision)  

