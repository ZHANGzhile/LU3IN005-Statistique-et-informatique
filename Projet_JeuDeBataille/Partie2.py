from Grille import Grille


class Partie2():

    def __init__(self):
        self.G = Grille()
        self.G.genere_grille()
        self.grille = self.G.Matrice

    #Calculer combien de façons de placer un bateau dans une grille
    def nbUnBateaux(self, grille, bateaux):
        l = self.G.longBateau(bateaux)
        nb = 0
        for i in range(0, grille.shape[0]): # Parcourir sur les lignes
            for j in range(0, grille.shape[0]): # Parcourir chaque élément de chaque ligne
                if (i+l) <= 10 and self.G.peut_placer(grille, bateaux, (j, i), 1): #Si cette coordonnée peut placer ce bateau horizontalement
                    nb = nb+1
                if (j+l) <= 10 and self.G.peut_placer(grille, bateaux, (j, i), 2): #Si cette coordonnée permet de placer ce bateau à la verticale, le nb +1
                    nb = nb+1
        return nb


    def nbUneList(self, grille): # Retouner une borne supérieure simple
        a = 1
        nb = 1
        while a <= 5:
            nb = nb * self.nbUnBateaux(grille, a)
            a += 1
        return nb # nb doit egal à 120*140*160*160*180

    def nbGrille(self):
        g1 = Grille()
        g1.genere_grille()
        g2 = Grille()
        g2.genere_grille()
        cpt = 0
        while not self.G.eq(g1.Matrice, g2.Matrice):
            g2 = Grille()
            g2.genere_grille()
            cpt = cpt + 1
        return cpt

    #bonus
    def nbTotal(self,Nbfois):
        i = 0
        listNb = []
        while i < Nbfois:
            nb = self.nbGrille()
            listNb.append(nb)
            i += 1

        return max(listNb)