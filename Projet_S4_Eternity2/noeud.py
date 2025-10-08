import pygame
from piece import Piece
import random


class Noeud:
    def __init__(self, grille, pieces):
        self.grille = {}
        for (ligne, colonne), piece in grille.items():
            # Conversion explicite des cotes en liste si nécessaire
            cotes = list(piece.cotes) if isinstance(piece.cotes, tuple) else piece.cotes
            
            new_piece = Piece(
                id_piece=piece.id_piece,
                x=piece.x,
                y=piece.y,
                cotes=cotes,  # Utilise la version liste
                couleurs=piece.couleurs,  # Supposé être une liste
                taille_piece=piece.taille_piece,
                x_debut=piece.x_debut,
                y_debut=piece.y_debut
            )
            new_piece.rotation_index = piece.rotation_index
            self.grille[(ligne, colonne)] = new_piece
        
        self.pieces = [p for p in pieces]  # Copie superficielle
        
    def _copier_piece(self, piece):
        """Crée une copie indépendante d'une pièce"""
        return Piece(
            id_piece=piece.id_piece,
            x=piece.x,
            y=piece.y,
            cotes=list(piece.cotes),
            couleurs=piece.couleurs,
            taille_piece=piece.taille_piece,
            x_debut=piece.x_debut,
            y_debut=piece.y_debut
        )
        
    def est_solution(self):
        from game import choix_grille
        if len(self.grille) == choix_grille**2 :
        # Vérifie si ce noeud représente une solution complète
            return True
    
    def generer_enfants(self):
        from game import ia_stop_event
        global ia_running
        
        enfants = []
        position_libre = self.trouver_case_libre()
        if not position_libre:
            return enfants
    
        # Mélange aléatoire des pièces à tester
        pieces_melangees = self.pieces
        
        for piece in pieces_melangees:
            if ia_stop_event.is_set():
                ia_running = False
                return enfants
                
            rotations = (0, 1, 2, 3)
            
            for rotation in rotations:
                piece_tmp = self._copier_piece(piece)
                for _ in range(rotation):
                    piece_tmp.rotate()
                    
                if self._essayer_placer_piece(piece_tmp, position_libre):
                    nouvelles_pieces = [p for p in self.pieces if p.id_piece != piece.id_piece]
                    enfants.append(Noeud(self._essayer_placer_piece(piece_tmp, position_libre), nouvelles_pieces))
        
        return enfants


    def trouver_case_libre(self):
        from game import choix_grille
        print(f"Grille actuelle : {self.grille}")  # Ajoutez ceci en début de fonction
    # Supposons que la grille est de taille choix_grille x choix_grille
        for ligne in range(choix_grille):  # Utilisez la taille globale de la grille
            for colonne in range(choix_grille):
                if (ligne, colonne) not in self.grille:
                    print(f"Case libre trouvée: {(ligne, colonne)}")
                    return (ligne, colonne)
        print("Aucune case libre trouvée!")
        return None  # Aucune case libre trouvée

    # def placer_piece(self, piece, position):
    #     colonne, ligne = position
    #     nouvelle_grille = self.grille
    
    #     if self.respecte_regle(piece, position, nouvelle_grille):
    #         nouvelle_grille[position] = piece
    #         return nouvelle_grille
    #     return None

    def _essayer_placer_piece(self, piece, position):
        from game import choix_grille, x_debut, y_debut, taille_piece
        ligne, colonne = position
        nouvelle_grille = self.grille
        
        # Vérifier les bords de la grille
        if ligne == 0 and piece.cotes[0] != 0:  # Bord haut
            return None
        if colonne == 0 and piece.cotes[3] != 0:  # Bord gauche
            return None
        if ligne == choix_grille-1 and piece.cotes[2] != 0:  # Bord bas
            return None
        if colonne == choix_grille-1 and piece.cotes[1] != 0:  # Bord droit
            return None
        
        # Vérifier les voisins
        if colonne > 0:  # Voisin de gauche
            voisin = self.grille.get((ligne, colonne-1))
            if voisin and voisin.cotes[1] != piece.cotes[3] or piece.cotes[3] == 0:
                return None
        if ligne > 0:  # Voisin du bas
            voisin = self.grille.get((ligne-1, colonne))
            if voisin and voisin.cotes[2] != piece.cotes[0] or piece.cotes[0] == 0:
                return None
        if colonne < choix_grille-1:  # Voisin de droite
            voisin = self.grille.get((ligne, colonne+1))
            if voisin and voisin.cotes[3] != piece.cotes[1] or piece.cotes[1] == 0:
                return None
        if ligne < choix_grille-1:  # Voisin du haut
            voisin = self.grille.get((ligne+1, colonne))
            if voisin and voisin.cotes[0] != piece.cotes[2] or piece.cotes[2] == 0:
                return None
        
        # Si toutes les vérifications sont passées
        nouvelle_grille[(ligne,colonne)] = piece
        piece.rect.x = x_debut + colonne * taille_piece
        piece.rect.y = y_debut + ligne * taille_piece
        piece.colonne = colonne
        piece.ligne = ligne
        return nouvelle_grille