import random
import numpy as np
import matplotlib.pyplot as plt



class Grille:

    def __init__(self):
        self.Matrice = np.zeros([10,10], dtype=int)


    # Obtenir chaque longeur de bateau
    def longBateau(self,bateau):
        if bateau == 1:
            return 5
        elif bateau == 2:
            return 4
        elif bateau == 3:
            return 3
        elif bateau == 4:
            return 3
        elif bateau == 5:
            return 2
        else:
            return 0

    def peut_placer(self,grille,bateau,position,direction):
        x = position[0]
        y = position[1]
        l = self.longBateau(bateau)
        # Créer une grille de longueur de navire, chacune case avec une valeur de 0, c'est pour afin de déterminer si les cases placée est entièrement à 0
        tmp = np.zeros(l, dtype=int)


        if direction == 1:
            if (y-l+1) >= 0 or (y+l) <= 10:
                # Comparer la sous-grille tranchée par coordonnées avec tmp, s'il est égal, cela signifie qu'elle n'est pas occupée
                return self.eq(grille[x, y:y+l], tmp) or self.eq(grille[x, y-l+1:y+1], tmp)
            else:
                return False

        if direction == 2:
            if (x+l) <= 10 or (x-l+1) >= 0:
                # Comparer la sous-grille tranchée par coordonnées avec tmp, s'il est égal, cela signifie qu'elle n'est pas occupée
                return self.eq(grille[x:x+l, y], tmp) or self.eq(grille[x-l+1:x+1, y], tmp)
            else:
                return False

    def place(self, grille, bateaux, position, direction):
        x = position[0]
        y = position[1]
        l = self.longBateau(bateaux)
        tmp0 = np.zeros(l, dtype=int)

        if direction == 1: #Placement horizontal
            if self.peut_placer(grille, bateaux, position, direction):
                if (y+l) <= 10 and self.eq(grille[x,y:y+l], tmp0): #Peut être placé et placé horizontalement vers la droite
                    grille[x, y:y+l] = bateaux
                    return grille
                elif (y-l+1) >= 0 and self.eq(grille[x, y-l+1:y+1], tmp0): #Peut être placé et placé horizontalement à gauche
                    grille[x, y-l+1:y+1] = bateaux
                    return grille
            else:  #Impossible de placer, renvoie la grille d'origine
                return grille

        if direction == 2: #Placement vertical
            if self.peut_placer(grille, bateaux, position, direction):
                if (x+l) <= 10 and self.eq(grille[x:x+l, y], tmp0): #Peut être placé et placé verticalement vers le bas
                    grille[x:x+l, y] = bateaux
                    return grille
                elif (x-l+1) >= 0 and self.eq(grille[x-l+1:x+1, y], tmp0): #Peut être placé et placé verticalement vers le haut
                    grille[x-l+1:x+1, y] = bateaux
                    return grille
            else: #Impossible de placer, renvoie la grille d'origine
                return grille


    def place_alea(self, grille, bateau):
        b = True
        while b:
            #Direction et coordonnées aléatoires
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            direction = random.randint(1,2)

            if self.peut_placer(grille, bateau, (x, y), direction):
                self.Matrice = self.place(grille, bateau, (x, y), direction)
                b = False




    def affiche(self, grille):
        plt.imshow(grille)
        plt.show()

    def eq(self, grilleA, grilleB):
        g = np.copy(grilleA)
        g2 = np.copy(grilleB)

        return np.array_equal(g, g2)

    def genere_grille(self):
        #Placer au hasard une liste de navires sur la grille
        for i in range(1, 6):
            self.place_alea(self.Matrice, i)































