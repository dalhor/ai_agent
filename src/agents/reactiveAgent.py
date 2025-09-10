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

from helper.memoryManager import MemoryManager, LongTermMemoryManager

class ReactiveAgent:
    def __init__(self, name="Agent"):
        self.name = name
        self.short_memory = MemoryManager()
        self.long_memory = LongTermMemoryManager()

    def entryInput(self, input: str) -> str:
        """Prend une entrée utilisateur et renvoie une action/réponse."""
        return input.lower()

    def decide(self, received_input: str) -> str:
        if "bonjour" in received_input:
            return "Bonjour à toi !"
        elif "au revoir" in received_input:
            return "Au revoir, à bientôt !"
        elif "aide" in received_input:
            return "Je peux répondre à 'bonjour', 'au revoir', et 'aide'."
        elif "souviens" in received_input:  
            memories = self.long_memory.search_memory(received_input, k=3)
            if memories:
                return "Je me souviens : " + "; ".join([m["text"] for m in memories])
            else:
                return "Je ne trouve rien dans ma mémoire."
        else:
            return "Je ne comprends pas encore cette requête."

    def act(self, user_input: str, decision: str) -> str:
        self.short_memory.save_memory(user_input, decision)

        if user_input.lower() not in ["souviens", "contexte", "aide"]:
            exchange = f"User: {user_input} | Agent: {decision}"
            self.long_memory.add_memory(exchange, {"user": user_input, "agent": decision})

        return decision


    def perceive_and_act(self, user_input: str) -> str:
        perceived = self.entryInput(user_input)
        decision = self.decide(perceived)
        return self.act(user_input, decision)  

