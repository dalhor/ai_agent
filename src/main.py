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

if __name__ == "__main__":
    agent = ReactiveAgent("Bot Réactif")
    print("Agent initialisé ✅ (mémoire courte + longue activées)")
    print("Tape 'quit' ou 'exit' pour arrêter.\n")

    while True:
        user_input = input("Toi : ")
        if user_input.lower() in ["quit", "exit"]:
            print("Agent : Fin de la session. Sauvegarde de la mémoire...")
            agent.long_memory.save_memory()
            break

        response = agent.perceive_and_act(user_input)
        print("Agent :", response)