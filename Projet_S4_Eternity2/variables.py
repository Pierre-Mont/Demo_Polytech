import pygame
import threading
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


#Variables couleurs
couleur_fond_ecran = None
couleur_fond_grille = None
couleur_grille = None
couleur_grille_lignes = None
couleur_titre = None
couleur_titre_regles = None
couleur_texte_regles = None
couleur_fond_regles = None
couleur_contour_regles = None
couleur_fond_fin = None
couleur_texte_fin = None
couleur_bouton_2 = None
couleur_hover_bouton_2 = None
couleur_texte_bouton_2 = None

# Configuration de l'écran
largeur_screen,longueur_screen = 1500 , 750
screen = pygame.display.set_mode((largeur_screen, longueur_screen))
pygame.display.set_caption("Eternity II")

# Variables globales
logo = pygame.image.load(resource_path("Images/Polytech_logo.png"))
logo = pygame.transform.scale(logo, (373, 125))
image_son_on = pygame.image.load(resource_path("Images/son_on.png"))
image_son_on = pygame.transform.scale(image_son_on, (40, 40))
image_son_off = pygame.image.load(resource_path("Images/son_off.png"))
image_son_off = pygame.transform.scale(image_son_off, (40, 40))

son_jouable = True
regles = False
ia_running = False
running = True
scene = 1
choix_grille = None
grille_en_cours = None
pieces_restantes = None

selected_tile = None
grille_jeu = {}
pieces = []
# Remplacez ia_stop_requested par un Event
ia_stop_event = threading.Event()

ia_state = {
    "running": False,
    "thread": None,
    "stop_requested": False,
    "saved_grid": None
}

x_debut = 50
y_debut = 200
x_debut_regles, y_debut_regles = 1100, 185


bouton_retour = pygame.Rect(x_debut_regles - 15, 15, 200, 60)
bouton_quitter = pygame.Rect(x_debut_regles + (210 - 15) , 15, 200, 60)
bouton_ia = pygame.Rect(x_debut_regles + 210 - 15, 80, 95, 50)
bouton_son = pygame.Rect(x_debut_regles + (210 - 15)  + 100, 80, 100, 50)
bouton_regles = pygame.Rect(x_debut_regles - 15, 80, 200, 50)
