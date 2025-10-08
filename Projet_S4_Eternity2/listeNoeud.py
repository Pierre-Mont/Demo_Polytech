from noeud import Noeud

class ListeNoeud:
    def __init__(self):
        print("Création d'une liste de Noeud")
        self.noeuds = []

    def ajouter_noeud(self, noeud):
        print("ajout du noeud :",noeud)
        self.noeuds.append(noeud)

    def supprimer_noeud(self, noeud):
        self.noeuds.remove(noeud)

    def obtenir_dernier_noeud(self):
        print("dernier noeud", self.noeuds[-1])
        # Retourne le dernier noeud ajouté (pour l'exploration en profondeur)
        return self.noeuds[-1] if self.noeuds else None

    def contient_noeud(self, noeud):
        # Vérifie si un noeud est déjà dans la liste
        return noeud in self.noeuds
