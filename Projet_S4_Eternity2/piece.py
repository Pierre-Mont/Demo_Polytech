import pygame



class Piece:

    #Initialisation
    def __init__(self, id_piece, x, y, cotes, couleurs, taille_piece, x_debut, y_debut):
        self.id_piece = id_piece
        self.x = x
        self.y = y
        self.cotes = cotes  # Haut, Droite, Bas, Gauche
        self.couleurs = couleurs
        self.rotation = 0  # Rotation actuelle (0, 90, 180, 270)
        self.rect = pygame.Rect(x, y, taille_piece, taille_piece)
        self.taille_piece = taille_piece
        self.ligne   = round((self.rect.y - y_debut) / taille_piece)    # Position ligne sur la grille (0 à choix_grille - 1)
        self.colonne = round((self.rect.x - x_debut) / taille_piece)
        self.rotation_index = 0  # Index de la rotation actuelle
        self.x_debut = x_debut
        self.y_debut=y_debut

    def rotate(self):
        # Rotation de 90 degrés (changer l'ordre des bords)
        self.couleurs = self.couleurs[-1:] + self.couleurs[:-1]
        self.cotes = self.cotes[-1:] + self.cotes[:-1]
        self.rotation = (self.rotation + 90) % 360
        self.rotation_index = (self.rotation_index + 1) % 4


    # Dessiner la pièce avec ses triangles colorés
    def draw(self, surface):
        cx, cy = self.rect.center  # Centre du carré
        corners = [
            (self.rect.left, self.rect.top),      # Haut-gauche
            (self.rect.right, self.rect.top),     # Haut-droit
            (self.rect.right, self.rect.bottom),  # Bas-droit
            (self.rect.left, self.rect.bottom),   # Bas-gauche
        ]

        # Triangle haut
        pygame.draw.polygon(surface, self.couleurs[0], [corners[0], corners[1], (cx, cy)])
        # Triangle droit
        pygame.draw.polygon(surface, self.couleurs[1], [corners[1], corners[2], (cx, cy)])
        # Triangle bas
        pygame.draw.polygon(surface, self.couleurs[2], [corners[2], corners[3], (cx, cy)])
        # Triangle gauche
        pygame.draw.polygon(surface, self.couleurs[3], [corners[3], corners[0], (cx, cy)])
        
        # Dessiner les traits entre les triangles
        trait_couleur = (128, 128, 128)  # Gris clair
        trait_epaisseur = 1
        
        pygame.draw.line(surface, trait_couleur, corners[0], corners[1], trait_epaisseur)  # Haut
        pygame.draw.line(surface, trait_couleur, corners[1], corners[2], trait_epaisseur)  # Droite
        pygame.draw.line(surface, trait_couleur, corners[2], corners[3], trait_epaisseur)  # Bas
        pygame.draw.line(surface, trait_couleur, corners[3], corners[0], trait_epaisseur)  # Gauche
        
         # Dessiner les traits sur les bords
        pygame.draw.line(surface, trait_couleur, corners[0], (cx, cy), trait_epaisseur)  # Diagonale haut-gauche
        pygame.draw.line(surface, trait_couleur, corners[1], (cx, cy), trait_epaisseur)  # Diagonale haut-droit
        pygame.draw.line(surface, trait_couleur, corners[2], (cx, cy), trait_epaisseur)  # Diagonale bas-droit
        pygame.draw.line(surface, trait_couleur, corners[3], (cx, cy), trait_epaisseur)  # Diagonale bas-gauche