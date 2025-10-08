import pygame
from variables import *
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generer_couleurs(nombre_couleurs, palette):
    if palette == "Pastel":
        couleurs_bases = {
            0: (173, 216, 230),  # bleu pastel
            1: (255, 182, 193),  # Rose pastel
            2: (240, 230, 140),  # Jaune pastel
            3: (144, 238, 144),  # Vert pastel
            4: (255, 223, 186),  # Orange pastel
            5: (221, 160, 221),  # Violet pastel
            6: (240, 128, 128),  # Rouge pastel
            7: (255, 255, 153),  # Jaune pastel
            8: (200, 200, 200),  # gris pastel
            9: (255, 218, 185),  # Pêche pastel
            10: (152, 251, 152),  # Vert menthe pastel
            11: (255, 192, 203),  # Rose bonbon pastel
            12: (135, 206, 250),  # Bleu ciel pastel
            13: (216, 191, 216),  # Lilas pastel
            14: (255, 228, 196),  # Bisque pastel
            15: (175, 238, 238),  # Cyan pastel
            16: (255, 182, 193),  # Rose clair pastel
            17: (176, 196, 222),  # Bleu acier pastel
            18: (245, 222, 179),  # Beige pastel
            19: (255, 239, 213),  # Papaya pastel
            20: (255, 245, 238),  # Blanc coquille pastel
            21: (255, 248, 220),  # Blé pastel
            22: (230, 230, 250),  # Lavande pastel
        }
    if palette == "Classique":
        couleurs_bases = {
            0: (127, 140, 141),  # Gris
            1: (255, 87, 51),    # Rouge vif
            2: (51, 255, 87),    # Vert vif
            3: (51, 87, 255),    # Bleu vif
            4: (241, 196, 15),   # Jaune
            5: (142, 68, 173),   # Violet
            6: (26, 188, 156),   # Turquoise
            7: (231, 76, 60),    # Rouge tomate
            8: (46, 204, 113),   # Vert émeraude
            9: (52, 152, 219),   # Bleu clair
            10: (230, 126, 34),  # Orange vif
            11: (155, 89, 182),  # Mauve
            12: (52, 73, 94),    # Bleu gris
            13: (22, 160, 133),  # Vert océan
            14: (192, 57, 43),   # Rouge brique
            15: (41, 128, 185),  # Bleu profond
            16: (39, 174, 96),   # Vert forêt
            17: (243, 156, 18),  # Orange doré
            18: (211, 84, 0),    # Orange foncé
            19: (189, 195, 199), # Gris clair
            20: (149, 165, 166), # Gris bleuté
            21: (44, 62, 80),    # Bleu nuit
            22: (236, 240, 241), # Blanc cassé
        }
    if palette == "Néon":
        couleurs_bases = {
            0: (0, 229, 229),    # Turquoise Néon (inchangé)
            1: (255, 0, 150),    # Rose Néon (plus saturé)
            2: (0, 0, 255),      # Bleu Électrique (plus saturé)
            3: (0, 255, 200),   # Aqua Néon (plus saturé)
            4: (255, 255, 50),  # Jaune Néon (plus saturé)
            5: (0, 128, 255),    # Bleu Flashy (plus saturé)
            6: (0, 255, 150),    # Vert Fluo (plus saturé)
            7: (255, 175, 0),    # Orange Fluo (plus saturé)
            8: (255, 0, 255),    # Magenta Néon (inchangé)
            9: (255, 50, 50),    # Rouge Néon (plus saturé)
            10: (0, 255, 50),    # Vert Néon (plus saturé)
            11: (50, 50, 255),   # Bleu Néon (plus saturé)
            12: (255, 0, 128),    # Rose Flash (plus saturé)
            13: (200, 0, 255),   # Violet Néon (plus saturé)
            14: (0, 255, 128),    # Vert Électrique (plus saturé)
            15: (255, 75, 75),   # Rouge Flash (plus saturé)
            16: (75, 255, 75),   # Vert Flash (plus saturé)
            17: (75, 75, 255),   # Bleu Flash (plus saturé)
            18: (255, 100, 0),   # Orange Néon (plus saturé)
            19: (175, 0, 255),   # Indigo Néon (plus saturé)
            20: (255, 175, 0),   # Orange Électrique (plus saturé)
            21: (0, 255, 255),   # Cyan Néon (inchangé)
            22: (255, 255, 255), # Blanc Éblouissant (inchangé)
        }

    return {i: couleurs_bases.get(i) for i in range(0, nombre_couleurs)}

def modification_style(palette_couleur):
    global couleur_fond_ecran, couleur_fond_grille, couleur_grille, couleur_grille_lignes, couleur_titre, couleur_titre_regles, couleur_texte_regles, couleur_fond_regles, couleur_contour_regles, couleur_fond_fin, couleur_texte_fin, couleur_bouton_2, couleur_hover_bouton_2, couleur_texte_bouton_2

    if palette_couleur == "Classique":
        couleur_fond_ecran = "lightblue"
        couleur_fond_grille = (127, 140, 141) #Gris
        couleur_grille = "black"
        couleur_grille_lignes = "white"
        couleur_titre = "black"
        couleur_titre_regles = "black"
        couleur_texte_regles = "black"
        couleur_fond_regles = (220, 220, 220)  # Gris clair
        couleur_contour_regles = (100, 100, 100)
        couleur_fond_fin = couleur_fond_ecran
        couleur_texte_fin = couleur_titre
        couleur_bouton_2 = (220, 220, 220)  # Gris clair
        couleur_hover_bouton_2 = (200, 200, 200)
        couleur_texte_bouton_2 = couleur_texte_regles

    elif palette_couleur == "Pastel":
        couleur_fond_ecran = (245, 245, 220) #Beige Pastel
        couleur_fond_grille = (173, 216, 230) #Bleu Pastel
        couleur_grille = "grey50"
        couleur_grille_lignes = (189, 252, 201) #Menthe Pastel
        couleur_titre = (255, 182, 193) #Corail Pastel
        couleur_titre_regles = (255, 182, 193) #Corail Pastel
        couleur_texte_regles = "grey50"
        couleur_fond_regles = (173, 216, 230) #Bleu Pastel
        couleur_contour_regles = (189, 252, 201) #Menthe Pastel
        couleur_fond_fin = couleur_fond_ecran
        couleur_texte_fin = couleur_titre
        couleur_bouton_2 = (173, 216, 230) #Bleu Pastel
        couleur_hover_bouton_2 = (153, 236, 250)
        couleur_texte_bouton_2 = couleur_texte_regles

    elif palette_couleur == "Néon":
        couleur_fond_ecran = "grey5"
        couleur_fond_grille = (0, 229, 229) #Turquoise Néon
        couleur_grille = "grey20"
        couleur_grille_lignes = (255, 0, 127) #Rose Néon
        couleur_titre = (255, 0, 127) #Rose Néon
        couleur_titre_regles = (255, 0, 127) #Rose Néon
        couleur_texte_regles = (255, 94, 0) #Orange Néon
        couleur_fond_regles = (0, 229, 229) #Turquoise Néon
        couleur_contour_regles = (255, 0, 127) #Rose Néon
        couleur_fond_fin = couleur_fond_ecran
        couleur_texte_fin = couleur_titre
        couleur_bouton_2 = (0, 229, 229) #Turquoise Néon
        couleur_hover_bouton_2 = (0, 255, 180)
        couleur_texte_bouton_2 = couleur_texte_regles

    else :
        # Valeurs par défaut si aucune palette n'est sélectionnée
        couleur_fond_ecran = "white"
        couleur_fond_grille = (200, 200, 200)
        couleur_grille = "black"
        couleur_grille_lignes = "grey"


def affichage_design_classique(screen, largeur_screen, logo, x_debut_regles, y_debut_regles):
    modification_style("Classique") #Pour avoir les couleurs classiques

    # Titre "Eternity II"
    try:
        font_titre = pygame.font.Font(resource_path("Orbitron/Orbitron-Regular.ttf"), 100)
    except:
        font_titre = pygame.font.Font(None, 100)

    texte_titre = font_titre.render("Eternity II", True, couleur_titre)
    screen.blit(texte_titre, (largeur_screen // 2 - texte_titre.get_width() // 2, 70 - texte_titre.get_height() // 2))

    # Affichage du logo
    screen.blit(logo, (10, 10))

    # TITRE "RÈGLES"
    try:
        font_titre_regles = pygame.font.Font(resource_path("Orbitron/Orbitron-Regular.ttf"), 30)
    except:
        font_titre_regles = pygame.font.Font(None, 35)

    titre_regles = font_titre_regles.render("RÈGLES", True, couleur_titre_regles)  # Noir
    screen.blit(titre_regles, (x_debut_regles + 120, y_debut_regles - 50))  # Centré au-dessus du texte

    # TEXTE DES RÈGLES (bien structuré)
    texte_regles = """Bienvenue dans Eternity II !

Le but du jeu est d'assembler
toutes les pièces dans la grille
de manière à ce que les couleurs
des côtés adjacents
correspondent.

Attention !
Tu ne peux pas poser deux
pièces l'une à coté de l'autre
si elles n'ont pas les bords de
même couleur.
Les pièces en bordure doivent
coincider avec la couleur du bord.

Commandes :
- Clic gauche : déplacer une pièce
- Clic droit : faire pivoter une pièce

Bonne chance !"""

    # Définition de la zone d'affichage
    rect_zone = pygame.Rect(x_debut_regles, y_debut_regles, 375, 520)  # Hauteur ajustée

    # Police et taille du texte
    try:
        font_regles = pygame.font.Font(resource_path("Orbitron/Orbitron-Regular.ttf"), 20)
    except:
        font_regles = pygame.font.Font(None, 25)

    # Affichage du fond de la zone
    pygame.draw.rect(screen, couleur_fond_regles, rect_zone, border_radius=10)  # Bord arrondi

    # Découper et afficher le texte proprement
    lignes = texte_regles.split("\n")  # Séparer les lignes avec "\n"
    y = rect_zone.top + 10  # Décalage du haut

    for ligne in lignes:
        if ligne.strip() == "":  # Vérifier si la ligne est vide pour ajouter un espace vertical
            y += font_regles.get_height() // 2
        else:
            texte_render = font_regles.render(ligne, True, couleur_texte_regles)  # Noir
            screen.blit(texte_render, (rect_zone.left + 5, y))
            y += font_regles.get_height()

    # Afficher le contour du rectangle
    pygame.draw.rect(screen, couleur_contour_regles, rect_zone, width=2, border_radius=10)



