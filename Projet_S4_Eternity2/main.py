import pygame
from game import *

def main():
    pygame.init()

    # Lancer le jeu
    run_game()

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:  # Si l'utilisateur fait Ctrl+C
        pygame.quit()
