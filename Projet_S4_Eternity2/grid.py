import random
from piece import *

def lire_fichier(filename):
    with open(filename, 'r') as f:
        taille_grille, nombre_couleurs = map(int, f.readline().strip().split())
        grille = []
        for ligne in f:
            piece = tuple(map(int, ligne.strip().strip('()').split(',')))
            grille.append(piece)
    return taille_grille, nombre_couleurs, grille

def creer_pieces(grille, couleurs, largeur_screen, longueur_screen, taille_piece, x_debut_regles, x_debut, y_debut):
    pieces = []
    for i, cotes in enumerate(grille):
        couleurs_piece = [
            couleurs[cotes[0]],  # Haut
            couleurs[cotes[1]],  # Droite
            couleurs[cotes[2]],  # Bas
            couleurs[cotes[3]],  # Gauche
        ]
        piece = Piece(i, random.randint(650, largeur_screen - (taille_piece + 50 + (largeur_screen-x_debut_regles))), random.randint(185, longueur_screen - (taille_piece + 50)), cotes, couleurs_piece, taille_piece, x_debut, y_debut)  # Par défaut, aucune position
     # Ajouter une rotation aléatoire (0, 90, 180, 270)
        rotations = random.choice([0, 1, 2, 3])  # 0 = pas de rotation, 1 = 90°, 2 = 180°, 3 = 270°
        for _ in range(rotations):
            piece.rotate()  # Appliquer la rotation

        pieces.append(piece)
    pieces =  random.sample(pieces, len(pieces))
    return pieces
