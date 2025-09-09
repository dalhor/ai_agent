###############################################################################
# File       : main.py
# Module     : ai_agent
# Role       : main
# Date       : 19/08/2025
#
# Description:
#    
#
# Author     : dalhor
###############################################################################

from agents.reactiveAgent import ReactiveAgent
from helper.memoryManager import MemoryManager

if __name__ == "__main__":
    agent = ReactiveAgent("Bot Réactif")
    memory = MemoryManager()

    while True:
        user_input = input("Toi : ")
        if user_input.lower() in ["quit", "exit"]:
            print("Agent : Fin de la session.")
            break

        response = agent.perceive_and_act(user_input)
        memory.save_memory(user_input, response)

        print("Agent :", response)

        # Exemple : taper "mémoire" pour afficher ce dont l'agent se souvient
        if "mémoire" in user_input.lower():
            print("Mémoire :", memory.get_recent())