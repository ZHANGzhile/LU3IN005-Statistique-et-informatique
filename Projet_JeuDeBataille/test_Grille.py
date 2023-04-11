from Grille import Grille






def main():
    G1 = Grille()
    G1.genere_grille()
    print("La grille 1: ")
    print(G1.Matrice)
    G2 = Grille()
    G2.genere_grille()
    print("La grille 2: ")
    print(G2.Matrice)
    print("Vérifier si les deux grilles sont égales: ", G1.eq(G1, G2))

    # G = Grille()
    # G.place_alea(G.Matrice,1)
    # G.place_alea(G.Matrice,3)
    # print(G.Matrice)

    G1.affiche(G1.Matrice)

if __name__ == '__main__':
    main()



