import numpy as np
import random

class Sous_marin():

    def __init__(self,N,Ps):
        self.N = N
        self.Matrice = np.zeros([N,N], dtype=int)
        self.Ps = Ps

    # set pi
    def aPriori(self):
        g = np.zeros([self.N, self.N], dtype=int)
        n1 = (self.N // 2 - self.N // 3)
        n2 = (self.N // 2 + self.N // 3) - 1
        for i in range(0, self.N):
            for j in range(0, self.N):
                if (j > n1 and j < n2) and (i > n1 and i < n2):
                    g[i][j] = random.randint(70,90)
                else:
                    g[i][j] = random.randint(1, 9)
        sum = np.sum(g)

        return g/sum


    def find(self):
        n1 = (self.N // 2 - self.N // 3)
        n2 = ((self.N // 2 + self.N // 3)-1)
        x = random.randint(n1, n2)
        y = random.randint(n1, n2)
        self.Matrice[x][y] = 1
        g = self.aPriori()
        print("Pi: ", g)
        a = True
        cpt = 0

        while a:
             # set pi
            (i, j) = np.where(g == np.max(g)) # trouver ou est la max pi
            if self.Matrice[i[0]][j[0]] != 1:
                g[i[0]][j[0]] = g[i[0]][j[0]]*(1-self.Ps) # pk = pk*（1-ps）
                cpt += 1
            else:
                cpt += 1
                a = False

        return cpt



