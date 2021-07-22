from mathematiques import Mathematique
import numpy as np
import math


class CalculationEffort:
    def __init__(self, inputdataaster):
        self.effort = inputdataaster.get("effort")
        self.N = self.effort.get("N")
        self.Mx = self.effort.get("Mx")
        self.Mz = self.effort.get("Mz")
        self.Vx = self.effort.get("Vx")
        self.Vz = self.effort.get("Vz")

        self.inertia = inputdataaster.get("inertia")
        self.Mzb = self.inertia.get("Mzb")
        self.Mxb = self.inertia.get("Mxb")
        self.PosFix = self.inertia.get("PosFix")
        self.CentreGeo1 = self.inertia.get("CentreGeo1")
        self.CentreGeo0 = self.inertia.get("CentreGeo0")
        self.Ix = self.inertia.get("Ix")
        self.Iy = self.inertia.get("Iy")
        self.Iz = self.inertia.get("Iz")
        self.Tb = self.inertia.get("Tb")
        self.PosCmax = self.inertia.get("PosCmax")
        self.PosCmax1 = self.inertia.get("PosCmax1")
        self.PosFix_bis = self.inertia.get("PosFix_bis")

        self.NbFixa = inputdataaster.get("NbFixa")
        self.eN = [0, 0]

        self.data_board_dowel = inputdataaster.get("data_board_dowel")
        self.Lx = self.data_board_dowel.get("Lx")
        self.Lz = self.data_board_dowel.get("Lz")

        self.Vedx = np.zeros((self.NbFixa, 1))
        self.Vedz = np.zeros((self.NbFixa, 1))
        self.Ved = np.zeros((self.NbFixa, 1))
        self.NEd = np.zeros((self.NbFixa, 1))

        self.inputdata = inputdataaster.get("inputdata")
        self.nd = self.inputdata.get("nd")
        self.Ar = self.inputdata.get("Ar")

        self.NbFixTraction = 0
        self.NEdg = 0

    def traction(self):
        CentreGeoTrac0 = 0
        CentreGeoTrac1 = 0
        self.CentreGrav0 = 0
        self.CentreGrav1 = 0

        if self.Mx != 0 and self.Mz != 0:
            if abs(self.Mx / self.Mz) < 0.01:
                Mx = np.sign(self.Mx) * self.Mz * 0.01
                Mx = Mx / 1000
                print("Mx est trop faible par rapport à Mz, il est ramené à 1% de Mz")

            elif abs(self.Mz / self.Mx) < 0.01:
                Mz = np.sign(self.Mz) * self.Mx * 0.01
                Mz = Mz / 1000
                print("Mz est trop faible par rapport à Mx, il est ramené à 1% de Mx")

        if self.N == 0 and self.Mx == 0 and self.Mz == 0:
            dico = {"NEd": self.NEd,
                    "NEdg": self.NEdg,
                    "z": 0,
                    "eN": self.eN,
                    "CEd": 0}
            print(dico)
            return dico

        if self.Mxb == 0 or self.Mzb == 0:
            Monoaxial = self.calculation_monoaxial()
            get_error = self.get_error
            if get_error is True:
                return
            self.TypeCompression = Monoaxial[0]
            if self.TypeCompression == "Compression partielle":
                self.NbFixTraction = Monoaxial[2]
                self.NEd = Monoaxial[1]
                self.NEdg = Monoaxial[3]
                self.PosCEd = Monoaxial[4]
                self.CEd = Monoaxial[5]
            elif self.TypeCompression == "Pas de compression":
                self.NEd = Monoaxial[1]
                self.NEdg = Monoaxial[2]
                self.CEd = 0
            elif self.TypeCompression == "Compression totale":
                self.CEd = Monoaxial[1]
                self.NEdg = Monoaxial[2]

        else:
            Biaxial = self.calculation_biaxial()

            get_error = self.get_error
            if get_error is True:
                return
            self.TypeCompression = Biaxial[0]
            if self.TypeCompression == "Compression partielle":
                self.NbFixTraction = Biaxial[2]
                self.NEd = Biaxial[1]
                self.NEdg = Biaxial[3][0]
                self.PosCEd = Biaxial[4]
                self.CEd = Biaxial[5]
            elif self.TypeCompression == "Pas de compression":
                self.CEd = 0
                self.NEd = Biaxial[1]
                self.NEdg = Biaxial[2]
            elif self.TypeCompression == "Compression totale":
                self.CEd = Biaxial[1]

        if self.NbFixTraction > 0:
            for j in range(self.NbFixa):
                if self.NEd[j, 0] > 0:
                    CentreGeoTrac0 = CentreGeoTrac0 + self.PosFix[j, 0]
                    CentreGeoTrac1 = CentreGeoTrac1 + self.PosFix[j, 1]
                    self.CentreGrav0 = self.CentreGrav0 + self.NEd[j, 0] * self.PosFix[j, 0]
                    self.CentreGrav1 = self.CentreGrav1 + self.NEd[j, 0] * self.PosFix[j, 1]

            CentreGeoTrac0 = CentreGeoTrac0 / self.NbFixTraction
            CentreGeoTrac1 = CentreGeoTrac1 / self.NbFixTraction
            self.CentreGrav0 = self.CentreGrav0 / self.NEdg
            self.CentreGrav1 = self.CentreGrav1 / self.NEdg

        eN0 = round(abs(CentreGeoTrac0 - self.CentreGrav0), 1)
        if eN0 < 0.0000000001:
            eN0 = 0

        eN1 = round(abs(CentreGeoTrac1 - self.CentreGrav1), 1)
        if eN1 < 0.0000000001:
            eN1 = 0

        self.eN[0] = eN0
        self.eN[1] = eN1

        if self.TypeCompression == "Compression partielle" and self.NbFixTraction > 0:
            self.z = math.sqrt((self.PosCEd[0] - self.CentreGrav0) ** 2 + (self.PosCEd[1] - self.CentreGrav1) ** 2)

        elif self.TypeCompression == "Pas de compression" or self.TypeCompression == "Compression totale":
            self.z = 0

        dico = {"NEd": self.NEd,
                "NEdg": self.NEdg,
                "z": self.z,
                "eN": self.eN,
                "CEd": self.CEd}
        print(dico)
        #print(self.CentreGrav0, self.CentreGrav1)
        return dico

    def shearing(self):

        VEdgx = 0
        VEdgz = 0
        eV0 = 0
        eV1 = 0

        for j in range(self.NbFixa):
            self.Vedx[j, 0] = self.Vx / self.NbFixa - (self.CentreGeo1 - self.PosFix[j, 1]) * self.Tb / self.Iy
            self.Vedz[j, 0] = self.Vz / self.NbFixa - (self.PosFix[j, 0] - self.CentreGeo0) * self.Tb / self.Iy
            self.Ved[j, 0] = (self.Vedx[j, 0] ** 2 + self.Vedz[j, 0] ** 2) ** (1 / 2)

            VEdgx = VEdgx + self.Vedx[j, 0]
            VEdgz = VEdgz + self.Vedz[j, 0]

        VEdg = math.sqrt(VEdgx ** 2 + VEdgz ** 2)
        for j in range(self.NbFixa):
            eV0 = eV0 + (self.PosFix[j, 0] - self.CentreGeo0) * self.Vedz[j, 0]

            if np.sign(self.Vedz[0, 0]) != np.sign(self.Vedz[j, 0]):
                self.kz = -1
            else:
                self.kz = 1
            eV1 = eV1 + (self.PosFix[j, 1] - self.CentreGeo1) * self.Vedx[j, 0]

            if np.sign(self.Vedx[0, 0]) != np.sign(self.Vedx[j, 0]):
                self.kx = -1
            else:
                self.kx = 1

        if abs(VEdgz) > 0.000000001 and self.kz != -1:
            eV0 = abs(eV0 / VEdgz)
        else:
            eV0 = 0
        if abs(VEdgx) > 0.000000001 and self.kx != -1:
            eV1 = abs(eV1 / VEdgx)
        else:
            eV1 = 0
        if abs(VEdg) < 0.000000001:
            VEdg = 0

        dico = {"VEdg": VEdg,
                "Vedx": self.Vedx,
                "Vedz": self.Vedz,
                "VEdgx": VEdgx,
                "VEdgz": VEdgz,
                "eV0": eV0,
                "eV1": eV1,
                "Ved": self.Ved}
        print(dico)
        #print(self.CentreGeo1, self.CentreGeo0)
        return dico

    def calculation_biaxial(self):
        global k, alpha, lref, pm
        self.errorOccured = False
        self.NbFixTraction = 0
        Nedg = 0
        L = np.zeros((self.NbFixa, 1))
        self.Convergence = False

        k3 = 0

        if self.PosCmax == 0 and self.PosCmax1 == 0:
            k3 = 1
        elif self.PosCmax == self.Lx and self.PosCmax1 == 0:
            k3 = 2
        elif self.PosCmax == 0 and self.PosCmax1 == self.Lz:
            k3 = 3
        elif self.PosCmax == self.Lx and self.PosCmax1 == self.Lz:
            k3 = 4

        TypeCompression = self.state_compression_board()
        if TypeCompression == "Compression totale":
            CEd = abs(self.N)
            listCEd = []
            listCEd.append(CEd)
            return TypeCompression, CEd

        elif TypeCompression == "Pas de compression":
            a = self.calculation_traction_without_compression()
            NEd = a[0]
            NEdg = a[1]
            return TypeCompression, NEd, NEdg

        k2 = 0
        lref0 = 0.1
        lrefp = 1

        if self.Ix != 0:
            alpha0 = math.atan(abs((self.Mzb / self.Mxb) * (self.Ix / self.Iz)))
        else:
            alpha0 = math.atan(abs(self.Mzb / self.Mxb))

        while self.Convergence is False and k2 < 5:
            if k2 == 1 and k3 != k2:
                self.PosCmax = 0
                self.PosCmax1 = 0
                self.PosFix_bis = self.geometrie.change_origin(self.PosCmax)
            elif k2 == 2 and k3 != k2:
                self.PosCmax = self.Lx
                self.PosCmax1 = 0
                self.PosFix_bis = self.geometrie.change_origin(self.PosCmax)
            elif k2 == 3 and k3 != k2:
                self.PosCmax = 0
                self.PosCmax1 = self.Lz
                self.PosFix_bis = self.geometrie.change_origin(self.PosCmax)
            elif k2 == 4 and k3 != k2:
                self.PosCmax = self.Lx
                self.PosCmax1 = self.Lz
                self.PosFix_bis = self.geometrie.change_origin(self.PosCmax)
            k1 = 0
            while self.Convergence is False and lref0 + k1 * lrefp < math.sin(alpha0 + math.atan(self.Lz / self.Lx)) * \
                    math.sqrt(self.Lx ** 2 + self.Lz ** 2):
                alpha = alpha0
                lref = lref0 + k1 * lrefp
                k = self.newton_biaxial(self.PosFix_bis, alpha, lref)

                k1 = k1 + 1
            pm = k[0]
            alpha = k[1]
            lref = k[2]
            k2 = k2 + 1

        if self.Convergence is False:
            print("La méthode de Newton n'a pas convergée")
            self.errorOccured = True
            return self.errorOccured

        L = self.distance_dowel_biaxial(self.PosFix_bis, alpha, lref)

        for j in range(self.NbFixa):
            self.NEd[j, 0] = pm * self.nd * self.Ar * L[j] / lref
            Nedg = Nedg + self.NEd[j]
            if self.NEd[j, 0] > 0:
                self.NbFixTraction = self.NbFixTraction + 1

        compression = self.calculation_compression(pm, alpha, lref, self.PosCmax, self.PosCmax1)
        compression1 = compression[0]
        CEd = compression[1]

        return TypeCompression, self.NEd, self.NbFixTraction, Nedg, compression1, CEd

    def calculation_compression(self, pm, alpha, lref, PosCmax, PosCmax1):
        global PosCEd1, PosCEd, listCEd
        self.Nt_u = 0
        self.Nt_d = 0
        self.G_d0 = 0
        self.G_d1 = 0
        self.G_u0 = 0
        self.G_u1 = 0

        if self.Mxb != 0 and self.Mzb == 0:
            PosCEd0 = self.Lx / 2
            PosCEd1 = lref / 3
            CEd = 0.5 * self.Lx * lref * pm
            if PosCmax1 > 0:
                PosCEd1 = self.Lz - PosCEd1

        elif self.Mzb != 0 and self.Mxb == 0:
            PosCEd1 = self.Lz / 2
            PosCEd0 = lref / 3
            CEd = 0.5 * self.Lz * lref * pm
            if PosCmax > 0:
                PosCEd0 = self.Lx - PosCEd0
        else:
            L = np.zeros((self.NbFixa - 1, 1))
            c0 = 0
            c1 = 0
            c = np.array([c0, c1])
            res = self.triangle_compression(c, pm, alpha, lref)
            Nt = res[0]
            G0 = res[1]
            G1 = res[2]
            res = np.zeros((3, 1))

            if lref > self.Lx * math.sin(alpha) or lref > self.Lz * math.cos(alpha):
                res = self.equation_straight_line_biaxial(alpha, lref)
                self.A0 = res[0]
                self.A1 = res[1]
                self.A2 = res[2]
                res = np.zeros((3, 1))

            if lref > self.Lx * math.sin(alpha):
                C_d0 = self.Lx
                C_d1 = 0
                lt_d = abs(self.A0 * C_d0 + self.A1 * C_d1 + self.A2) / math.sqrt(self.A0 ** 2 + self.A1 ** 2)
                pt_d = (lt_d / lref) * pm
                C_d = np.array([C_d0, C_d1])
                res = self.triangle_compression(C_d, pt_d, alpha, lt_d)
                self.Nt_d = res[0]
                self.G_d0 = res[1]
                self.G_d1 = res[2]
                res = np.zeros((3, 1))

            if lref > self.Lz * math.cos(alpha):
                C_u0 = 0
                C_u1 = self.Lz
                lt_u = abs(self.A0 * C_u0 + self.A1 * C_u1 + self.A2) / math.sqrt(self.A0 ** 2 + self.A1 ** 2)
                pt_u = (lt_u / lref) * pm
                C_u = np.array([C_u0, C_u1])
                res = self.triangle_compression(C_u, pt_u, alpha, lt_u)
                self.Nt_u = res[0]
                self.G_u0 = res[1]
                self.G_u1 = res[2]
                res = np.zeros((3, 1))

            CEd = Nt - self.Nt_d - self.Nt_u
            PosCEd0 = (G0 * Nt - self.G_d0 * self.Nt_d - self.G_u0 * self.Nt_u) / CEd
            PosCEd1 = (G1 * Nt - self.G_d1 * self.Nt_d - self.G_u1 * self.Nt_u) / CEd
            if PosCmax > 0:
                PosCEd0 = self.Lx - PosCEd0
            if PosCmax1 > 0:
                PosCEd1 = self.Lz - PosCEd1

        PosCEd = np.array((PosCEd0, PosCEd1))
        listCEd = []
        listCEd.append(CEd)
        return PosCEd, CEd

    def triangle_compression(self, c, pm, alpha, lref):
        d = lref / math.sin(alpha)

        Nt = (1 / 6) * math.tan(alpha) * pm * d ** 2

        G0 = c[0] + d / 4
        G1 = c[1] + d * math.tan(alpha) / 4
        #print(c, pm, alpha, lref)
        return np.array([Nt, G0, G1])

    def equation_straight_line_biaxial(self, alpha, lref):

        if self.Lx * math.sin(alpha) <= lref <= self.Lz * math.cos(alpha):
            d2 = lref / math.cos(alpha)
            q = math.sqrt(d2 ** 2 - lref ** 2)
            s = self.Lx / math.cos(alpha)
            d = math.sqrt(lref ** 2 + (s - q) ** 2)
            d1 = math.sqrt(d ** 2 - self.Lx ** 2)
            A0 = (d2 - d1) / self.Lx
            A1 = 1
            A2 = -d2

        elif lref <= self.Lx * math.sin(alpha) and lref >= self.Lz * math.cos(alpha):
            d2 = lref / math.sin(alpha)
            q = math.sqrt(d2 ** 2 - lref ** 2)
            s = self.Lz / math.sin(alpha)
            d = math.sqrt(lref ** 2 + (s - q) ** 2)
            d1 = math.sqrt(d ** 2 - self.Lz ** 2)
            A0 = 1
            A1 = -(d1 - d2) / self.Lz
            A2 = -d2

        else:
            d1 = lref / math.sin(alpha)
            d2 = d1 * math.tan(alpha)
            A0 = d2
            A1 = d1
            A2 = -d1 * d2

        return np.array([A0, A1, A2])

    def distance_dowel_biaxial(self, PosFix_bis, alpha, lref):
        L = np.zeros((self.NbFixa, 1))

        res = self.equation_straight_line_biaxial(alpha, lref)
        A0 = res[0]
        A1 = res[1]
        A2 = res[2]

        for j in range(self.NbFixa):
            if A0 * PosFix_bis[j, 0] + A1 * PosFix_bis[j, 1] + A2 <= 0:
                L[j, 0] = 0
            else:
                L[j, 0] = abs(A0 * PosFix_bis[j, 0] + A1 * PosFix_bis[j, 1] + A2) / math.sqrt(A0 ** 2 + A1 ** 2)
        return L

    def systeme_biaxial(self, PosFix_bis, pm, alpha, lref):  # Equilibre statique
        L = np.zeros((self.NbFixa, 1))
        self.Nt_u = 0
        self.Nt_d = 0
        self.G_d0 = 0
        self.G_d1 = 0
        self.G_u0 = 0
        self.G_u1 = 0
        #print(PosFix_bis, pm, alpha, lref)
        c0 = 0
        c1 = 0
        c = np.array([c0, c1])
        res = self.triangle_compression(c, pm, alpha, lref)
        Nt = res[0]
        G0 = res[1]
        G1 = res[2]
        #print(res)
        if lref > self.Lx * math.sin(alpha) or lref > self.Lz * math.cos(alpha):
            res = self.equation_straight_line_biaxial(alpha, lref)
            self.A0 = res[0]
            self.A1 = res[1]
            self.A2 = res[2]

        if lref > self.Lx * math.sin(alpha):
            C_d0 = self.Lx
            C_d1 = 0
            lt_d = abs(self.A0 * C_d0 + self.A1 * C_d1 + self.A2) / math.sqrt(self.A0 ** 2 + self.A1 ** 2)
            pt_d = (lt_d / lref) * pm
            C_d = np.array([C_d0, C_d1])
            res = self.triangle_compression(C_d, pt_d, alpha, lt_d)
            self.Nt_d = res[0]
            self.G_d0 = res[1]
            self.G_d1 = res[2]

        if lref > self.Lz * math.cos(alpha):
            C_u0 = 0
            C_u1 = self.Lz
            lt_u = abs(self.A0 * C_u0 + self.A1 * C_u1 + self.A2) / math.sqrt(self.A0 ** 2 + self.A1 ** 2)
            pt_u = (lt_u / lref) * pm
            C_u = np.array([C_u0, C_u1])
            res = self.triangle_compression(C_u, pt_u, alpha, lt_u)
            self.Nt_u = res[0]
            self.G_u0 = res[1]
            self.G_u1 = res[2]

        L = self.distance_dowel_biaxial(PosFix_bis, alpha, lref)

        Suml = 0
        Sumlz = 0
        Sumlx = 0

        for j in range(self.NbFixa):
            Suml = Suml + L[j, 0]
            Sumlz = Sumlz + L[j, 0] * (self.Lz / 2 - self.PosFix[j, 1])
            Sumlx = Sumlx + L[j, 0] * (self.PosFix[j, 0] - self.Lx / 2)

        #print(Suml, Sumlx, Sumlz)

        if self.PosCmax == 0 and self.PosCmax1 == 0:
            self.A11 = -1
            self.A21 = -1

        elif self.PosCmax == self.Lx and self.PosCmax1 == 0:
            self.A11 = -1
            self.A21 = 1

        elif self.PosCmax == 0 and self.PosCmax1 == self.Lz:
            self.A11 = 1
            self.A21 = -1

        elif self.PosCmax == self.Lx and self.PosCmax1 == self.Lz:
            self.A11 = 1
            self.A21 = 1

        f0 = Nt - self.Nt_d - self.Nt_u - (self.nd * self.Ar * pm * Suml / lref) - self.N
        f1 = -self.A11 * ((self.Lz / 2 - G1) * Nt - (self.Lz / 2 - self.G_d1) * self.Nt_d - (
                self.Lz / 2 - self.G_u1) * self.Nt_u) - self.nd * self.Ar * pm * Sumlz / lref + self.Mx  # Ar : section resistante à chercher
        f2 = -self.A21 * ((G0 - self.Lx / 2) * Nt - (self.G_d0 - self.Lx / 2) * self.Nt_d - (
                self.G_u0 - self.Lx / 2) * self.Nt_u) - self.nd * self.Ar * pm * Sumlx / lref + self.Mz
        f = np.array([f0, f1, f2])
        #print(Nt, self.Nt_d, self.Nt_u, self.nd, self.Ar, pm, lref, self.N)
        return f

    def calculation_jocobien_biaxial(self, PosFix_bis, pm, alpha, lref, d_pm, d_alpha, d_lref):
        F_d = self.systeme_biaxial(PosFix_bis, pm + d_pm, alpha, lref)
        F_g = self.systeme_biaxial(PosFix_bis, pm - d_pm, alpha, lref)
        F_dpm = np.zeros((3, 1))

        for j in range(3):
            F_dpm[j, 0] = (F_d[j] - F_g[j]) / (2 * d_pm)

        F_d = self.systeme_biaxial(PosFix_bis, pm, alpha + d_alpha, lref)
        F_g = self.systeme_biaxial(PosFix_bis, pm, alpha - d_alpha, lref)
        F_dalpha = np.zeros((3, 1))

        for j in range(3):
            F_dalpha[j, 0] = (F_d[j] - F_g[j]) / (2 * d_alpha)

        F_d = self.systeme_biaxial(PosFix_bis, pm, alpha, lref + d_lref)
        F_g = self.systeme_biaxial(PosFix_bis, pm, alpha, lref - d_lref)
        F_dlref = np.zeros((3, 1))

        for j in range(3):
            F_dlref[j, 0] = (F_d[j] - F_g[j]) / (2 * d_lref)

        Jac = np.zeros((3, 3))

        for j in range(3):
            Jac[j, 0] = F_dpm[j]
            Jac[j, 1] = F_dalpha[j]
            Jac[j, 2] = F_dlref[j]

        return Jac

    def newton_biaxial(self, PosFix_bis, alpha0, lref0):
        d_pm = 0.000001
        d_alpha = 0.000001
        d_lref = 0.000001
        pm = 100
        alpha = alpha0
        lref = lref0
        X0 = pm
        X1 = alpha
        X2 = lref

        f = self.systeme_biaxial(PosFix_bis, pm, alpha, lref)
        Err = Mathematique(None, f).magnitude()
        NbBoucle = 0
        NbBoucleMax = 100
        ErrMax = 0.0001

        while Err > ErrMax and NbBoucle < NbBoucleMax:
            m = self.calculation_jocobien_biaxial(PosFix_bis, pm, alpha, lref, d_pm, d_alpha, d_lref)
            if np.linalg.det(m) == 0:
                self.Convergence = False
                return
            else:
                Minv = np.linalg.inv(m)
            #print(m)
            f = self.systeme_biaxial(PosFix_bis, pm, alpha, lref)

            X_Next = Mathematique(Minv, f).product_matrix_vector()

            X_Next[0, 0] = abs(X0 - X_Next[0, 0])

            if X1 - X_Next[1, 0] >= 2 * math.atan(1):
                X_Next[1, 0] = X1 + X_Next[1, 0]
            else:
                X_Next[1, 0] = abs(X1 - X_Next[1, 0])

            if X2 - X_Next[2, 0] >= math.sin(alpha + math.atan(self.Lz / self.Lx)) * math.sqrt(
                    self.Lx ** 2 + self.Lz ** 2):
                X_Next[2, 0] = X2 + X_Next[2, 0]
            else:
                X_Next[2, 0] = abs(X2 - X_Next[2, 0])

            X = X_Next
            #print(X)
            pm = X[0, 0]
            alpha = X[1, 0]
            lref = X[2, 0]
            X0 = pm
            X1 = alpha
            X2 = lref

            f = self.systeme_biaxial(PosFix_bis, pm, alpha, lref)
            Err = Mathematique(None, f).magnitude()
            if alpha <= 0 or alpha >= 2 * math.atan(1) or lref >= math.sin(
                    alpha + math.atan(self.Lz / self.Lx)) * math.sqrt(
                self.Lx ** 2 + self.Lz ** 2):
                self.Convergence = False
                print("Non convergence")
                return
            NbBoucle = NbBoucle + 1

        if NbBoucle >= NbBoucleMax:
            self.Convergence = False
            #print(NbBoucle)
            print('Non Convergence')
            return
        else:
            self.Convergence = True
            #print(pm, alpha, lref)
            #print(NbBoucle)
            return pm, alpha, lref  # Renvoi une liste des trois valeurs

    def state_compression_board(self):
        condi2 = -self.N / self.NbFixa
        condi3 = 0

        if self.Ix != 0:
            condi2 = condi2 - abs((self.Mxb / self.Ix) * (self.CentreGeo1 - self.PosCmax1))

        elif self.Ix == 0 and self.Mxb != 0:
            condi3 = -1

        if self.Iz != 0:
            condi2 = condi2 - abs((self.Mzb / self.Iz) * (self.CentreGeo0 - self.PosCmax))

        elif self.Iz == 0 and self.Mzb != 0:
            condi3 = -1

        if self.N > 0 and (self.N - 6 * abs(self.Mz) / self.Lx - 6 * abs(self.Mx) / self.Lz) >= 0:
            TypeCompression = "Compression totale"

        elif self.N < 0 and condi2 >= 0 and condi3 != -1:
            TypeCompression = "Pas de compression"
        else:
            TypeCompression = "Compression partielle"
        return TypeCompression

    def calculation_traction_without_compression(self):
        global NEdg
        NEd = np.zeros((self.NbFixa, 1))
        NEdg = 0
        for j in range(self.NbFixa):
            NEd[j, 0] = -self.N / self.NbFixa
            if self.Ix != 0:
                NEd[j, 0] = NEd[j, 0] + (self.Mxb / self.Ix) * (self.CentreGeo1 - self.PosFix[j, 1])
            if self.Iz != 0:
                NEd[j, 0] = NEd[j, 0] + (self.Mzb / self.Iz) * (self.PosFix[j, 0] - self.CentreGeo0)
            if NEd[j, 0] > 0:
                NEdg = NEdg + NEd[j, 0]
                self.NbFixTraction = self.NbFixTraction + 1
            else:
                NEd[j, 0] = 0

        return NEd, NEdg

    def calculation_monoaxial(self):
        global Nedg
        self.errorOccured = False
        self.Convergence = False

        NEd = np.zeros((self.NbFixa, 1))
        self.NbFixTraction = 0

        if self.Mxb != 0 and self.Mzb == 0:
            self.alpha = 0
        elif self.Mxb == 0 and self.Mzb != 0:
            self.alpha = 2 * math.atan(1)

        TypeCompression = self.state_compression_board()

        if TypeCompression == "Compression totale":
            CEd = abs(self.N)
            listCEd = []
            listCEd.append(CEd)
            Nedg = 0
            return TypeCompression, CEd, Nedg

        elif TypeCompression == "Pas de compression":
            self.traction_without_compression = self.calculation_traction_without_compression()
            NEd = self.traction_without_compression[0]
            Nedg = self.traction_without_compression[1]
            return TypeCompression, NEd, Nedg

        k = 0
        lref0 = 0.1
        lrefp = 1

        while self.Convergence is False and (
                (self.Mxb != 0 and lref0 + k * lrefp < self.Lz) or (self.Mzb != 0 and lref0 + k * lrefp < self.Lx)):
            self.lref = lref0 + k * lrefp
            self.a = self.newton_monoaxial(self.PosFix_bis, self.lref)
            k = k + 1

        pm = self.a[0]
        lref = self.a[1]

        if self.Convergence is False:
            print("La méthode n'a pas convergé")
            self.errorOccured = True
            return self.errorOccured

        if self.Mxb != 0:
            self.L = self.distance_dowel_monoaxial(self.PosFix_bis, lref, "x")
        elif self.Mzb != 0:
            self.L = self.distance_dowel_monoaxial(self.PosFix_bis, lref, "z")

        for j in range(self.NbFixa):
            NEd[j, 0] = (pm * self.nd * self.Ar * self.L[j, 0]) / lref
            Nedg = Nedg + NEd[j, 0]
            if NEd[j, 0] > 0:
                self.NbFixTraction = self.NbFixTraction + 1

        PosCEd = self.calculation_compression(pm, self.alpha, lref, self.PosCmax, self.PosCmax1)[0]
        CEd = self.calculation_compression(pm, self.alpha, lref, self.PosCmax, self.PosCmax1)[1]

        print(Nedg)
        return TypeCompression, NEd, self.NbFixTraction, Nedg, PosCEd, CEd

    @property
    def get_error(self):
        if self.errorOccured is True:
            get_error = True
        else:
            get_error = False
        return get_error

    def newton_monoaxial(self, PosFix_bis, lref0):
        d_pm = 0.000001
        d_lref = 0.000001

        pm = 100
        lref = lref0
        X0 = pm
        X1 = lref

        f = self.systeme_monoaxial(PosFix_bis, pm, lref)
        Err = Mathematique(None, f).magnitude()
        NbBoucle = 0

        NbBoucleMax = 100
        ErrMax = 0.0001

        while Err > ErrMax and NbBoucle < NbBoucleMax:
            m = self.calculation_jacobien_monoaxial(PosFix_bis, pm, lref, d_pm, d_lref)

            f = self.systeme_monoaxial(PosFix_bis, pm, lref)

            if np.linalg.det(m) == 0:
                self.Convergence = False
                return
            else:
                Minv = np.linalg.inv(m)

            X_Next = Mathematique(Minv, f).product_matrix_vector()

            X_Next[0, 0] = abs(X0 - X_Next[0, 0])

            if self.Mx != 0 and X1 - X_Next[1, 0] >= self.Lz:
                X_Next[1, 0] = X1 + X_Next[1, 0]
            elif self.Mz != 0 and X1 - X_Next[1, 0] >= self.Lx:
                X_Next[1, 0] = abs(X1 - X_Next[1, 0])
            else:
                X_Next[1, 0] = abs(X1 - X_Next[1, 0])

            X = X_Next

            pm = X[0, 0]
            lref = X[1, 0]
            X0 = pm
            X1 = lref

            if lref <= 0 or (self.Mx != 0 and lref >= self.Lz) or (self.Mz != 0 and lref >= self.Lx):
                self.Convergence = False
                return

            f = self.systeme_monoaxial(PosFix_bis, pm, lref)
            Err = Mathematique(None, f).magnitude()

            NbBoucle = NbBoucle + 1

        if NbBoucle >= NbBoucleMax:
            self.Convergence = False
            return self.Convergence
        else:
            self.Convergence = True
            return pm, lref

    def systeme_monoaxial(self, PosFix_bis, pm, lref):
        suml = 0
        sumlx = 0
        sumlz = 0
        f = np.zeros((2, 1))
        L = np.zeros((self.NbFixa, 1))

        if self.Mxb != 0 and self.Mzb == 0:
            L = self.distance_dowel_monoaxial(PosFix_bis, lref, "x")
            # print(L)
        elif self.Mxb == 0 and self.Mzb != 0:
            L = self.distance_dowel_monoaxial(PosFix_bis, lref, "z")

        for j in range(self.NbFixa):
            suml = suml + L[j, 0]
            sumlx = sumlx + L[j, 0] * (self.PosFix[j, 0] - self.Lx / 2)
            sumlz = sumlz + L[j, 0] * (self.PosFix[j, 1] - self.Lz / 2)

        # print(suml, sumlx, sumlz)

        if self.Mxb != 0 and self.Mzb == 0:
            N_bis = (lref * self.Lx / 2) * pm
            Mx_bis = -(lref * self.Lx / 2) * (-0.5 * self.Lz + lref / 3) * pm
            f[0, 0] = N_bis - (self.nd * self.Ar * suml * pm / lref) - self.N
            f[1, 0] = Mx_bis - np.sign(self.Mxb) * (self.nd * self.Ar * sumlz * pm / lref) - abs(self.Mx)

        elif self.Mxb == 0 and self.Mzb != 0:
            N_bis = (lref * self.Lz / 2) * pm
            Mz_bis = (lref * self.Lz / 2) * (0.5 * self.Lx - lref / 3) * pm
            f[0, 0] = N_bis - (self.nd * self.Ar * suml * pm / lref) - self.N
            f[1, 0] = Mz_bis - np.sign(self.Mzb) * (self.nd * self.Ar * sumlx * pm / lref) - abs(self.Mz)

        return f

    def calculation_jacobien_monoaxial(self, PosFix_bis, pm, lref, d_pm, d_lref):
        Jac = np.zeros((2, 2))

        F_d = self.systeme_monoaxial(PosFix_bis, abs(pm + d_pm), lref)
        F_g = self.systeme_monoaxial(PosFix_bis, abs(pm - d_pm), lref)
        F_dpm = np.zeros((2, 1))

        for j in range(2):
            F_dpm[j, 0] = (F_d[j] - F_g[j]) / (2 * d_pm)

        F_d = self.systeme_monoaxial(PosFix_bis, pm, lref + d_lref)
        F_g = self.systeme_monoaxial(PosFix_bis, pm, lref - d_lref)
        F_dlref = np.zeros((2, 1))

        for j in range(2):
            F_dlref[j, 0] = (F_d[j] - F_g[j]) / (2 * d_lref)

        for j in range(2):
            Jac[j, 0] = F_dpm[j, 0]
            Jac[j, 1] = F_dlref[j, 0]

        return Jac

    def distance_dowel_monoaxial(self, PosFix_bis, lref, dir):
        L = np.zeros((self.NbFixa, 1))
        if dir == "x":
            self.A0 = 0
            self.A1 = 1
            self.A2 = -lref
        elif dir == "z":
            self.A0 = 1
            self.A1 = 0
            self.A2 = -lref

        for j in range(self.NbFixa):
            L[j, 0] = abs(self.A0 * PosFix_bis[j, 0] + self.A1 * PosFix_bis[j, 1] + self.A2) / math.sqrt(
                self.A0 ** 2 + self.A1 ** 2)

            if self.A0 * PosFix_bis[j, 0] + self.A1 * PosFix_bis[j, 1] + self.A2 <= 0:
                L[j, 0] = 0
        return L
