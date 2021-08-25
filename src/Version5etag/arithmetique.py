import numpy as np


class Arithmetique:
    def __init__(self):
        self.c = np.zeros((4, 2))
        self.surf = []

    def Intersection(self, surf1, surf2):
        """Calcul d'intersection de surfaces"""
        p = 0
        for i in range(4):
            self.surf.append(surf1[i, 0])
        xmax = max(self.surf)
        xmin = min(self.surf)
        self.surf = []
        for i in range(4):
            self.surf.append(surf1[i, 1])
        ymax = max(self.surf)
        ymin = min(self.surf)

        for j in range(len(surf1)):
            if xmin <= surf2[j, 0] <= xmax:
                self.c[j, 0] = surf2[j, 0]
            elif surf2[j, 0] < xmin:
                self.c[j, 0] = xmin
                p = p + 1
            elif surf2[j, 0] > xmax:
                self.c[j, 0] = xmax
                p = p + 1

            if ymin <= surf2[j, 1] <= ymax:
                self.c[j, 1] = surf2[j, 1]
            elif surf2[j, 1] < ymin:
                self.c[j, 1] = ymin
                p = p + 1

            elif surf2[j, 1] > ymax:
                self.c[j, 1] = ymax
                p = p + 1

        if p == 8:
            self.c = np.zeros((4, 2))

        C = self.Surface(self.c)
        return C

    def Surface(self, list):
        """Calcul de surface"""
        self.surf = []
        for i in range(4):
            self.surf.append(list[i, 0])
        xmax = max(self.surf)
        xmin = min(self.surf)
        self.surf = []
        for i in range(4):
            self.surf.append(list[i, 1])
        ymax = max(self.surf)
        ymin = min(self.surf)

        surface = (xmax - xmin) * (ymax - ymin)
        return surface
