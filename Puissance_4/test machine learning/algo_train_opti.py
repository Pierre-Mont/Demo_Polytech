import sqlite3
import random
# from algo4inversedepth_2 import algo5
from multiprocessing.pool import ThreadPool





def train(n_episodes):
    # connect avec la db
    conn = sqlite3.connect('training_data.db')
    c = conn.cursor()
    # crée la table si elle n'existe pas
    c.execute('''CREATE TABLE IF NOT EXISTS training_data
                 (board TEXT, action INTEGER, eval REAL, nb INTEGER)''')
    
    for simulation in range(n_episodes):
        # init de la partie
        board = ''
        
        playerb = random.randint(1, 2) #pour savoir qui a commencé pour la boucle de fin
        player = playerb
        
        
        # coup1 = []
        # coup2 = []
        
        coupt = [] # à la fin boucle en fonction index paire ou impaire
        
        
        done = False
        tie = False
        # pour le random
        cdispo = {i:0 for i in range(7)}
        grillen = [[ 0 for _ in range(7)] for _ in range(6)]
        
        # print(simulation)
        while not done and not tie:
            # if len(cdispo) == 0:
            #     print('attention')
            # choisi un mouvement soit aléatoire ou réfléchi (pour s'entrainer)
            action = select_action(board, grillen, cdispo, player, c, epsilon = 0.1) # 0.1
            

            
            # Apply the move
            board += str(action)
            putpiece(grillen, player, action)
            
            # savoir si la game est fini
            done = gagne(grillen, player, action)
            
            # savoir si la game est fini car grille complete
            if not done and len(board) == 42:
                tie = True
            
            # Insert the data into the database
            # c.execute("INSERT INTO training_data VALUES (?,?,?,?)", (board, action, reward))
            
#             if player == 1:
#                 coup1.append((board[:-1], action))
#             else :
#                 coup2.append((board[:-1], action))
            coupt.append((board[:-1], action))


            if done or tie: # on met à jour la table
                # print(simulation, player, done, tie, board)
                # pour le joueur 1
                
                # opti
                
                # regarde si la grille + coup existe
                # b = ','.join("'" + str(i) + "'" for i in coupt)
                b = str(coupt)[1:-1]
                # print(b)
                c.execute("SELECT * FROM training_data WHERE (board, action) IN (" + b + ")")
                tab = c.fetchall()
                
                # récompense suivant les cas
                if tie:
                    rewardp = 0
                    rewardi = 0
                    
                elif player == playerb : # (player == 1 and playerb == 1) or (player == 2 and playerb == 2):
                    rewardp = 2
                    rewardi = -2
                    
                else: # (player == 1 and playerb == 2) or (player == 2 and playerb == 1):
                    rewardp = -2
                    rewardi = 2
                    
                print(simulation, done, player, playerb, rewardp)

                
                coupdb = [(t[0], t[1]) for t in tab]
                
                for i in range(len(coupt)):
                    
                    if i % 2 == 0: # paire
                        
                        if coupt[i] in coupdb: # si le coup est déjà dans la db
                            
                            it = coupdb.index(coupt[i]) # récupères l'indice du coup dans le tableau de la db
                            c.execute("UPDATE training_data SET eval = ?, nb = ? WHERE board = ? AND action = ?", ((tab[it][2] * tab[it][3] + rewardp) / (tab[it][3] + 1), tab[it][3] + 1, tab[it][0], tab[it][1]))
                        
                        else: # on l'ajoute
                            c.execute("INSERT INTO training_data VALUES (?,?,?,?)", (coupt[i][0], coupt[i][1], rewardp, 1))

                    else: # impaire
                        
                        if coupt[i] in coupdb: # coup déjà dans la db
                            
                            it = coupdb.index(coupt[i]) # récupères l'indice du coup dans le tableau de la db
                            c.execute("UPDATE training_data SET eval = ?, nb = ? WHERE board = ? AND action = ?", ((tab[it][2] * tab[it][3] + rewardi) / (tab[it][3] + 1), tab[it][3] + 1, tab[it][0], tab[it][1]))
                        
                        else: #on l'ajoute
                            c.execute("INSERT INTO training_data VALUES (?,?,?,?)", (coupt[i][0], coupt[i][1], rewardi, 1))

                        

                '''
                if player  == 1:
                    reward = 2
                else:
                    reward = -2
                    
                if tie:
                    reward = 0

                # on regard si on a déja joué certains coups auparavant
                b = ','.join("'" + str(i) + "'" for i in [j[0] for j in coup1])
                c.execute("SELECT * FROM training_data WHERE board IN (" + b + ")")
                # print('abc', c.fetchall())
                tab = c.fetchall()
                # print(tab)
                for i in tab:
                    # print(i, coup1, 'a')
                    if (i[0], i[1]) in coup1: # vérifie si le combo grille PLUS pion joué est bien présent
                        c.execute("UPDATE training_data SET eval = ?, nb = ? WHERE board = ? AND action = ?", ((i[2] * i[3] + reward) / (i[3] + 1), i[3] + 1, i[0], i[1]))
                        coup1.remove(coup1[coup1.index((i[0], i[1]))])
                        # print('updatea', i)
                    # coup1.remove((i[0][:-1], coup1[i[0][:-1]][1]))
                
                # sinon on les ajoute
                for i in coup1:
                    c.execute("INSERT INTO training_data VALUES (?,?,?,?)",(i[0], i[1], reward, 1))
                coup1 = []
            
            
                # pour le joueur 2
                if tie:
                    reward = 0
                elif player  == 1:
                    reward = -2
                elif reward != 1:
                    reward = 2

                    
                # on regard si on a déja joué certains coups auparavant
                b = ','.join("'" + str(i) + "'" for i in [j[0] for j in coup2])
                c.execute("SELECT * FROM training_data WHERE board IN (" + b + ")")
                # print('efg', c.fetchall())
                tab = c.fetchall()
                # print(tab)
                for i in tab:
                    # print(i, coup2, 'b')
                    if (i[0], i[1]) in coup2: # vérifie si le combo grille PLUS pion joué est bien présent
                        c.execute("UPDATE training_data SET eval = ?, nb = ? WHERE board = ? AND action = ?", ((i[2] * i[3] + reward) / (i[3] + 1), i[3] + 1, i[0], i[1]))
                        coup2.remove(coup2[coup2.index((i[0], i[1]))])
                        # print('updateb', i)
                    # coup1.remove((i[0][:-1], coup1[i[0][:-1]][1]))
                
                # sinon on les ajoute
                for i in coup2:
                    c.execute("INSERT INTO training_data VALUES (?,?,?,?)",(i[0], i[1], reward, 1))
                coup2 = []  
                '''
                
            player = player * -1 + 3
    
    # Save and close the connection to the database
    conn.commit()
    conn.close()
    return True



def select_action(board, grillen, cdispo, player, c, epsilon):
    if random.random() <= epsilon:

        # if cdispo == {}:
        #     print(cdispo, len(board))
        coup = random.choice(list(cdispo.keys()))
        # print(cdispo, coup)

        # utilisation de l'algo minimax
        # coup = algo5(grillen, player)
        
        cdispo[coup] += 1
        if cdispo[coup] >= 6:
            del(cdispo[coup])
        

        return coup
    
    else : #on cherche dans la db un coup
        try :
            # c.execute("SELECT action FROM training_data WHERE board = " + board)
            c.execute("SELECT action FROM training_data WHERE board = ? ORDER BY eval DESC", (board,))
            coup = c.fetchall()
            # print(coup)
            coup = coup[0][0]
            cdispo[coup] += 1
            if cdispo[coup] >= 6:
                del(cdispo[coup])
            return coup
            
        except Exception as e:
            # print("/!\ Error :", e) # car la grille n'est pas encore existante dans la db
            # if len(cdispo) == 0:
            #     print(cdispo, done, tie)
            
            coup = random.choice(list(cdispo.keys()))
            
            # coup = algo5(grillen, player)
            
            cdispo[coup] += 1
            if cdispo[coup] >= 6:
                del(cdispo[coup])
            return coup
        
def putpiece(grille, player, x):
    cpt = 0
    test = False
    while cpt <= 5 and not test:
        if grille[cpt][x] == 0:
            cpt += 1
        else:
            test = True
            
    grille[cpt - 1][x] = player


    
def gagne(grille, player, action):
    x = int(action)
    y = 0
    # print(grille)
    while y + 1 <= 5 and grille[y][x] == 0:
        y += 1
        
    if grille[y][x] == player: # savoir si le joueur à bien posé son pion ici en dernier sinon ça ne sert à rien de regarder
        
        # test hori
        k = 0
        while k < 4:
            if [player] * 4 == grille[y][k : k + 4]:
                return True
            k += 1
            
        # test verti
        if y <= 2 and [grille[y + k][x] for k in range(4)]== [player for _ in range(4)]:
            return True
        
        # test diag négatif
        diag = []
        for k in range(6 - y):
            if x + k < 7 and y + k < 6 and grille[y + k][x + k] == player:
                    # diag.append(player)
                diag.append((y + k, x + k))
            else:
                break
        for k in range(1, y):
            if x - k >= 0 and y - k >= 0 and grille[y - k][x - k] == player:
                    # diag.append(player)
                diag.append((y - k, x - k))
            else:
                break
        
        if len(diag) >= 4:
            return True
        
        #test diag positif
        diag = []
        for k in range(y + 1):
            if x + k < 7 and y - k >= 0 and grille[y - k][x + k] == player:
                    # diag.append(player)
                diag.append((y - k, x + k))
            else:
                break
            
        for k in range(1, 6 - y):
            if x - k >= 0 and y + k < 6 and grille[y + k][x - k] == player:
                    # diag.append(player)
                diag.append((y + k, x - k))
            else:
                break
            
        if len(diag) >= 4:
            return True
        
    return False
            
            
# print("commencé")

# train(6000)

# print('terminé')










def AIs(grillen, board):
    
    conn = sqlite3.connect('training_data.db')
    c = conn.cursor()

    
    try :
        c.execute("SELECT action FROM training_data WHERE board = ? ORDER BY eval DESC", (board,))
        coup = c.fetchall()

        coup = coup[0][0]

        return coup
        
    except Exception as e:
        print('pif')
        cdispo = [i for i in range(len(grillen[0])) if grillen[0][i] == 0]
        
        coup = random.choice(list(cdispo))

        return coup
    
    conn.close()
    
def AId(grillen, board):
    
    conn = sqlite3.connect('training_data.db')
    c = conn.cursor()


    c.execute("SELECT action FROM training_data WHERE board = ? ORDER BY eval DESC", (board,))
    coup = c.fetchall()

    coup = coup[0][0]

    return coup

    conn.close()

