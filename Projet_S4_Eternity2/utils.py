import pygame
import sys
import os


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


pygame.mixer.init()
son_check = pygame.mixer.Sound(resource_path("Son/Check.ogg"))
son_faux = pygame.mixer.Sound(resource_path("Son/Faux.ogg"))
son_victoire = pygame.mixer.Sound(resource_path("Son/Victoire.ogg"))


def load_image(path, size):
    image = pygame.image.load(resource_path(path))
    return pygame.transform.scale(image, size)

def load_sound(path):
    return pygame.mixer.Sound(resource_path(path))

def play_sound(sound):
    pygame.mixer.Sound.play(sound)
    pygame.mixer.music.stop()

def sons(son,son_jouable):

    if son_jouable == True:

        if son == "son_check":
            pygame.mixer.Sound.play(son_check)
            pygame.mixer.music.stop()

        elif son == "son_faux":
            pygame.mixer.Sound.play(son_faux)
            pygame.mixer.music.stop()

        elif son == "son_victoire":
            pygame.mixer.Sound.play(son_victoire)
            pygame.mixer.music.stop()

def affichage_regles(regles,couleur_titre_regles,x_debut_regles,y_debut_regles, screen, couleur_fond_regles, couleur_contour_regles, couleur_texte_regles, couleur_fond_ecran):

    if regles == True :
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

    else :
        rect_zone = pygame.Rect(x_debut_regles, y_debut_regles, 375, 520)
        pygame.draw.rect(screen, couleur_fond_ecran, rect_zone, width=2, border_radius=10)