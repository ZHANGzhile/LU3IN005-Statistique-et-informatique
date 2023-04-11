import random

import numpy as np

def verifieMatrice(m):
    for i in range(0, len(m)):
        sum = 0
        for j in range(0, len(m[0])):
            sum = sum + m[i][j]
        print(sum)
        if not sum == 1:
            return False
    return True

print(verifieMatrice(np.array([[0.9, 0.1, 0.        ],
       [0.        , 0.9, 0.1],
       [0.1, 0.        , 0.9]])))

d= {1:2,2:3,4:5}
print(list(d.keys()))
print(list(d.values()))
sd = str(0)
print(sd)
title = 'adsf' + str(0) + 'ascadc'
print(title)
"""
if prob > p0[1]:  # si prob > P_0(I), alors on initial l'etat est S, les etats suivant sont S ou I
    chaine.append(0)
    while (len(chaine) < T and boolean):
        prob = rd.uniform(0, 1)
        if prob > A[0][0]:
            chaine.append(1)
            boolean = False  # si l'etat est transforme a I, alors on termine cette boucle, car etats suivants sont I ou R
        else:
            chaine.append(0)
    boolean = True

else:  # si prob < P_0(I), alors on initial l'etat est I, suivant etats sont juste I ou R
    chaine.append(1)

while (len(chaine) < T and boolean):
    prob = rd.uniform(0, 1)
    if prob > A[1][1]:
        chaine.append(2)
        boolean = False  # si l'etat est transforme a R, alors on termine cette boucle, car etats suivants seulement R
    else:
        chaine.append(1)

# si l'etat est R, alors les etats suivants seulment R
while (len(chaine) < T and boolean):
    prob = rd.uniform(0, 1)
    if prob > A[2][0]:
        chaine.append(2)
        boolean = False  # si l'etat est transforme a R, alors on termine cette boucle, car etats suivants seulement R
    else:
        chaine.append(0)
for i in range(len(chaine), T):
    chaine.append(2)

return chaine"""
print(0.15393982808022946+0.1759312320916912+0.6157593123209177)
print(150 * 0.6511627906976757)


def nonConfinementIndividu(etat, longueur, A):
    boolean2 = True
    chaine = [4,5]

    while (len(chaine) <= longueur + 2):
        if etat == 0 or chaine.pop() == 0:  # si l'etat initial est S, les etats suivant sont S ou I
            while (len(chaine) <= longueur + 2 and boolean2):
                prob = random.uniform(0, 1)
                if prob <= A[0][1]:
                    chaine.append(1)
                    boolean2 = False  # si l'etat est transforme a I, alors on termine cette boucle, car etats suivants sont I ou R
                else:
                    chaine.append(0)
            boolean2 = True

        if etat == 1 or chaine.pop() == 1:
            while (len(chaine) <= longueur + 2 and boolean2):
                prob = random.uniform(0, 1)
                if prob <= A[1][2]:
                    chaine.append(2)
                    boolean2 = False  # si l'etat est transforme a R, alors on termine cette boucle, car etats suivants seulement R
                else:
                    chaine.append(1)
            boolean2 = True

        # si l'etat est R, alors les etats suivants sont R ou S
        if etat == 2 or chaine.pop() == 2:
            while (len(chaine) <= longueur + 2 and boolean2):
                prob = random.uniform(0, 1)
                if prob <= A[2][0]:
                    chaine.append(0)
                    boolean2 = False  # si l'etat est transforme a S, alors on retourne le debut
                else:
                    chaine.append(2)
            boolean2 = True

    return chaine[2:]

print(nonConfinementIndividu(2,50,np.array([[0.92,0.08,0],[0,0.93,0.07],[0.02,0,0.98]])))