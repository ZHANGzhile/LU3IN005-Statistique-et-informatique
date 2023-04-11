"""
Groupe 3: 
        Zhang zhile 21201131
        Zhang jiawen 21117173
"""

import math
import utils
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt


def getPrior(data):
    N = len(data['target'])  # Taille totale de l'échantillon
    N1 = 0  # le nombre de target = 1
    for i in data['target']:
        if i == 1:
            N1 += 1

    estimation = N1 / N  # p ~ N1/N
    # par la table, on peut trouve p(-1,96 < z < 1,96) = 0,95
    max5pourcent = estimation + (1.96) * math.sqrt((estimation * (1 - estimation)) / N)
    min5pourcent = estimation - (1.96) * math.sqrt((estimation * (1 - estimation)) / N)

    return {'estimation': estimation,
            "min5pourcent": min5pourcent,
            "max5pourcent": max5pourcent}


class APrioriClassifier(utils.AbstractClassifier):
    def __init__(self):
        pass

    # 2.a
    def estimClass(self, attrs):
        return 1

    # 2.b
    def statsOnDF(self, df):
        N = len(df['target'])
        VP = 0
        VN = 0
        FP = 0
        FN = 0
        for i in range(0, N):
            di = utils.getNthDict(df, i)
            if self.estimClass(di) == 0 and di['target'] == 0:
                VN += 1
            elif self.estimClass(di) == 1 and di['target'] == 1:
                VP += 1
            elif self.estimClass(di) == 1 and di['target'] == 0:
                FP += 1
            else:
                FN += 1

        return {'VP': VP, 'VN': VN, 'FP': FP, 'FN': FN, 'Précision': VP / (VP + FP), 'Rappel': VP / (VP + FN)}


# 3.a
def P2D_l(df, attr):
    N = len(df['target'])
    attr_valeurs = set(df[attr]) # Nombre de toutes les valeurs de cet attr, ex: l'attr thal a 4 valeurs différentes , age a 13 valeurs différentes
    N1 = 0
    d0 = {}
    d1 = {}
    for i in range(0, N):
        di = utils.getNthDict(df, i)  # Données pour un seul échantillon
        if di['target'] == 1:
            N1 += 1
            if di[attr] in d1:  # s'il exsit cette valeur dans d1.keys()
                d1[di[attr]] += 1
            else:
                d1[di[attr]] = 1  # sinon, on initialise cette valeur de l'attr est 1
        else: #target = 0
            if di[attr] in d0:
                d0[di[attr]] += 1
            else:
                d0[di[attr]] = 1
    d1_2 = {}
    d0_2 = {}
    for i in attr_valeurs:
        if i in d1.keys():
            d1_2[i] = d1[i] / N1 # si au moins une échantillon a cette valeur dans target = 1, alors on calcule la probabilité
        else:
            d1_2[i] = 0.0   # sinon, on met 0 dans cette valeur
        if i in d0.keys():
            d0_2[i] = d0[i] / (N - N1) # si au moins une échantillon a cette valeur dans target = 0, alors on calcule la probabilité
        else:
            d0_2[i] = 0.0 # sinon, on met 0 dans cette valeur

    return {1: d1_2, 0: d0_2}


def P2D_p(df, attr):
    N = len(df['target'])
    d = {}
    for i in range(0, N):
        di = utils.getNthDict(df, i) # Données pour un seul échantillon
        if di[attr] in d:
            if di['target'] == 1:
                d[di[attr]][1] += 1
            else:
                d[di[attr]][0] += 1
        else:
            if di['target'] == 1:
                d[di[attr]] = {1: 1, 0: 0}
            else:
                d[di[attr]] = {1: 0, 0: 1}

    for i in d.keys():
        total = d[i][1] + d[i][0]
        d[i][0] = d[i][0] / total
        d[i][1] = d[i][1] / total

    return d


# 3.b
class ML2DClassifier(APrioriClassifier):
    def __init__(self, df, attr):
        self.data = df
        self.attr = attr
        self.donnes = P2D_l(df, attr)

    def estimClass(self, attrs):
        value = attrs[self.attr]
        if self.donnes[1][value] > self.donnes[0][value]:
            return 1
        else:
            return 0


# 3.c
class MAP2DClassifier(APrioriClassifier):
    def __init__(self, df, attr):
        self.data = df
        self.attr = attr
        self.donnes = P2D_p(df, attr)

    def estimClass(self, attrs):
        value = attrs[self.attr]
        if self.donnes[value][1] > self.donnes[value][0]:
            return 1
        else:
            return 0


# 4.1
def nbParams(data, attrs=None):
    d = {}  # key is attr，value is "le nb de valeurs différentes pour cet attr"
    nb = 1
    for i in data.keys():
        l = data[i]
        set_l = set(l)
        d[i] = len(set_l)

    """
    la taille de mémoire = (le nb de valeur du premier attr * le nb de valeur du deuxième attr *.... * 8
    """
    if attrs is not None:
        nb_attrs = len(attrs)
        for i in attrs:
            nb = nb * d[i]
    else:
        nb_attrs = 14
        nb = np.prod(list(d.values()))

    print(nb_attrs, "variable(s) : ", nb * 8, "octets")


# 4.2
def nbParamsIndep(data):
    d = {} # key is attr，value is "le nb de valeurs différentes pour cet attr"
    nb = 1
    for i in data.keys():
        l = data[i]
        set_l = set(l)
        d[i] = len(set_l)

    """
       la taille de mémoire = (le nb de valeur du premier attr + le nb de valeur du deuxième attr + .....) * 8
    """
    for j in data.keys():
        nb = sum(list(d.values()))

    print(len(data.keys()), "variable(s) : ", nb * 8, "octets")


def drawNaiveBayes(df, attr):
    s = ""
    for i in df.keys():
        if i != attr:
            if s == "":
                s = attr + "->" + i
            else:
                s = s + ";" + attr + "->" + i
    return utils.drawGraph(s)


# 5.3
def nbParamsNaiveBayes(data, parent, attrs=None):
    d = {} # key est l'attr，value is "le nb de valeurs différentes pour cet attr"
    for i in data.keys():
        l = data[i]
        set_l = set(l)
        d[i] = len(set_l)

    val_parent = d[parent]
    nb = val_parent

    """
    la taille de mémoire = 
    le nb de valeur du premier attr * le nb de valeur du parent attr * 8 
    + le nb de valeur du deuxième attr * le nb de valeur du parent attr * 8
    + .....
    mais dans les cas l'attr = l'attr parent comme(train,'target',['target']) ou attrs = [] comme(train,'target',[]),
    la taille de mémoire = le nb de valeur du parent attr * 8
    """
    if attrs is not None:
        nb_attrs = len(attrs)
        for i in attrs:
            if i == parent:
                nb = val_parent
            else:
                nb = nb + val_parent * d[i]
    else:
        nb_attrs = 14
        nb = val_parent * sum(list(d.values())) - val_parent

    print(nb_attrs, "variable(s) : ", nb * 8, "octets")


# 5.4
class MLNaiveBayesClassifier(APrioriClassifier):
    def __init__(self, df):
        self.data = df
        self.d = {}
        for i in df.keys():
            self.d[i] = P2D_l(self.data, i)  # on crée un dic où les keys sont les attrs, les valeurs sont P2D_l(self.data, attr)

    def estimProbas(self, df):
        d_individu = {}
        for i in df.keys(): #parcours les attrs
            if i != 'target':
                if i in self.d.keys():
                    if df[i] in self.d[i][1].keys():  # si la valeur de l'attr i de cette personne exsit dans le P2D_l(self.data, i)
                        if d_individu == {}:  # si c'est le premier attr, on l'initialise
                            #d[i] = P2D_l(self.data, i), ex: d[i][1] = {1: 0.03217821782178218, 2: 0.7821782178217822,3: 0.1782178217821782,0: 0.007425742574257425}
                            d_individu = {0: self.d[i][0][df[i]], 1: self.d[i][1][df[i]]}
                        else:
                            #on calcule 𝑃(𝑎𝑡𝑡𝑟1|𝑡𝑎𝑟𝑔𝑒t=1)*𝑃(𝑎𝑡𝑡𝑟2|𝑡𝑎𝑟𝑔𝑒t=1)*𝑃(𝑎𝑡𝑡𝑟3|𝑡𝑎𝑟𝑔𝑒t=1)⋯ et 𝑃(𝑎𝑡𝑡𝑟1|𝑡𝑎𝑟𝑔𝑒t=0)*𝑃(𝑎𝑡𝑡𝑟2|𝑡𝑎𝑟𝑔𝑒t=0)*𝑃(𝑎𝑡𝑡𝑟3|𝑡𝑎𝑟𝑔𝑒t=0)⋯
                            target_1 = d_individu[1] * self.d[i][1][df[i]]
                            target_0 = d_individu[0] * self.d[i][0][df[i]]
                            d_individu = {0: target_0, 1: target_1}
                    else: # si la valeur de l'attr i de cette personne n'exsit pas dans le P2D_l(self.data, i), on retourne {0: 0.0, 1: 0.0}
                        d_individu = {0: 0.0, 1: 0.0}

        return d_individu

    def estimClass(self, attrs):
        d = self.estimProbas(attrs)
        if d[1] > d[0]:
            return 1
        else:
            return 0


class MAPNaiveBayesClassifier(APrioriClassifier):
    def __init__(self, df):
        self.data = df
        self.p_target1 = getPrior(df)['estimation']
        self.d = {}
        for i in df.keys():
            self.d[i] = P2D_l(self.data, i)  # on crée un dic où les keys sont les attrs, les valeurs sont P2D_l(self.data, attr)

    def estimProbas(self, df):
        p_target0 = 1 - self.p_target1
        d_individu = {}
        for i in df.keys():  # parcours les attrs
            if i != 'target':
                if i in self.d.keys():
                    if df[i] in self.d[i][1].keys():  # si la valeur de l'attr i de cette personne exsit dans le P2D_l(self.data, i)

                        if d_individu == {}:  # si c'est le premier attr, on l'initialise
                            # d[i] = P2D_l(self.data, i), ex: d[i][1] = {1: 0.03217821782178218, 2: 0.7821782178217822,3: 0.1782178217821782,0: 0.007425742574257425}
                            # Initialiser d_individu={0:P(attr1|target = 0)*P(target = 0), 1: P(attr1|target = 1)*P(target = 1)}
                            d_individu = {0: self.d[i][0][df[i]] * p_target0, 1: self.d[i][1][df[i]]*self.p_target1}
                        else:
                            # on calcule P(target = 1)*𝑃(𝑎𝑡𝑡𝑟1|𝑡𝑎𝑟𝑔𝑒t=1)*𝑃(𝑎𝑡𝑡𝑟2|𝑡𝑎𝑟𝑔𝑒t=1)*𝑃(𝑎𝑡𝑡𝑟3|𝑡𝑎𝑟𝑔𝑒t=1)⋯ et P(target = 0)*𝑃(𝑎𝑡𝑡𝑟1|𝑡𝑎𝑟𝑔𝑒t=0)*𝑃(𝑎𝑡𝑡𝑟2|𝑡𝑎𝑟𝑔𝑒t=0)*𝑃(𝑎𝑡𝑡𝑟3|𝑡𝑎𝑟𝑔𝑒t=0)⋯
                            target_1 = d_individu[1] * self.d[i][1][df[i]]
                            target_0 = d_individu[0] * self.d[i][0][df[i]]
                            d_individu = {0: target_0, 1: target_1}

                    else:  # si la valeur de l'attr i de cette personne n'exsit pas dans le P2D_l(self.data, i), on retourne {0: 0.0, 1: 0.0}
                        d_individu = {0: 0.0, 1: 0.0}

        if d_individu[0] == 0 and d_individu[1] == 0:
            return {0: 0.0, 1: 0.0}
        else:
            return {0: d_individu[0] / (d_individu[1] + d_individu[0]),
                    1: d_individu[1] / (d_individu[0] + d_individu[1])}

    def estimClass(self, attrs):
        d = self.estimProbas(attrs)
        if d[1] > d[0]:
            return 1
        else:
            return 0


def isIndepFromTarget(df, attr, x):
    N = len(df['target'])
    attr_valeurs = set(df[attr])
    d0 = {}
    d1 = {}
    for i in range(0, N):
        di = utils.getNthDict(df, i)# Données pour un seul échantillon
        if di['target'] == 1:
            if di[attr] in d1: # s'il exsit cette valeur dans d1.keys()
                d1[di[attr]] += 1
            else:
                d1[di[attr]] = 1 # sinon, on initialise cette valeur de l'attr est 1
        else:  # target = 0
            if di[attr] in d0:
                d0[di[attr]] += 1
            else:
                d0[di[attr]] = 1
    d1_2 = {}
    d0_2 = {}
    for i in attr_valeurs:
        if i in d1.keys():
            d1_2[i] = d1[i]
        else:
            d1_2[i] = 0
        if i in d0.keys():
            d0_2[i] = d0[i]
        else:
            d0_2[i] = 0
    # Tout le code ci-dessus est le même que celui de la fonction P2d_l, sauf que le résultat final n'est pas un dic de probabilité, mais un dic de nombre
    # Car ce qu'on a besoin est un table comme
    # target/thal | 0 | 1 | 2 | 3 |
    #       0     |nb1|nb2|nb3|nb4|
    #       1     |nb5|nb6|nb7|nb8|

    value_0 = list(d0_2.values())
    value_1 = list(d1_2.values())
    l = chi2_contingency([value_0, value_1])

    if l[1] > x: # l[1] est "The p-value of the test", ce qu'on a besoin de comparer avec x
        return True
    else:
        return False


class ReducedMLNaiveBayesClassifier(MLNaiveBayesClassifier):
    def __init__(self, df, x):
        self.x = x
        self.data_reduced = df.copy()
        for i in df.keys():
            if i != 'target':
                if isIndepFromTarget(df, i, x):
                    del self.data_reduced[i]
        super().__init__(self.data_reduced)  #on modifie la donnees dans la class MLNaiveBayesClassifier

    def draw(self):
        return drawNaiveBayes(self.data_reduced, "target")


class ReducedMAPNaiveBayesClassifier(MAPNaiveBayesClassifier):
    def __init__(self, df, x):
        self.x = x
        self.data_reduced = df.copy()
        for i in df.keys():
            if i != 'target':
                if isIndepFromTarget(df, i, x):
                    del self.data_reduced[i]
        super().__init__(self.data_reduced)  # on modifie la donnees dans la class MLNaiveBayesClassifier

    def draw(self):
        return drawNaiveBayes(self.data_reduced, "target")


# 7.2
def mapClassifiers(dic, df):

    l_x = []# Liste des coordonnées horizontales(liste de Précision)
    l_y = []# Liste des coordonnées verticals(liste de Rappel)
    for i in dic.keys():
        d = dic[i].statsOnDF(df)
        l_x.append(d['Précision'])
        l_y.append(d['Rappel'])

    print(l_x, l_y)
    plt.scatter(l_x, l_y, marker='x')
    for i in range(len(l_x)):
        plt.text(l_x[i], l_y[i], i+1) #Numéroter chaque point
    plt.show()
