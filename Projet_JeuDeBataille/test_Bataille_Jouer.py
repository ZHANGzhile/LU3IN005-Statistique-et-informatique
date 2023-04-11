import numpy as np

from Bataille import Bataille
import matplotlib.pyplot as plt

from Jouer import Jouer

"""
B = Bataille()
print(B.grille)
B.play((3,5))
print("******************")
B.reset()
print(B.grille)
print(B.grille[0][5])"""

def main():

    J = Jouer()
    i=0
    j=0
    k=0
    lA = []
    lH = []
    lP = []

    while k < 500:
        cptP = J.PrbSimple()
        print("la ", k, "-eme foi de la version probabilite simplie: ", cptP)
        lP.append(cptP)
        k += 1

    while i < 1000:
        cptA = J.aleatoire()
        print("la ", i, "-eme foi de la version aleatoire: ", cptA)
        lA.append(cptA)
        i += 1

    while j < 1000:

        cptH = J.heuristique()
        print("la ", j, "-eme foi de la version heuristique: ", cptH)
        lH.append(cptH)
        j += 1


    coupsA = len(list(set(lA)))
    coupsH = len(list(set(lH)))
    coupsP = len(list(set(lP)))
    print("la moyenne de la version aleatoire: ", np.mean(lA))
    print("la moyenne de la version heuristique: ", np.mean(lH))
    print("la moyenne de version prbSimple: ", np.mean(lP))


    fig = plt.figure(figsize=(15, 5))
    axs = []
    axs.append(fig.add_subplot(131))
    axs[0].hist(lA, bins=coupsA, rwidth=0.8)
    axs[0].set_xlabel("nombre de coups")
    axs[0].set_ylabel("occurrence")
    axs[0].set_title("version aleatoire")

    axs.append(fig.add_subplot(132))
    axs[1].hist(lH, bins=coupsH, rwidth=0.8)
    axs[1].set_xlabel("nombre de coups")
    axs[1].set_ylabel("occurrence")
    axs[1].set_title("version heuristique")

    axs.append(fig.add_subplot(133))
    axs[2].hist(lP, bins=coupsP, rwidth=0.8)
    axs[2].set_xlabel("nombre de coups")
    axs[2].set_ylabel("occurrence")
    axs[2].set_title("version prbsimple")

    plt.subplots_adjust(hspace=0.1, wspace=0.3)# 调整子图间隔

    plt.show()


if __name__ == '__main__':
    main()