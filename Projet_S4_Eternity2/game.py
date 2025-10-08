import pygame
import random
import threading
from piece import *
from grid import *
from styles import *
from utils import *
from noeud import *
from listeNoeud import *
from methArbo import *
from variables import *
import sys
from threading import Event
import os

# Initialisation de Pygame
pygame.init()


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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


def run_game():
    global running, scene, choix_grille, palette_couleur, selected_tile, grille_jeu, taille_piece, pieces, largeur_screen, ia_thread, ia_stop_requested
    clock = pygame.time.Clock()
    try :
        while running:
            clock.tick(60)
            if scene == 1:
                show_menu()
            elif scene == 2:
                play_game()

    finally:
        # ia_stop_event.set()
        # if ia_thread is not None :
        #     if 'ia_thread' in globals() and ia_thread.is_alive():
        #         ia_thread.join()
        pygame.quit()

def show_menu():
    global running, scene, choix_grille, palette_couleur, logo, taille_piece, pieces, font_titre, font_bouton

    try:
        font_titre = pygame.font.Font(resource_path("Orbitron/Orbitron-Regular.ttf"), 25)
        font_bouton = pygame.font.Font(resource_path("Orbitron/Orbitron-Regular.ttf"), 35)
    except:
        font_titre = pygame.font.Font(None, 50)
        font_bouton = pygame.font.Font(None, 50)

    couleur_fond = "lightblue"
    couleur_bouton = (100, 100, 255)
    couleur_hover = (50, 50, 200)
    couleur_selection = (0, 200, 0)
    blanc = (255, 255, 255)

    tailles_possibles = [4, 6, 8, 12, 16]
    boutons = []
    boutons2 = []
    # choix_grille = None  # Aucune sélection au départ
    palette_couleur = None # Aucune sélection au départ
    run = True

    while run:
        screen.fill(couleur_fond)
        affichage_design_classique(screen, largeur_screen,logo, x_debut_regles, y_debut_regles)

        titre = font_titre.render("Choisissez la taille de la grille", True, (0, 0, 0))
        screen.blit(titre, (50, 160))

        boutons.clear()
        for i, taille in enumerate(tailles_possibles):
            rect = pygame.Rect(150, 215 + i * 70, 200, 50)
            boutons.append((rect, taille))

            if rect.collidepoint(pygame.mouse.get_pos()):
                couleur = couleur_hover if choix_grille != taille else couleur_selection
            else:
                couleur = couleur_selection if choix_grille == taille else couleur_bouton

            pygame.draw.rect(screen, couleur, rect, border_radius=10)
            texte = font_bouton.render(f"{taille}x{taille}", True, blanc)
            screen.blit(texte, (rect.x + (rect.width - texte.get_width()) // 2, rect.y + (rect.height - texte.get_height()) // 2))

        titre2 = font_titre.render("Choisissez la couleur des pièces", True, (0, 0, 0))
        screen.blit(titre2, (550, 160))

        boutons2.clear()
        for i, palette in enumerate(["Classique", "Pastel", "Néon"]):
            rect = pygame.Rect(675, 230 + i * 100, 200, 50)
            boutons2.append((rect, palette))

            if rect.collidepoint(pygame.mouse.get_pos()):
                couleur = couleur_hover if palette_couleur != palette else couleur_selection
            else:
                couleur = couleur_selection if palette_couleur == palette else couleur_bouton

            pygame.draw.rect(screen, couleur, rect, border_radius=10)
            texte2 = font_bouton.render(f"{palette}", True, blanc)
            screen.blit(texte2, (rect.x + (rect.width - texte2.get_width()) // 2, rect.y + (rect.height - texte2.get_height()) // 2))

        bouton_jouer = pygame.Rect(225, 670, 200, 60)
        if bouton_jouer.collidepoint(pygame.mouse.get_pos()):
            couleur_jouer = (255, 50, 50) if choix_grille is None and palette_couleur is None else (0, 100, 200)
        else:
            couleur_jouer = (255, 0, 0) if choix_grille is None or palette_couleur is None else (0, 150, 255)

        texte_jouable = """Vous avez bien sélectionné une taille et un style ?
Dans ce cas là vous êtes prêt à jouer !

Appuie ici : """
        y = 600
        for ligne in texte_jouable.split("\n"):
            if ligne.strip() == "":
                y += font_titre.get_height() // 2
            else:
                texte_render = font_titre.render(ligne, True, (0, 0, 0))
                screen.blit(texte_render, (50, y))
                y += font_titre.get_height()

        pygame.draw.rect(screen, couleur_jouer, bouton_jouer, border_radius=10)
        texte_jouer = font_bouton.render("Jouer", True, blanc)
        screen.blit(texte_jouer, (bouton_jouer.x + (bouton_jouer.width - texte_jouer.get_width()) // 2, bouton_jouer.y + (bouton_jouer.height - texte_jouer.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, taille in boutons:
                    if rect.collidepoint(event.pos):
                        choix_grille = taille
                for rect, palette in boutons2:
                    if rect.collidepoint(event.pos):
                        palette_couleur = palette
                if bouton_jouer.collidepoint(event.pos) and choix_grille is not None and palette_couleur is not None:
                    taille_piece = 480 // choix_grille
                    scene = 2
                    fichier =  resource_path("Grille/Grille" + str(choix_grille) + "x" + str(choix_grille) + ".txt")
                    taille_grille, nombre_couleurs, grille = lire_fichier(fichier)
                    couleurs = generer_couleurs(nombre_couleurs, palette_couleur)
                    pieces = creer_pieces(grille, couleurs, largeur_screen, longueur_screen, taille_piece, x_debut_regles, x_debut, y_debut)
                    modification_style(palette_couleur)
                    run = False

def play_game():
        handle_events()

def draw_ecran():
    global choix_grille, taille_piece, couleur_fond_ecran ,couleur_fond_grille, couleur_grille, couleur_grille_lignes, couleur_titre, couleur_titre_regles, couleur_texte_regles, couleur_fond_regles, couleur_contour_regles, bouton_retour, bouton_quitter, bouton_ia, bouton_son, bouton_regles, couleur_bouton_2, couleur_hover_bouton_2, couleur_texte_bouton_2, pieces, rect_zone

    x_debut, y_debut = 50, 200

    screen.fill(couleur_fond_ecran)  # Effacer l'écran

    # Dessiner la grille
    pygame.draw.rect(screen, couleur_fond_grille, (35, 185, 510, 510))  # Fond de la grille en gris

    for j in range(choix_grille**2):
        i = j
        if j % choix_grille == 0 and j != 0:
            y_debut += taille_piece
        if j >= choix_grille:
            i = i % choix_grille

        pygame.draw.rect(screen, couleur_grille, ((x_debut + (i * taille_piece)), y_debut, taille_piece, taille_piece))
        pygame.draw.rect(screen, couleur_grille_lignes, ((x_debut + (i * taille_piece)), y_debut, taille_piece, taille_piece), width=1)

    try:
        font_titre = pygame.font.Font(resource_path("Orbitron/Orbitron-Regular.ttf"), 100)
    except:
        font_titre = pygame.font.Font(None, 100)

    texte_titre = font_titre.render("Eternity II", True, couleur_titre)
    screen.blit(texte_titre, (largeur_screen // 2 - texte_titre.get_width() // 2, 70 - texte_titre.get_height() // 2))

    # Affichage du logo
    screen.blit(logo, (10, 10))



    ## BOUTONS

    #Bouton retour
    bouton_retour = pygame.Rect(x_debut_regles - 15, 15, 200, 60)

    # Détection du survol et sélection
    if bouton_retour.collidepoint(pygame.mouse.get_pos()):
        couleur_retour = couleur_hover_bouton_2
    else:
        couleur_retour = couleur_bouton_2

    pygame.draw.rect(screen, couleur_retour, bouton_retour, border_radius=10)
    texte_retour = font_bouton.render("Retour", True, couleur_texte_bouton_2)
    screen.blit(texte_retour, (bouton_retour.x + (bouton_retour.width - texte_retour.get_width()) // 2, bouton_retour.y + (bouton_retour.height - texte_retour.get_height()) // 2))


    #Bouton quitter
    bouton_quitter = pygame.Rect(x_debut_regles + (210 - 15) , 15, 200, 60)

    # Détection du survol et sélection
    if bouton_quitter.collidepoint(pygame.mouse.get_pos()):
        couleur_quitter = couleur_hover_bouton_2
    else:
        couleur_quitter = couleur_bouton_2

    pygame.draw.rect(screen, couleur_quitter, bouton_quitter, border_radius=10)
    texte_quitter = font_bouton.render("Quitter", True, couleur_texte_bouton_2)
    screen.blit(texte_quitter, (bouton_quitter.x + (bouton_quitter.width - texte_quitter.get_width()) // 2, bouton_quitter.y + (bouton_quitter.height - texte_quitter.get_height()) // 2))

    ##TEST POUR IA
    #Bouton ia
    bouton_ia = pygame.Rect(x_debut_regles + 210 - 15, 80, 95, 50)

    # Détection du survol et sélection
    if bouton_ia.collidepoint(pygame.mouse.get_pos()):
        couleur_ia = couleur_hover_bouton_2
    else:
        couleur_ia = couleur_bouton_2

    pygame.draw.rect(screen, couleur_ia, bouton_ia, border_radius=10)
    texte_ia = font_bouton.render("IA", True, couleur_texte_bouton_2)
    screen.blit(texte_ia, (bouton_ia.x + (bouton_ia.width - texte_ia.get_width()) // 2, bouton_ia.y + (bouton_ia.height - texte_ia.get_height()) // 2))
    ##FIN TEST IA


    #Bouton son
    bouton_son = pygame.Rect(x_debut_regles + (210 - 15)  + 100, 80, 100, 50)

    # Détection du survol et sélection
    if bouton_son.collidepoint(pygame.mouse.get_pos()):
        couleur_son = couleur_hover_bouton_2
    else:
        couleur_son = couleur_bouton_2

    pygame.draw.rect(screen, couleur_son, bouton_son, border_radius=10)
    if son_jouable == True:
        screen.blit( image_son_on, ( x_debut_regles + (210 - 15)  + 100 + 30, 85) )
    else:
        screen.blit( image_son_off, ( (x_debut_regles + (210 - 15)  + 100) + 30 , 85) )


    #Bouton Règles
    bouton_regles = pygame.Rect(x_debut_regles - 15, 80, 200, 50)

    # Détection du survol et sélection
    if bouton_regles.collidepoint(pygame.mouse.get_pos()):
        couleur_regles = couleur_hover_bouton_2
    else:
        couleur_regles = couleur_bouton_2

    pygame.draw.rect(screen, couleur_regles, bouton_regles, border_radius=10)
    texte_regles = font_bouton.render("regles", True, couleur_texte_bouton_2)
    screen.blit(texte_regles, (bouton_regles.x + (bouton_regles.width - texte_regles.get_width()) // 2, bouton_regles.y + (bouton_regles.height - texte_regles.get_height()) // 2))


    affichage_regles(regles,couleur_titre_regles,x_debut_regles,y_debut_regles, screen, couleur_fond_regles, couleur_contour_regles, couleur_texte_regles, couleur_fond_ecran)


def run_ia():
    global grille_jeu, pieces, ia_state, grille_backup, pieces_backup

    ia_state["running"] = True
    ia_state["stop_requested"] = False

    try:
        # Sauvegarde l'état actuel avant de démarrer
        grille_backup = {k:v for k,v in grille_jeu.items()}
        pieces_backup = [p for p in pieces]

        noeud_initial = Noeud(grille_backup, pieces_backup)
        solution = explorer_profondeur(noeud_initial, grille_jeu, pieces, screen)

        if solution and not ia_state["stop_requested"]:
            # Applique la solution complète
            grille_jeu.clear()
            for (lig, col), piece in solution.grille.items():
                piece.ligne, piece.colonne = lig, col
                piece.rect.x = x_debut + col * taille_piece
                piece.rect.y = y_debut + lig * taille_piece
                grille_jeu[(lig, col)] = piece

    except Exception as e:
        print(f"Erreur dans l'IA: {e}")
    finally:
        ia_state["running"] = False
        # Force le rafraîchissement de l'affichage
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))

def handle_events():
    global running, scene, selected_tile, grille_jeu, son_jouable, regles, screen, ia_running, couleur_fond_ecran, ia_thread, ia_state, pieces
    from methArbo import grille_en_cours, pieces_restantes

    # Gestion des événements
    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # Quitter
            # ia_stop_event.set()
            ia_state["stop_requested"] = True
            ia_state["thread"].join()  # Attend la fin du thread
            ia_state["thread"] = None
            running = False


        # Sélectionner une pièce avec la souris
        if event.type == pygame.MOUSEBUTTONDOWN:

            if bouton_ia.collidepoint(event.pos):
                if not ia_state["running"]:
                    print("Démarrage IA")
                    ia_state["thread"] = threading.Thread(target=run_ia)
                    ia_state["thread"].start()
                else:
                    print("Arrêt IA demandé")
                    ia_state["stop_requested"] = True
                    ia_state["thread"].join()

                    grille_jeu.clear()

                    with lock:
                        grille_jeu = grille_en_cours

                    for piece in pieces:
                        piece.rect.x = random.randint(650, largeur_screen - (taille_piece + 50 + (largeur_screen - x_debut_regles)))
                        piece.rect.y = random.randint(185, longueur_screen - (taille_piece + 50))
                        piece.colonne = None
                        piece.ligne = None

                    # Met à jour les pièces dans la grille (visuellement)
                    for (lig, col), piece in grille_jeu.items():
                        piece.rect.x = x_debut + col * taille_piece
                        piece.rect.y = y_debut + lig * taille_piece
                        piece.ligne = lig
                        piece.colonne = col

                    pieces = list(grille_jeu.values()) + pieces_restantes

                    # Rafraîchit l'affichage
                    screen.fill(couleur_fond_ecran)
                    draw_ecran()
                    for piece in pieces:
                        piece.draw(screen)
                    # for piece in pieces_a_placer:
                    # piece.draw(screen)
                    pygame.display.flip()


                # Gestion de l'événement de rafraîchissement
            if event.type == pygame.USEREVENT:
                screen.fill(couleur_fond_ecran)
                draw_ecran()
                for piece in pieces:
                    piece.draw(screen)
                pygame.display.flip()

            if bouton_retour.collidepoint(event.pos): #bouton retour au menu
                if ia_state["running"]:
                    ia_state["stop_requested"] = True
                    if ia_state["thread"] is not None:
                        ia_state["thread"].join()
                ia_state["running"] = False
                grille_jeu = {} if ia_state["saved_grid"] is None else ia_state["saved_grid"]
                selected_tile = None
                scene = 1

            if bouton_son.collidepoint(event.pos):
                if son_jouable == True:
                    son_jouable = False
                else:
                    son_jouable = True

            if bouton_regles.collidepoint(event.pos):
                if regles == True :
                    regles = False
                else:
                    regles = True

            if bouton_quitter.collidepoint(event.pos):
                if ia_running :
                    ia_state["stop_requested"] = True
                    ia_state["thread"].join()  # Attend la fin du thread
                    ia_state["thread"] = None
                    pygame.time.wait(100)
                    running = False
                else:
                    running = False


            if event.button == 1 and not ia_running :  # Clic gauche pour déplacer
                for piece in pieces:
                    if piece.rect.collidepoint(event.pos):
                        selected_tile = piece

                        if (piece.ligne, piece.colonne) in grille_jeu:  # Si elle était placée
                            grille_jeu.pop((piece.ligne, piece.colonne), None)
                            piece.ligne, piece.colonne = None, None  # La rendre libre



            elif event.button == 3 and not ia_running :  # Clic droit pour pivoter
                for piece in pieces:
                    if piece.rect.collidepoint(event.pos):
                        if (piece.ligne, piece.colonne) in grille_jeu: #vérifie si la pièce est déja dans la grille
                            continue  # Ignore la tentative de rotation
                        piece.rotate()


        # Relâcher la pièce et la fixer sur la grille
        if event.type == pygame.MOUSEBUTTONUP and selected_tile and not ia_running :

            # Trouver la case la plus proche
            selected_tile.colonne = round((selected_tile.rect.x - x_debut) / taille_piece)
            selected_tile.ligne   = round((selected_tile.rect.y - y_debut) / taille_piece)

            # Vérifier que la pièce reste dans la zone de la grille
            if 0 <= selected_tile.colonne < choix_grille and 0 <= selected_tile.ligne < choix_grille:

                # Vérifier si une pièce est déjà présente
                if grille_jeu.get((selected_tile.ligne, selected_tile.colonne)) is None:
                    posable = True

                    # Vérifie si la pièce au dessus a la même couleur
                    if selected_tile.ligne != 0 and posable:
                        if grille_jeu.get((selected_tile.ligne -1, selected_tile.colonne)) is not None:
                            if grille_jeu.get((selected_tile.ligne -1, selected_tile.colonne)).cotes[2] == selected_tile.cotes[0]:
                                posable = True
                            else:
                                posable = False

                    # Vérifie si le bord est gris (haut)
                    if selected_tile.ligne == 0 and posable:
                        if selected_tile.cotes[0] == 0:
                            posable = True
                        else:
                            posable = False

                    # Vérifie si la pièce à gauche a la même couleur
                    if selected_tile.colonne != 0 and posable:
                        if grille_jeu.get((selected_tile.ligne, selected_tile.colonne -1)) is not None:
                            if grille_jeu.get((selected_tile.ligne, selected_tile.colonne -1)).cotes[1] == selected_tile.cotes[3]:
                                posable = True
                            else:
                                posable = False

                    # Vérifie si le bord est gris (gauche)
                    if selected_tile.colonne == 0 and posable:
                        if selected_tile.cotes[3] == 0:
                            posable = True
                        else:
                            posable = False

                    # Vérifie si la pièce en dessous a la même couleur
                    if selected_tile.ligne != choix_grille - 1 and posable:
                        if grille_jeu.get((selected_tile.ligne +1, selected_tile.colonne)) is not None:
                            if grille_jeu.get((selected_tile.ligne + 1, selected_tile.colonne)).cotes[0] == selected_tile.cotes[2]:
                                posable = True
                            else:
                                posable = False

                        # Vérifie si le bord est gris (bas)
                    if selected_tile.ligne == choix_grille - 1 and posable:
                        if selected_tile.cotes[2] == 0:
                            posable = True
                        else:
                            posable = False

                        # Vérifie si la pièce à droite a la même couleur
                    if selected_tile.colonne != choix_grille - 1 and posable:
                        if grille_jeu.get((selected_tile.ligne, selected_tile.colonne +1)) is not None:
                            if grille_jeu.get((selected_tile.ligne, selected_tile.colonne +1)).cotes[3] == selected_tile.cotes[1]:
                                posable = True
                            else:
                                posable = False

                        # Vérifie si le bord est gris (droite)
                    if selected_tile.colonne == choix_grille - 1 and posable:
                        if selected_tile.cotes[1] == 0:
                                posable = True
                        else:
                            posable = False

                        # Si toutes les conditions sont vérifiées
                    if posable:
                        selected_tile.rect.x = x_debut + selected_tile.colonne * taille_piece
                        selected_tile.rect.y = y_debut + selected_tile.ligne * taille_piece
                        grille_jeu[(selected_tile.ligne, selected_tile.colonne)] = selected_tile  # Ajouter au dictionnaire
                            #SON
                        sons("son_check",son_jouable)
                        print( "pièces : ", pieces , "nombre de pièces" , len(pieces))

                        # Sinon, replacer la pièce aléatoirement dans le tas
                    else:
                        selected_tile.rect.x = random.randint(650, largeur_screen - (taille_piece + 50 + (largeur_screen-x_debut_regles)))
                        selected_tile.rect.y = random.randint(185, longueur_screen - (taille_piece + 50))

                        selected_tile.colonne = None
                        selected_tile.ligne = None

                        sons("son_faux",son_jouable)

                else:
                    # Si une pièce est déjà présente, replacer la pièce aléatoirement
                    selected_tile.rect.x = random.randint(650, largeur_screen - (taille_piece + 50 + (largeur_screen-x_debut_regles)))
                    selected_tile.rect.y = random.randint(185, longueur_screen - (taille_piece + 50))

                    selected_tile.colonne = None
                    selected_tile.ligne = None

                    sons("son_faux",son_jouable)

            else:
                # Si hors de la grille,laisser hors de la grille
                selected_tile.colonne = None
                selected_tile.ligne = None

            selected_tile = None  # Désélectionner la pièce



            # Déplacer une pièce sélectionnée
        if event.type == pygame.MOUSEMOTION and selected_tile and not ia_running :

            selected_tile.rect.x, selected_tile.rect.y = event.pos

                # Empêcher de dépasser à gauche et à droite de la fenêtre
            selected_tile.rect.x = max(0, min(selected_tile.rect.x, largeur_screen - taille_piece))

                # Empêcher de dépasser en haut et en bas de la fenêtre
            selected_tile.rect.y = max(0, min(selected_tile.rect.y, longueur_screen - taille_piece))

        draw_ecran()

        if not ia_running :


            # Dessiner les pièces
            for piece in pieces:
                piece.draw(screen)

            if len(grille_jeu) == choix_grille**2: #Vérifie si toutes les pièces sont dans la grille
                try:
                    font_texte_fin = pygame.font.Font(resource_path("Orbitron/Orbitron-Regular.ttf"), 60)
                except:
                    font_texte_fin = pygame.font.Font(None, 74)

                texte_fin_simple = """Félicitations !
    Bien joué ! Merci d'avoir joué !
    Maintenant tu peux essayer une
    grille plus compliquée !
    Nathan Deltour et Tanguy Douillard"""

                texte_fin_compliqué = """Félicitations !
    On ne peut faire plus compliqué !
    Merci d'avoir joué !
    Nathan Deltour et Tanguy Douillard"""

                if choix_grille != 16:
                    texte_fin = texte_fin_simple
                else:
                    texte_fin = texte_fin_compliqué

                #fond pour mieux pouvoir lire
                rect_fin = pygame.Rect(180, 180, 1200, 400)
                pygame.draw.rect(screen, couleur_fond_fin, rect_fin, border_radius=10)

                # Découper et afficher le texte proprement
                lignes = texte_fin.split("\n")  # Séparer les lignes avec "\n"
                y = 200 #longueur_screen // 2 - texte.get_height() // 2  # Décalage du haut

                for ligne in lignes:
                    if ligne.strip() == "":  # Vérifier si la ligne est vide pour ajouter un espace vertical
                        y += font_texte_fin.get_height() // 2
                    else:
                        texte_render = font_texte_fin.render(ligne, True, couleur_texte_fin)  # Noir
                        screen.blit(texte_render, (200, y))
                        y += font_texte_fin.get_height()

                pygame.display.flip()
                sons("son_victoire",son_jouable)
                pygame.time.delay(5000)  # Pause pour que le joueur voie le message
                running = False  # Terminer le jeu


            pygame.display.flip()


if __name__ == "__main__":
    run_game()
    pygame.quit()