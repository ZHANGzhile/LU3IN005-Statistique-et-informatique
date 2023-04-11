from Sous_marin import Sous_marin


def main():
    s = Sous_marin(100, 0.4)
    #print(s.aPriori())
    print("Vous trouvez le sous-marin et le nombre de coups consacrées à l’exploration est de :", s.find())

if __name__ == '__main__':
    main()