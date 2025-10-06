
import tkinter as tk

import random
import time


# from algo4_1 import algoNoah4
# from algo4inversedepth_2 import algo5
# from nouveau import algop4
# from algo4_puissancen import algon
from algo4_puissancen_thread import algon_th

# from train_opti.algo_train_opti import AIt
# from train_opti.algo_train_opti import AId

profondeur = 7


class Jeu:
    ''' joueur 1 : rouge
        joueur 2 : jaune'''
    def __init__(self, fen):
        self.fen = fen
        
        #frame mère
        self.frame1 = tk.Frame(self.fen, padx = 10, pady = 10)
        self.frame1.pack()
        
        # affichage titre jeu
        self.lb1 = tk.Label(self.frame1, text = "Puissance 4", font = ("bold", 30))
        self.lb1.grid(row = 0, column = 0, columnspan = 2)
 
        # création canvas
        self.cg = tk.Canvas(self.frame1, width = 810, height = 700, bg = "blue")
        self.cg.grid(row = 1, column = 0, rowspan = 2)

        # création choix mode de jeu
        self.checkbox = tk.Frame(self.frame1, background = "lightgrey")
        self.checkbox.grid(row = 1, column = 1)
        self.choix = tk.IntVar(value = 0)
        
        self.b1 = tk.Radiobutton(self.checkbox, text = "J vs J", font = ("", 20) ,background = "lightgrey", variable = self.choix, value = 1)
        self.b1.pack(anchor = tk.W)
        
        self.b2 = tk.Radiobutton(self.checkbox, text = "J vs AI", font = ("", 20), background = "lightgrey", variable = self.choix, value = 2)
        self.b2.pack(anchor = tk.W)
        
        self.b3 = tk.Radiobutton(self.checkbox, text = "AI vs AI", font = ("", 20), background = "lightgrey", variable = self.choix, value = 3)
        self.b3.pack(anchor = tk.W)
        
        # création bouton jouer
        self.value = tk.StringVar(value = "Veuillez sélectionner un mode de jeu puis appuyer sur le bouton jouer")
        self.lb2 = tk.Label(self.frame1, textvariable = self.value, font = ("", 20))
        self.lb2.grid(row = 3, column = 0, columnspan = 2, pady = 10)
        
        self.bj = tk.Button(self.frame1, text = "jouer", bg = "green", font = ("", 15), command = self.jouer)
        self.bj.grid(row = 4, column = 0, columnspan = 2)
        
        # création du choix puissance n?
        self.n = 4
        self.inpchoix = tk.Frame(self.frame1, background = "blue")
        self.inptxt = tk.Text(self.inpchoix, height = 1, width = 2, font = ("", 15))
        self.inptxt.insert('1.0', '4') # car n est de base à 4
        #self.inptxt.set("4")
        self.inptxt.pack()
        self.selectnButton = tk.Button(self.inpchoix, text  = "Select puissance n", font = ("", 10), command = self.updaten)
        self.selectnButton.pack()
        
        self.inpchoix.grid(row = 2, column = 1)
        
        # création de la grille
        for i in range(6):
            for j in range(7):
                self.cg.create_oval(25 + 110 * j, 25 + i * 110, 25 + 110 * (j + 1) - 10, 25 + (i + 1) * 110 - 10, fill = "white")
        
        self.cg.bind("<Button-1>", self.callback)
                
        self.play = False # aucun joueur ne peut jouer 
        


    def updaten(self):
        if self.inptxt.get('1.0', tk.END)[0:-1] in [str(i) for i in range(1,7)]:
            if 1 < int(self.inptxt.get('1.0', tk.END)) < 7:
                self.n = int(self.inptxt.get('1.0'))
                self.lb1['text'] = 'Puissance ' + str(self.n)
            else:
                self.inptxt.delete('1.0', tk.END) #supprime tout depuis l'index 1.0 -> 0 à ...
                self.inptxt.insert('1.0', str(self.n))
        #self.inptxt['state'] = 'disabled'
        else:
            self.inptxt.delete('1.0', tk.END) #supprime tout depuis l'index 1.0 -> 0 à ...
            self.inptxt.insert('1.0', str(self.n))
        # print(self.n)
        
    def jouer(self):
        if self.choix.get() != 0:
            # self.lb2.update_idletasks()
            
            self.inptxt.delete('1.0', tk.END)
            self.inptxt.insert('1.0', str(self.n)) #actualisation au cas où
    
            self.inptxt['state'] = 'disabled' #désactive le changement de puissance n
            # self.value.set(["J vs J", "J vs AI", "AI vs AI"][self.choix.get() - 1])
            
            self.grille = [[ 0 for _ in range(7)] for _ in range(6)]
            self.gameStatus = True
            
            # pour l'algo qui apprend
            self.board = ''
            
            # pour surligner le dernier pion jouer
            self.p = [-1, -1]
            
            
            # reset la grille si on a déjà joué
            self.cg["bg"] = "blue"
            for i in range(6):
                for j in range(7):
                    self.cg.create_oval(25 + 110 * j, 25 + i * 110, 25 + 110 * (j + 1) - 10, 25 + (i + 1) * 110 - 10, fill = "white")
            
            self.Jturn = random.randint(1, 2) # quelle jouer joue en poremier 
            # self.frame1.after(100, self.value.set("Au tour du joueur " + str(self.Jturn)))
            self.value.set("Au tour du joueur " + str(self.Jturn))
            self.lb2.update_idletasks()
            
            
            # savoir le mode de partie pour la lancer 
            if self.choix.get() == 1: # J vs J
                self.play = True
                
            elif self.choix.get() == 2: # J vs AI
                if self.Jturn == 1:
                    self.play = True
                else:
                    self.play = False # le bot joue en premier
                    self.AI()
                    # self.frame1.after(10, self.AI())
            
            elif self.choix.get() == 3: # AI vs AI
                self.play = False # le jouer ne peut pas jouer 
                self.AI()
                # self.frame1.after(10, self.AI())
            
    def callback(self, event):
        # print(self.play, self.choix.get())
        if self.play and self.gameStatus:
            
            # print("clicked", event.x, event.y)
            if 20 < event.x < 810 - 15:
                # print ((event.x - 20) // 110)
                x = (event.x - 20) // 110
                if 0 <= x < 7 and self.grille[0][x] == 0:
                    self.play = False
                    self.putpiece(x)
                    
                    # savoir si parti  fini
                    co = self.gagne()
                    # print(co)
                    if not self.gameStatus:
                        self.value.set("Le gagnant est le joueur " + str(self.Jturn))
                        for i in co:
                            self.dessinevict(i[1], i[0])
                            time.sleep(0.4)
                            self.cg.update_idletasks()
                        self.inptxt['state'] = 'normal' # réactive la puissance n
                            
                    elif not 0 in self.grille[0]:
                        self.gameStatus = False
                        self.value.set("Egalité")
                        self.lb2.update()
                        self.inptxt['state'] = 'normal' # réactive la puissance n
                        self.dessinega()

                    
                    elif self.choix.get() == 1:
                        self.play = True
                        self.Jturn = 1 if self.Jturn == 2 else 2
                        self.value.set("Au tour du joueur " + str(self.Jturn))

                    elif self.choix.get() == 2:
                        self.play = False
                        self.Jturn = 1 if self.Jturn == 2 else 2                        
                        self.value.set("Au tour du joueur " + str(self.Jturn))
                        self.lb2.update_idletasks()

                        self.AI()
                        # self.cg.after(10, self.AI())
                        
                    # print(self.grille)

                    
    def putpiece(self, x):
        cpt = 0
        test = False
        while cpt <= 5 and not test:
            if self.grille[cpt][x] == 0:
                cpt += 1
            else:
                test = True
                
        self.grille[cpt - 1][x] = self.Jturn
        self.dessine(x, cpt - 1)
        self.board += str(x)
        
        
    def AI(self, depht = 6):
        # print(self.grille)
        if self.gameStatus:
            '''possible = [i for i in range(7) if self.grille[0][i] == 0]
            x = random.choice(possible)'''
            if self.Jturn == 1: #rouge
                a = time.perf_counter()
                # x = algo5(self.grille, self.Jturn)
                x = algon_th(self.grille, self.Jturn, self.n, profondeur)
                print(self.Jturn, time.perf_counter() - a)
            else: #jaune
                a = time.perf_counter()
                # x = algo5(self.grille, self.Jturn)
                '''
                if self.n == 4:
                    x = algo5(self.grille, self.Jturn)
                else:
                    x = algon(self.grille, self.Jturn, self.n)'''
                x = algon_th(self.grille, self.Jturn, self.n, profondeur)
                '''
                try:
                    x = AId(self.grille, self.board)
                except Exception as e:
                    x = algo5(self.grille, self.Jturn)
                '''
                print(self.Jturn, time.perf_counter() - a)
                # x = algo5(self.grille, self.Jturn)
            time.sleep(0.2) # voir le jeu se déroulé
                

            # sécurité voir si x valable
            if self.grille[0][x] == 0:
                self.putpiece(x)
                
                #savoir si parti fini
                co = self.gagne()
                # print(co)
                if not self.gameStatus:
                    self.value.set("Le gagnant est le joueur " + str(self.Jturn))
                    for i in co:
                        self.dessinevict(i[1], i[0])
                        time.sleep(0.4)
                        self.cg.update_idletasks()
                    self.inptxt['state'] = 'normal' # réactive la puissance n

                elif not 0 in self.grille[0]:
                    self.gameStatus = False
                    self.value.set("Egalité")
                    self.lb2.update()
                    self.inptxt['state'] = 'normal' # réactive la puissance n
                    self.dessinega()

                
                elif self.choix.get() == 2:
                    self.play = True
                    self.Jturn = 1 if self.Jturn == 2 else 2
                    self.value.set("Au tour du joueur " + str(self.Jturn))
                    self.lb2.update_idletasks()


                elif self.choix.get() == 3:
                    self.play = False
                    self.Jturn = 1 if self.Jturn == 2 else 2
                    self.cg.update_idletasks()
                    
                    self.value.set("Au tour du joueur " + str(self.Jturn))
                    
                    self.lb2.update_idletasks()
                    self.cg.update() # permet de FORCER l'actualisation de l'affichage
                    self.AI()

                    # self.cg.after(10, self.AI())

            else:
                print('non')
                self.AI()
                
    
    def dessine(self, x, y):
        # self.cg.create_oval(25, 25, 50, 50)
        if self.p != [-1, -1]:
            # reset le rond d'avant
            self.cg.create_oval(25 + 110 * self.p[0], 25 + self.p[1] * 110, 25 + 110 * (self.p[0] + 1) - 10, 25 + (self.p[1] + 1) * 110 - 10, fill = "red" if self.Jturn == 2 else "yellow")

        self.p = [x, y]
        
        self.cg.create_oval(25 + 110 * x, 25 + y * 110, 25 + 110 * (x + 1) - 10, 25 + (y + 1) * 110 - 10, fill = "cyan")

        # self.cg.create_oval(25 + 110 * x, 25 + y * 110, 25 + 110 * (x + 1) - 10, 25 + (y + 1) * 110 - 10, fill = "red" if self.Jturn == 1 else "yellow")
        # cercle plus petit pour avoir contour orange
        
        self.cg.create_oval(25 + 110 * x + 10, 25 + y * 110 + 10, 25 + 110 * (x + 1) - 10 -10 , 25 + (y + 1) * 110 - 10 - 10, fill = "red" if self.Jturn == 1 else "yellow", width = 0)

        
        self.cg.update_idletasks() # ou juste update() pour être sûr que le canvas soit à jour


    def dessinevict(self, x, y):
        # cercle vert
        self.cg.create_oval(25 + 110 * x, 25 + y * 110, 25 + 110 * (x + 1) - 10, 25 + (y + 1) * 110 - 10, fill = "lightgreen")
        #cercle couleur init
        self.cg.create_oval(25 + 110 * x + 10, 25 + y * 110 + 10, 25 + 110 * (x + 1) - 10 -10 , 25 + (y + 1) * 110 - 10 - 10, fill = "red" if self.Jturn == 1 else "yellow", width = 0)

        self.cg.update_idletasks()

    def dessinega(self):
        # self.cg["bg"] = "lightgrey"
        rgb = (255, 0, 0)
        print("égalité")
        for x in range(7):
            for y in range(6):
                n = (int(rgb[0] - (x) * (255 /7) ), int(rgb[1] + (y) * (255/6)) , int(rgb[2] + (x) * (255 / 7) ))

                # n = (int(rgb[0] - (x) * (255 /13) - (y) * (255 /11)), int(rgb[1] + (x) * (255 /13) + (y) * (255 /11)), int(rgb[2] + (x) * (255 /13) + (y) * (255 /11)))
                # print(n)
                h = self.from_rgb(n)
                self.cg.create_oval(25 + 110 * x, 25 + y * 110, 25 + 110 * (x + 1) - 10, 25 + (y + 1) * 110 - 10, fill = h)
                time.sleep(0.1)

        
                self.cg.update_idletasks()
        
    def gagne(self):
        for x in range(7):
            y = 0
            while y + 1 <= 5 and self.grille[y][x] == 0:
                y += 1
                
            if self.grille[y][x] == self.Jturn: # savoir si le joueur à bien posé son pion ici en dernier sinon ça ne sert à rien de regarder
                
                # test hori
                k = 0
                while k < (8 - self.n): #pour adpater à self.n #4:
                    if [self.Jturn] * self.n == self.grille[y][k : k + self.n]:
                        self.gameStatus = False
                        return [(y, k + i) for i in range(self.n)] # pour pouvoir dessiner les coordonnéees gagnante
                    k += 1
                    
                # test verti
                if y <= (6 - self.n) and [self.grille[y + k][x] for k in range(self.n)]== [self.Jturn for _ in range(self.n)]:
                    self.gameStatus = False
                    return [ (y + i, x) for i in range(self.n)]
                
                # test diag négatif
                diag = []
                for k in range(6 - y):
                    if x + k < 7 and y + k < 6 and self.grille[y + k][x + k] == self.Jturn:
                            diag.append((y + k, x + k)) 
                    else:
                        break
                for k in range(1, y):
                    if x - k >= 0 and y - k >= 0 and self.grille[y - k][x - k] == self.Jturn:
                            diag.append((y - k, x - k))
                    else:
                        break
                
                if len(diag) >= self.n:
                    self.gameStatus = False
                    return diag
                
                #test diag positif
                diag = []
                for k in range(y + 1):
                    if x + k < 7 and y - k >= 0 and self.grille[y - k][x + k] == self.Jturn:
                            diag.append((y - k, x + k))
                    else:
                        break
                for k in range(1, 6 - y):
                    if x - k >= 0 and y + k < 6 and self.grille[y + k][x - k] == self.Jturn:
                            diag.append((y + k, x - k))
                    else:
                        break
                    
                if len(diag) >= self.n:
                    self.gameStatus = False
                    return diag

    def from_rgb(self, rgb):
        # couleur rgb -> couleur hexa
        return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
    
        # pour python 3.6 - 
        # return '#' + ''.join('{:02X'.format(i) for i in rgb)
    
    
def main(): 
    root = tk.Tk()
    app = Jeu(root) # /!\ assignation nécessaire sinon problème avec checkbox
    root.mainloop()
    
if __name__ == '__main__':
    main()
