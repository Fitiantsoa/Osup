import numpy as np


class Geometrie:
    def __init__(self, effort, dnom, inputdata, data_dowel):
        self.NbFixa = data_dowel.get("nbCheville")
        self.data_board_dowel = data_dowel
        self.Lx = data_dowel.get("Lx")
        self.Lz = data_dowel.get("Lz")
        self.sx1 = 0
        self.sz1 = 0
        self.Mx = effort.get("Mx")
        self.Mz = effort.get("Mz")
        self.N = effort.get("N")
        self.T = effort.get("T")
        self.Vx = effort.get("Vx")
        self.Vz = effort.get("Vz")
        self.position_fixing = self.calculation_position_fixing()
        self.PosFix = self.position_fixing[2]
        self.CentreGeo0 = self.position_fixing[0]
        self.CentreGeo1 = self.position_fixing[1]
        self.geometric_center = self.effort_geometric_center()
        self.Mzb = self.geometric_center[4]
        self.Mxb = self.geometric_center[3]
        self.dnom = dnom
        self.ccrN = inputdata.get("ccrN")
        self.scrN = inputdata.get("scrN")
        self.hef = data_dowel.get("hef")
        self.DistFixBord = self.calculation_distance_fixing_edge()[0]
        self.change = self.change_origin("")

    def calculation_position_fixing(self):

        global CentreGeo1, CentreGeo0
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

        elif self.NbFixa == 2:
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

    def change_origin(self, PosCmax2):  # Verifier et correcte
        global PosCmax, PosCmax1

        PosFix_bis = np.zeros((self.NbFixa, 2))
        PosCmax = 0
        PosCmax1 = 0

        if PosCmax2 == "":
            if self.Mxb != 0 and self.Mzb != 0:
                if self.Mxb > 0 and self.Mzb > 0:
                    PosCmax = 0
                    PosCmax1 = self.Lz
                elif self.Mxb > 0 > self.Mzb:
                    PosCmax = self.Lx
                    PosCmax1 = self.Lz
                elif self.Mxb < 0 < self.Mzb:
                    PosCmax = 0
                    PosCmax1 = 0
                elif self.Mxb < 0 and self.Mzb < 0:
                    PosCmax = self.Lx
                    PosCmax1 = 0
            elif self.Mxb != 0 and self.Mzb == 0:
                if self.Mxb > 0:
                    PosCmax = self.Lx / 2
                    PosCmax1 = self.Lz
                else:
                    PosCmax = self.Lx / 2
                    PosCmax1 = 0

            elif self.Mxb == 0 and self.Mzb != 0:
                if self.Mzb > 0:
                    PosCmax = 0
                    PosCmax1 = self.Lz / 2
                else:
                    PosCmax = self.Lx
                    PosCmax1 = self.Lz / 2
        else:
            PosCmax = PosCmax2[0]
            PosCmax1 = PosCmax2[1]

        for i in range(self.NbFixa):
            if self.Mxb != 0 and self.Mzb != 0:
                PosFix_bis[i, 0] = abs(self.PosFix[i, 0] - PosCmax)
                PosFix_bis[i, 1] = abs(self.PosFix[i, 1] - PosCmax1)

            elif self.Mxb != 0 and self.Mzb == 0:
                PosFix_bis[i, 0] = self.PosFix[i, 0] - PosCmax
                PosFix_bis[i, 1] = abs(self.PosFix[i, 1] - PosCmax1)
            elif self.Mxb == 0 and self.Mzb != 0:
                PosFix_bis[i, 0] = abs(self.PosFix[i, 0] - PosCmax)
                PosFix_bis[i, 1] = self.PosFix[i, 1] - PosCmax1

        return PosFix_bis, PosCmax, PosCmax1

    def effort_geometric_center(self):
        Ix = 0
        Iz = 0

        for j in range(self.NbFixa):
            Ix = Ix + (self.PosFix[j, 1] - self.CentreGeo1) ** 2
            Iz = Iz + (self.PosFix[j, 0] - self.CentreGeo0) ** 2
        Iy = Ix + Iz

        Mxb = self.Mx - (self.Lz / 2 - self.CentreGeo1) * (-self.N)
        Tb = self.T + (self.Lz / 2 - self.CentreGeo1) * self.Vx - (self.Lx / 2 - self.CentreGeo0) * self.Vz
        Mzb = self.Mz + (self.Lx / 2 - self.CentreGeo0) * (-self.N)
        #print(Ix, Iy, Iz, Mxb, Mzb, Tb)
        return Ix, Iy, Iz, Mxb, Mzb, Tb

    def calculation_position_edge(self):
        PosBord = np.zeros((2, 2))

        PosBord[0, 0] = self.data_board_dowel.get("dx0") - self.data_board_dowel.get("cx0")
        PosBord[0, 1] = (self.Lx - self.data_board_dowel.get("dx1")) + self.data_board_dowel.get("cx1")

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
        smin = self.data_board_dowel.get("sx0")

        if smin >= self.sx1 != 0:
            smin = self.sx1

        if smin >= self.data_board_dowel.get("sz0") != 0:
            smin = self.data_board_dowel.get("sz0")

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
            "Mxb": self.Mxb,
            "Mzb": self.Mzb,
            "Ix": self.geometric_center[0],
            "Iy": self.geometric_center[1],
            "Iz": self.geometric_center[2],
            "Tb": self.geometric_center[5],
            "PosFix": self.PosFix,
            "CentreGeo0": self.CentreGeo0,
            "CentreGeo1": self.CentreGeo1,
            "DistFixBord": self.DistFixBord,
            "DistFixFix": self.calculation_distance_fixing_fixing(),
            "PosCmax": self.change[1],
            "PosCmax1": self.change[2],
            "PosFix_bis": self.change[0],
            "c": self.calculation_cmin(""),
            "s": self.calculation_smin(),
            "NbFixaBord": self.calculation_distance_fixing_edge()[1]}
