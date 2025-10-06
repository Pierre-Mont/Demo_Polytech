from math import inf
from multiprocessing.pool import ThreadPool

grille = [[0] * 7 for _ in range(6)]


def algon_th(grilla, nb, pui, depthinit = 7): #pui -> puissance n
    # global pui #pouvoir l'utiliser à tout moment
    grillecopy = [grilla[i][:] for i in range(6)]  # copie de la grille
    
    def putgrille(grilla, pos, AI):
        i = 0
        grillacopy = [grilla[i][:] for i in range(6)]
        while i + 1 < len(grilla) and grilla[i + 1][pos] == 0:
            i += 1
        if AI:
            grillacopy[i][pos] = nb
        else:
            if nb == 1:
                grillacopy[i][pos] = 2
            else:
                grillacopy[i][pos] = 1
                
        return grillacopy
        # x *-1 +3
    

    def functvictn(grilla, nb):
        tableauall = [0 for i in range(pui - 2)] # création d'un tableau pour stocker les alignement potentielle (1011 -> 3, 121 -> 0, 1100 ->2, 1 -> 0)
                                                # (c'est à dire vérifier si il est bien possible d'en faire une victoire donc que les cases soient libres jusqu'à n - 1 sinon c'eest une victoire donc pas besoins de checker)
        if tableauall == []: #pour pui = 2
            return []

        yhori = []
        for i in range(7): #pour check les derniers pions joué sur chaque colonne
            y = 0
            while y + 1 < len(grilla) and grilla[y][i] == 0:
                y += 1
            if grilla[y][i] == nb: #pour vérifier si c'est bien le pion du joueur qu'on recherche
                
                #hori
                if y not in yhori: # vérifier qu'une fois la ligne
                    
                    if nb*-1+3 in grilla[y][:]:
                        hori = str(grilla[y][:])[1:-1].split(str(nb * -1 + 3)) #pro
                        
                        for c in hori:
                            if len(c.replace(', ','')) == pui:
                                v = len(c.replace(', ', '').replace('0', ''))
                                # print('oui',v, c, 'npn')
                                if v >= len(tableauall):
                                    tableauall[-1] += 1
                                elif v >= 2:
                                    tableauall[v - 2] += 1
                            
                    yhori.append(y)
   
                #vertical
                # matrice(grilla)
                verti = str([grilla[y + k][i] for k in range(6 - y)]).split(str(nb*-1+3))[0] #récupération de la suite de nombrela plus haute
                if len(verti) > 1 and y - (pui - len(verti)) >= 0: #on regarde si il y a encore la place de faire un puissance n (len(verti) + 6 - y <= pui)
                    if len(verti) < pui:
                        tableauall[len(verti) - 2] += 1
                
                
                 #test diago
                #négatif
                diag = []
        
                for o in range(6-y):
                    if i+o<7 and y+o<6 and (grilla[y+o][i+o] == nb or grilla[y+o][i+o] == 0):
                        diag.append(grilla[y+o][i+o])
                    else:
                        break
                            
                for o in range(1,y):
                    if i-o>=0 and y-o>=0 and (grilla[y-o][i-o] == nb or grilla[y-o][i-o] == 0):
                        diag.append(grilla[y-o][i-o])
                    else:
                        break
                    
                if len(diag) >= pui:
                    v = len(str(diag)[1:-1].replace(', ', '').replace('0',''))
                    if v >= 2:
                        if v >= len(tableauall):
                            tableauall[-1] += 1
                        else:
                            tableauall[v - 2] += 1
                    
                #positif
                diag = []
        
                for o in range(y+1):
                    if i+o<7 and y-o>=0 and (grilla[y-o][i+o] == nb or grilla[y-o][i+o] == 0):
                        diag.append(grilla[y-o][i+o])
                    else:
                        break
                    
                for o in range(1,6-y):
                    if i-o>=0 and y+o<6 and (grilla[y+o][i-o] == nb or grilla[y+o][i-o] == 0):
                        diag.append(grilla[y+o][i-o])
                    else:
                        break
                    
                    
                if len(diag) >= pui:
                    v = len(str(diag)[1:-1].replace(', ', '').replace('0',''))
                    if v >= 2:
                        if v >= len(tableauall):
                            tableauall[-1] += 1
                        else:
                            tableauall[v - 2] += 1
        
        # print(tableauall)
        return tableauall

                
    
    def gameOver(grilla,pos):

        i = 0
        while i+1 < len(grilla) and grilla[i][pos]==0:
            i += 1
        
        a = grilla[i][pos]

        #test hori
        k = 0    
        while k < (8 - pui): #pour adpater à pui:
            if [a] * pui == grilla[i][k : k + pui]:
                return True
            k += 1
        
        #test vertical            
        if i <= (6 - pui) and [grilla[i + k][pos] for k in range(pui)] == [a for _ in range(pui)]:
            return True


        #test diago
            #négatif
        diag = []

        for o in range(6-i):
            if pos+o<7 and i+o<6 and grilla[i+o][pos+o] == a:
                diag.append(a)
            else:
                break
                    
        for o in range(1,i):
            if pos-o>=0 and i-o>=0 and grilla[i-o][pos-o] == a:
                diag.append(a)
            else:
                break
            
        if len(diag) >= pui:
            return True
            
        #positif
        diag = []

        for o in range(i+1):
            if pos+o<7 and i-o>=0 and grilla[i-o][pos+o] == a:
                diag.append(a)
            else:
                break
            
        for o in range(1,6-i):
            if pos-o>=0 and i+o<6 and grilla[i+o][pos-o] == a:
                diag.append(a)
            else:
                break
            
        if len(diag) >= pui:
            return True
        
        return False


    def minimax(grilla,profondeur, nb, Max, pos, alpha, beta):
        #print(profondeur)
        #matrice(grilla)
        """
        grilla : c'est la grille
        profondeur : la profondeur de recherche
        nb : le numéro du jouer dans la grilla
        Max : booléan pour savoir si on cherche le max ou le min
        pos : endroit ou l'on pose le pion
        """

        game = gameOver(grilla, pos)
        # print(game, pos, profondeur)
        if game : # or (pui == 2 and depthinit - 1 == profondeur):
            # print('coucou', nb, nb * -1 + 3)
            
            eva = 0
            tab = functvictn(grilla, nb)
            for i in range(len(tab)):
                eva += ((tab[i] * (i + 1) * 100) *1.25)
                
                
            tab = functvictn(grilla, nb * -1 +3)
            for i in range(len(tab)):
                eva -= ((tab[i] * (i + 1) * 100) * 1.25)
                
            eva += (1000 * profondeur * (-1 if Max else 1))
            
            # print('coucouc', eva, nb, Max, profondeur)
            return eva
                            


        if profondeur==1:
            #fonction d'évaluation
                #rajouter functn
            # print('prof', nb, nb * -1 + 3)

            eva = 0
            
            # print('avant')
            
            tab = functvictn(grilla, nb)
            # print('+', tab)
            for i in range(len(tab)):
                eva += ((tab[i] * (i + 1) * 100) *1.25)
                
            tab = functvictn(grilla, nb * -1 +3)
            # print('-', tab)
            for i in range(len(tab)):
                eva -= ((tab[i] * (i + 1) * 100) * 1.25)
            
            # print(eva)
            return eva
                
        #test si la grille est pleine, pour éviter de renvoyé None
        elif not 0 in grilla[0]:
            return 0 
        
        if 0 in grilla[0]:
            
            if Max:
                Eval = -inf
                for p in range(7):
                    if grilla[0][p]==0:
                        Eval = max(Eval,minimax(putgrille(grilla, p, True), profondeur - 1, nb, False, p, alpha, beta))
                            
                        alpha = max(alpha, Eval)
                        if Eval >= beta: 
                            return beta

                return Eval

            else:
                Eval = inf
                for p in range(7):
                    if grilla[0][p]==0:
                        Eval = min(Eval,minimax(putgrille(grilla, p, False), profondeur - 1, nb, True, p, alpha, beta))

                        beta = min(beta, Eval)
                        if Eval <= alpha: 
                            return alpha


                        
                return Eval
        #return random.randint(0,10)f
    

    
    if not 1 in grilla[5] and not 2 in grilla[5]:
        return 3
    
    #lancement algo minimax
    
    pos = [0]*len(grilla[0])
    for i in range(len(grilla[0])):
        if grilla[0][i]==0:
            #pos[i]=minimax(putgrille(grillecopy, i, True), depthinit, nb, False, i, -inf, inf)
            pos[i] = ThreadPool(processes=1).apply_async(minimax, (putgrille(grillecopy, i, True), depthinit, nb, False, i, -inf, inf))
        else:
            pos[i]=-inf
            
    for k in range(len(pos)):
        if pos[k] != -inf:
            pos[k] = pos[k].get()
    
    
    # print(nb, pos)
    return pos.index(max(pos))

def matrice(tab):
    for i in tab:
        print(i)
    print('')






    