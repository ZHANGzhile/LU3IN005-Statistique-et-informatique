import numpy as np

from Partie2 import Partie2

def main():
    G = Partie2()
    grille = np.zeros(G.grille.shape, dtype=int)
    # print(G.nbUnBateaux(grille, 2)) # affiche 140
    # print(G.nbUneList(grille)) # affiche 77,414,400,000
    # print(G.nbGrille())

if __name__ == '__main__':
    main()