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


class ReactiveAgent:
    def __init__(self, name="Agent"):
        self.name = name
        self.memory = []

    def entryInput(self, input: str) -> str:
        """Prend une entrée utilisateur et renvoie une action/réponse."""
        return input.lower()

    def decide(self, receivedInput: str) -> str:
        if "bonjour" in receivedInput:
            return "Bonjour à toi !"
        elif "au revoir" in receivedInput:
            return "Au revoir, à bientôt !"
        elif "aide" in receivedInput:
            return "Je peux répondre à 'bonjour', 'au revoir', et 'aide'."
        else:
            return "Je ne comprends pas encore cette requête."

    def act(self, decision: str, user_input: str) -> str:
        self.memory.append({"user": user_input, "agent": decision})
        return decision

    def perceive_and_act(self, user_input: str) -> str:
        perceived = self.entryInput(user_input)
        decision = self.decide(perceived)
        return self.act(decision, user_input)
