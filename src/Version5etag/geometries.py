import numpy as np


class Geometrie:
    def __init__(self, dnom, inputdata, data_dowel):
        self.NbFixa = int(data_dowel.get("nbCheville"))
        self.data_board_dowel = data_dowel
        self.orientation = data_dowel.get("orientation")
        self.Lx = data_dowel.get("Lx")
        self.Lz = data_dowel.get("Lz")
        self.sx1 = 0
        self.sz1 = 0
        self.position_fixing = self.calculation_position_fixing()
        self.PosFix = self.position_fixing[2]
        self.CentreGeo0 = self.position_fixing[0]
        self.CentreGeo1 = self.position_fixing[1]
        self.dnom = dnom
        self.ccrN = inputdata.get("ccrN")
        self.scrN = inputdata.get("scrN")
        self.hef = data_dowel.get("hef")
        self.DistFixBord = self.calculation_distance_fixing_edge()[0]

    def calculation_position_fixing(self):

        global CentreGeo1, CentreGeo0
        print(self.NbFixa)
        CentreGeo0 = 0
        CentreGeo1 = 0
        PosFix = np.zeros((self.NbFixa, 2))

        if self.NbFixa == 4:
            PosFix[0, 0] = self.data_board_dowel.get("dx0")
            PosFix[0, 1] = self.data_board_dowel.get("dz0")

            PosFix[1, 0] = PosFix[0, 0] + self.data_board_dowel.get("sx0")
            PosFix[1, 1] = PosFix[0, 1]

            PosFix[2, 0] = PosFix[0, 0]
            PosFix[2, 1] = PosFix[0, 1] + self.data_board_dowel.get("sz0")

            PosFix[3, 0] = PosFix[0, 0] + self.data_board_dowel.get("sx0")
            PosFix[3, 1] = PosFix[0, 1] + self.data_board_dowel.get("sz0")

        elif self.NbFixa == 2 and self.orientation == "Vertical":
            PosFix[0, 0] = self.data_board_dowel.get("dz0")
            PosFix[0, 1] = self.data_board_dowel.get("dx0")
            PosFix[1, 0] = PosFix[0, 0] + self.data_board_dowel.get("sz0")
            PosFix[1, 1] = PosFix[0, 1]

        elif self.NbFixa == 2 and self.orientation == "Horizontal":
            PosFix[0, 0] = self.data_board_dowel.get("dx0")
            PosFix[0, 1] = self.data_board_dowel.get("dz0")
            PosFix[1, 0] = PosFix[0, 0] + self.data_board_dowel.get("sx0")
            PosFix[1, 1] = PosFix[0, 1]

        for j in range(self.NbFixa):
            CentreGeo0 = CentreGeo0 + PosFix[j, 0]
            CentreGeo1 = CentreGeo1 + PosFix[j, 1]

        CentreGeo1 = CentreGeo1 / self.NbFixa
        CentreGeo0 = CentreGeo0 / self.NbFixa
        return CentreGeo0, CentreGeo1, PosFix

    def calculation_position_edge(self):
        PosBord = np.zeros((2, 2))

        PosBord[0, 0] = self.data_board_dowel.get("dx0") - self.data_board_dowel.get("cx0")
        PosBord[0, 1] = (self.Lx - self.data_board_dowel.get("dx1")) + self.data_board_dowel.get("cx1")
        print(self.data_board_dowel.get("dz0"), self.data_board_dowel.get("cz0"), self.data_board_dowel)
        PosBord[1, 0] = self.data_board_dowel.get("dz0") - self.data_board_dowel.get("cz0")
        PosBord[1, 1] = (self.Lz - self.data_board_dowel.get("dz1")) + self.data_board_dowel.get("cz1")

        return PosBord

    def calculation_distance_fixing_fixing(self):
        DistFixFix = np.zeros((self.NbFixa, 2, 2))

        for j in range(self.NbFixa):
            DistFixFix[j, 0, 0] = 1000000000000000
            DistFixFix[j, 0, 1] = 1000000000000000
            DistFixFix[j, 1, 0] = 1000000000000000
            DistFixFix[j, 1, 1] = 1000000000000000
            for k in range(self.NbFixa):
                if k != j:
                    if self.PosFix[j, 0] - self.PosFix[k, 0] > 0 and abs(self.PosFix[j, 0] - self.PosFix[k, 0]) <= \
                            DistFixFix[j, 0, 0]:
                        DistFixFix[j, 0, 0] = abs(self.PosFix[j, 0] - self.PosFix[k, 0])
                    elif self.PosFix[j, 0] - self.PosFix[k, 0] < 0 and abs(self.PosFix[j, 0] - self.PosFix[k, 0]) <= \
                            DistFixFix[j, 0, 1]:
                        DistFixFix[j, 0, 1] = abs(self.PosFix[j, 0] - self.PosFix[k, 0])

                    if self.PosFix[j, 1] - self.PosFix[k, 1] > 0 and abs(self.PosFix[j, 1] - self.PosFix[k, 1]) <= \
                            DistFixFix[j, 1, 0]:
                        DistFixFix[j, 1, 0] = abs(self.PosFix[j, 1] - self.PosFix[k, 1])
                    elif self.PosFix[j, 1] - self.PosFix[k, 1] < 0 and abs(self.PosFix[j, 1] - self.PosFix[k, 1]) <= \
                            DistFixFix[j, 1, 1]:
                        DistFixFix[j, 1, 1] = abs(self.PosFix[j, 1] - self.PosFix[k, 1])
            if DistFixFix[j, 0, 0] == 1000000000000000:
                DistFixFix[j, 0, 0] = 0

            if DistFixFix[j, 0, 1] == 1000000000000000:
                DistFixFix[j, 0, 1] = 0

            if DistFixFix[j, 1, 0] == 1000000000000000:
                DistFixFix[j, 1, 0] = 0

            if DistFixFix[j, 1, 1] == 1000000000000000:
                DistFixFix[j, 1, 1] = 0
        return DistFixFix

    def calculation_distance_fixing_edge(self):
        DistFixBord = np.zeros((self.NbFixa, 2, 2))
        self.PosBord = self.calculation_position_edge()
        NbFixBord = np.zeros((self.NbFixa, 1))
        for j in range(self.NbFixa):
            if abs(self.PosFix[j, 0] - self.PosBord[0, 0]) <= 10 * self.hef and abs(self.PosFix[j, 0] - self.PosBord[0, 0]) <= 60 * self.dnom:
                DistFixBord[j, 0, 0] = abs(self.PosFix[j, 0] - self.PosBord[0, 0])
                if DistFixBord[j, 0, 0] <= self.ccrN:
                    NbFixBord[j, 0] = NbFixBord[j, 0] + 1
            else:
                DistFixBord[j, 0, 0] = 1E+15

            if abs(self.PosFix[j, 0] - self.PosBord[0, 1]) <= 10 * self.hef and abs(self.PosFix[j, 0] - self.PosBord[0, 1]) <= 60 * self.dnom:
                DistFixBord[j, 0, 1] = abs(self.PosFix[j, 0] - self.PosBord[0, 1])
                if DistFixBord[j, 0, 1] <= self.ccrN:
                    NbFixBord[j, 0] = NbFixBord[j, 0] + 1
            else:
                DistFixBord[j, 0, 1] = 1E+15

            if abs(self.PosFix[j, 1] - self.PosBord[1, 0]) <= 10 * self.hef and abs(self.PosFix[j, 1] - self.PosBord[1, 0]) <= 60 * self.dnom:
                DistFixBord[j, 1, 0] = abs(self.PosFix[j, 1] - self.PosBord[1, 0])
                if DistFixBord[j, 1, 0] <= self.ccrN:
                    NbFixBord[j, 0] = NbFixBord[j, 0] + 1
            else:
                DistFixBord[j, 1, 0] = 1E+15

            if abs(self.PosFix[j, 1] - self.PosBord[1, 1]) <= 10 * self.hef and abs(self.PosFix[j, 1] - self.PosBord[1, 1]) <= 60 * self.dnom:
                DistFixBord[j, 1, 1] = abs(self.PosFix[j, 1] - self.PosBord[1, 1])
                if DistFixBord[j, 1, 1] <= self.ccrN:
                    NbFixBord[j, 0] = NbFixBord[j, 0] + 1
            else:
                DistFixBord[j, 1, 1] = 1E+15
        return DistFixBord, NbFixBord

    def calculation_smin(self):
        global smin
        self.orientation = self.data_board_dowel.get("orientation")
        if self.NbFixa == 2 and self.orientation == "Vertical":
            smin = self.data_board_dowel.get("sz0")
        elif self.NbFixa == 2 and self.orientation == "Horizontal":
            smin = self.data_board_dowel.get("sx0")
        elif self.NbFixa == 4:
            smin = self.data_board_dowel.get("sx0")

            if smin >= self.sx1 != 0:
                smin = self.sx1

            if smin >= float(self.data_board_dowel.get("sz0")) != 0:
                smin = float(self.data_board_dowel.get("sz0"))

            if smin >= self.sz1 != 0:
                smin = self.sz1

        return smin

    def calculation_cmin(self, j):
        if j == "":
            cmin = self.data_board_dowel.get("cx0")

            if self.data_board_dowel.get("cx1") <= cmin:
                cmin = self.data_board_dowel.get("cx1")

            if self.data_board_dowel.get("cz0") <= cmin:
                cmin = self.data_board_dowel.get("cz0")

            if self.data_board_dowel.get("cz1") <= cmin:
                cmin = self.data_board_dowel.get("cz1")

        else:
            if self.DistFixBord[j, 0, 0] <= self.DistFixBord[j, 0, 1]:
                cmin = self.DistFixBord[j, 0, 0]
            else:
                cmin = self.DistFixBord[j, 0, 1]

            if self.DistFixBord[j, 1, 0] <= cmin:
                cmin = self.DistFixBord[j, 1, 0]
            elif self.DistFixBord[j, 1, 1] <= cmin:
                cmin = self.DistFixBord[j, 1, 1]

        return cmin

    def inertia(self):
        return {
            "PosFix": self.matrix_into_list(self.PosFix),
            "CentreGeo0": self.CentreGeo0,
            "CentreGeo1": self.CentreGeo1,
            "DistFixBord": self.list_matrix_into_list(self.DistFixBord),
            "DistFixFix": self.list_matrix_into_list(self.calculation_distance_fixing_fixing()),
            "c": self.calculation_cmin(""),
            "s": self.calculation_smin(),
            "NbFixaBord": self.vector_into_list(self.calculation_distance_fixing_edge()[1])}

    def matrix_into_list(self, matrix):
        list = []
        for i in range(len(matrix)):
            for j in range(2):
                list.append(matrix[i, j])
        return list

    def list_matrix_into_list(self, matrix):
        list = []
        for i in range(len(matrix)):
            for j in range(2):
                for k in range(2):
                    list.append(matrix[i, j, k])
        return list

    def vector_into_list(self, matrix):
        list = []
        for i in range(len(matrix)):
            for j in range(1):
                list.append(matrix[i, j])
        return list

