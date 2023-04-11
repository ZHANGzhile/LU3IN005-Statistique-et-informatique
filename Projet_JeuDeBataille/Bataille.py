import random
import numpy as np

from Grille import Grille


class Bataille:

    def __init__(self):
        self.cla = Grille()
        self.cla.genere_grille()
        self.grille = self.cla.Matrice

    def play(self,position):
        x = position[0]
        y = position[1]
        if self.grille[x, y] not in [0, -1, -2]:
            self.grille[x, y] = -2  # Si touché, change la case de frappe à -2
        else:
            self.grille[x, y] = -1 # S'il rate, change la grille de tir en -2

    def victoire(self):
        b = self.grille.__contains__(1) or self.grille.__contains__(2) or self.grille.__contains__(3) or self.grille.__contains__(4) or self.grille.__contains__(5)
        return not b

    def reset(self):
        cla = Grille()
        cla.genere_grille()
        self.grille = cla.Matrice





