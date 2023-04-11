import random
import numpy as np

from Bataille import Bataille
from Bataille import Grille

class Jouer:

    def __init__(self):
        self.cla = Bataille()
        self.m = np.zeros([10, 10], dtype=int)

    def aleatoire(self):
        cpt = 0
        b = True
        while b:
            x = random.randint(0, 9) # Set des coordonnées aléatoires
            y = random.randint(0, 9)
            if self.cla.grille[x, y] not in [-1, -2]: # Si la case n'a pas été tirée
                cpt += 1
                self.cla.play((x, y))


            if self.cla.victoire():
                b = False
                self.cla.reset()

        return cpt

    """
    Cette fonction consiste à explorer les quatre cases autour de la case tiré
    """
    def FourDirection(self, x, y, grille, type): #type est une liste de l'indentifiants codes des bateaux
        cpt = 0
        # S'il y a un/des bateau(x) dans la direction verticale
        if ((x + 1) <= 9 and grille[x + 1][y] in type) or ((x - 1) >= 0 and grille[x - 1][y] in type):
            if (x + 1) <= 9 and grille[x + 1][y] in type: #la direction vers le bas
                b = True
                i = 0
                while b:
                    if (x + 1 + i) < 10 and grille[x + 1 + i][y] in type:#Si la case suivant vaut l'identifiant des bateaux
                        self.cla.play((x + 1 + i, y)) # On joue cette case
                        self.m[x+1+i][y] = 1 # Pour la version probabiliste simplifiée
                        cpt += 1
                        i += 1
                    else:
                        b = False

            if (x - 1) >= 0 and grille[x - 1][y] in type: # la direction vers le haut
                b = True
                i = 0
                while b:
                    if (x - 1 - i) >= 0 and grille[x - 1 - i][y] in type:
                        self.cla.play((x - 1 - i, y))
                        self.m[x-1-i][y] = 1
                        cpt += 1
                        i = i + 1
                    else:
                        b = False

        # S'il y a un/des bateau(x) dans la direction horizontale
        elif ((y + 1) < 10 and grille[x][y + 1] in type) or ((y - 1) >= 0 and grille[x][y - 1] in type):
            if (y + 1) < 10 and grille[x][y + 1] in type: # la direction vers la droite
                b = True
                i = 0
                while b:
                    if (y + 1 + i) < 10 and grille[x][y + 1 + i] in type:
                        self.cla.play((x, y + 1 + i))
                        self.m[x][y+1+i] = 1
                        cpt += 1
                        i += 1
                    else:
                        b = False

            if (y - 1) >= 0 and grille[x][y - 1] in type: #la direction vers la gauche
                b = True
                i = 0
                while b:
                    if (y - 1 - i) >= 0 and grille[x][y - 1 - i] in type:
                        self.cla.play((x, y - 1 - i))
                        self.m[x][y-1-i] = 1
                        cpt += 1
                        i += 1
                    else:
                        b = False
        return cpt


    def heuristique(self):
        cpt = 0
        a = True
        while a:
            x = random.randint(0, 9)
            y = random.randint(0, 9)

            if self.cla.grille[x][y] not in [-1, -2]: # Si la case n'a pas été tirée
                if self.cla.grille[x][y] == 0:
                    cpt += 1
                    self.cla.play((x, y))
                else: # La case vaut 1 ou 2 ou 3 ou 4 ou 5
                    self.cla.play((x, y))
                    cpt += 1
                    cpt = cpt + self.FourDirection(x, y, self.cla.grille, [1, 2, 3, 4, 5])

            if self.cla.victoire():
                    #print(self.cla.grille)
                    a = False
                    self.cla.reset()
        return cpt


    def PrbSimple(self):
        l = [1, 2, 3, 4, 5]
        cpt = 0
        a = True

        while a:
            b = random.randint(0, len(l)-1)# Nous sélectionnons au hasard un navire dans la liste des navires
            tab = np.zeros([10, 10], dtype=int)# Grille de calcul des probabilités
            long = self.cla.cla.longBateau(l[b])
            tmp = np.zeros(long, dtype=int)
            # On parcoure tout l'échiquier et calcule la probabilité que chaque case puisse avoir ce navire
            for i in range(0, 10):
                for j in range(0, 10):
                    if (i + long) <= 10 and self.cla.cla.eq(self.m[i:i+long, j], tmp):
                        tab[i:i+long, j] = tab[i:i+long, j] + 1
                    if (j + long) <= 10 and self.cla.cla.eq(self.m[i, j:j+long], tmp):
                        tab[i, j:j + long] = tab[i, j:j + long]+1

            (tabx, taby) = np.where(tab == np.max(tab)) # Sélectionne les coordonnées de la grille avec la probabilité la plus élevée

            if self.cla.grille[tabx[0]][taby[0]] == 0:
                self.cla.play((tabx[0], taby[0]))
                self.m[tabx[0]][taby[0]] = -2 # S'il échoue, change la valeur de la case dans m en -2
                cpt += 1

            else: # La case vaut 1 ou 2 ou 3 ou 4 ou 5
                b1 = self.cla.grille[tabx[0]][taby[0]]# Nous explorons quel navire est exactement le case qui frappe
                self.cla.play((tabx[0], taby[0]))
                cpt += 1
                self.m[tabx[0]][taby[0]] = 1 # S'il frappe le navire avec succès , change la valeur de la case dans m en 1
                cpt = cpt + self.FourDirection(tabx[0], taby[0], self.cla.grille, [b1]) # Ici, nous n'explorons ce bateau qu'autour
                del l[l.index(b1)] # Nous supprimerons ce navire de la liste des navires


            if self.cla.victoire() or l == []:
                #print(self.cla.grille)
                self.cla.reset()
                self.m = np.zeros([10, 10], dtype=int)
                a = False

        return cpt

g = Jouer()
i = 0
while i<10:
    g.PrbSimple()
    i+=1
















