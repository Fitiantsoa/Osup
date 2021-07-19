import Utilitai.Osup.SharedVar as sv
from math import *

# ---------------Définition variables ---------------------
# e (mm) : épaisseur de la platine.
# bras* (mm) : distance du centre de la tuyauterie jusqu’au centre du profilé.
# S (MPa) : contrainte maximale admissible des aciers ou du matériau constituant la boulonnerie.
# a (mm) : entraxe pour platine deux chevilles et entraxe horizontale pour platine quatre chevilles.
# b (mm) : entraxe verticale entre les chevilles.
# L (mm) : longueur de la platine.
# H (mm) : largeur de la platine.
# D (mm): bras de levier, distance entre l’axe neutre de la cheville et le bord du fer soudé sur la
# platine.
# d  (mm) : longueur de diffusion.
# bprofilé (mm) : longueur des ailes du profilé.
# h (mm) : longueur de l’âme du profilé.

class Carac_chevilles():
    def __init__(self,data):
        self.nbCheville = data['platine']['nbCheville']
        self.axis = data['platine']['axis']
        self.orientation = data['platine']['orientation']
        self.l = data['platine']['l']
        self.h = data['platine']['h']
        self.e = data['platine']['e']
        self.b = data['platine']['b']
        self.a = data['platine']['a']
        self.bprofile = data['platine']['bprofile']
        self.hprofile = data['platine']['hprofile']
        self.inertieY = data['platine']['inertieY']

    def carac2chevilles(self,i):
        # Gives diffusion length of 2 dowels plate
        if self.orientation[i] == "Vertical":
            if self.inertieY[i] == "forte":
                D = (self.b[i] - float(self.bprofile[i])) / 2
            else:
                D = (self.b[i] - float(self.hprofile[i])) / 2
            d = min(pi * D, self.h[i])
        else:
            if self.inertieY[i] == "forte":
                D = self.a[i] - float(self.hprofile[i]) / 2
            else:
                D = (self.a[i] - float(self.bprofile[i])) / 2
            d = min(pi * D, self.l[i])
        return [D,d]

    def carac4chevilles(self,i):
        # Gives diffusion length of 2 dowels plate
        if self.inertieY[i] == "forte":
            Ph = (self.b[i] - self.bprofile[i]) / 2  # pliage horizontal
            Pv = (self.a[i] - self.hprofile[i]) / 2  # pliage vertical
            yb = self.hprofile[i] / 2
            zb = -self.bprofile[i] / 2
        else:
            Ph = (self.b[i] - self.hprofile[i]) / 2
            Pv = (self.a[i] - self.bprofile[i]) / 2
            yb = self.bprofile[i] / 2
            zb = -self.hprofile[i] / 2
        Po = (Ph ** 2 + Pv ** 2) ** 0.5
        Cv = min(pi * Ph / 2, (self.l[i] - self.a[i]) / 2) + min(pi * Ph / 2, self.a[i] / 2)  # longueur de diffusion vertical
        Ch = min(pi * Pv / 2, (self.h[i] - self.b[i]) / 2) + min(pi * Pv / 2, self.b[i] / 2)
        (yd, zd) = self.DpointCoordinate(yb, zb,i)
        (yc, zc) = self.CpointCoordinate(yb, zb,i)
        Co = min(pi * Po, ((yd - yc) ** 2 + (zc - zd) ** 2) ** 0.5)
        P = [Pv, Ph, Po]  # liste des pliages
        C= [Ch, Cv, Co]  # liste longueur de diffusion
        ratio = [Pv / Ch, Ph / Cv, Po / Co]
        id = ratio.index(max(ratio))
        print("P,D", [P[id], C[id]])
        return [P[id], C[id]]

    def DpointCoordinate(self, yb,zb,i):
        # Point D coordinates
        if 1/(zb + self.b[i]/2)*((zb+self.b[i]/2)*zb - (yb - self.a[i]/2)*(self.l[i]/2-yb)) <= 0:
            zd = 1/(zb + self.b[i]/2)*((zb+self.a[i]/2)*zb - (yb - self.a[i]/2)*(self.l[i]/2-yb))
            yd = self.l[i]/2
        else:
            zd = 0
            yd = 1/(yb - sv.a/2)*((zb + sv.b/2)*zb + yb*(yb - sv.a/2))
        return (yd,zd)

    def CpointCoordinate(self, yb,zb, i):
        #Point C coordinates
        if 1/(zb + self.b[i]/2)*((zb + self.b[i]/2)*zb + yb*(yb - self.a[i]/2)) >= -self.h[i]/2:
            zc = 1/(zb + self.b[i]/2)*((zb + self.b[i]/2)*zb + yb*(yb - self.a[i]/2))
            yc = 0
        else:
            zc = -self.h[i]/2
            yc = 1/(yb - self.a[i]/2)*((zb + self.b[i]/2)*(self.h[i]/2 + zb) + yb*(yb - self.a[i]/2))
        return (yc, zc)

    def cisaillement2chev(self,Fx, Fy, Fz, Mx, My, Mz,i):
        # Give shear for 2 dowels plate
        if self.orientation[i] == "Vertical":
            dim = self.b[i]
        else:
            dim = self.a[i]
        if self.axis[i] == 'X':
            Cmax = ((Fy / 2) ** 2 + (Mx / dim + Fz / 2) ** 2) ** 0.5
        elif self.axis[i] == 'Y':
            Cmax = ((Fx / 2) ** 2 + (My / dim + Fz / 2) ** 2) ** 0.5
        else:
            Cmax = ((Fx / 2) ** 2 + (Mz / dim + Fy / 2) ** 2) ** 0.5
        print('Cmax',Cmax)
        return Cmax

    def cisaillement4chev( self,Fx, Fy, Fz, Mx, My, Mz,i):
        if self.axis[i] == "X":
            Fcis_trans = Fy
            Flong = Fz
            Mtorsion = Mx
        elif self.axis[i] == "Y":
            Fcis_trans = Fx
            Flong = Fz
            Mtorsion = My
        else :
            Fcis_trans = Fy
            Flong = Fx
            Mtorsion = Mz
            #Gives shear for 4 dowels plate
        Cmax1 = ((Flong / 4 + (Mtorsion * self.a[i] / (2 * (self.b[i] ** 2 + self.a[i] ** 2)))) ** 2 + (Fcis_trans / 4 + (Mtorsion * self.b[i] / (2 * (self.b[i] ** 2 + self.a[i] ** 2)))) ** 2) ** 0.5
        Cmax2 = ((Flong / 4 + (Mtorsion * self.a[i] / (2 * (self.b[i] ** 2 + self.a[i] ** 2)))) ** 2 + (Fcis_trans / 4 - (Mtorsion * self.b[i] / (2 * (self.b[i] ** 2 + self.a[i] ** 2)))) ** 2) ** 0.5
        Cmax3 = ((Flong / 4 - (Mtorsion * self.a[i] / (2 * (self.b[i] ** 2 + self.a[i] ** 2)))) ** 2 + (Fcis_trans / 4 + (Mtorsion * self.b[i] / (2 * (self.b[i] ** 2 + self.a[i] ** 2)))) ** 2) ** 0.5
        Cmax4 = ((Flong / 4 - (Mtorsion * self.a[i] / (2 * (self.b[i] ** 2 + self.a[i] ** 2)))) ** 2 + (Fcis_trans / 4 - (Mtorsion * self.b[i] / (2 * (self.b[i] ** 2 + self.a[i] ** 2)))) ** 2) ** 0.5
        Cmax = max([Cmax1, Cmax2, Cmax3, Cmax4])
        print("Cmax",Cmax)
        return Cmax

    def traction2chev(self, Fx, Fy, Fz, Mx, My, Mz,i):
        # Gives traction for 2 dowels plate
        if self.orientation[i] == "Vertical":
            if self.axis[i] == "Y":
                if Fy < 0:
                    Tmax = -Fy/2 + Mx/self.b[i] + Mz/self.l[i]
                else:
                    Tmax = Mx/self.b[i] + Mz/self.l[i]
            elif self.axis[i] == "Z":
                if Fz < 0:
                    Tmax = -Fz/2 + My/self.b[i] + Mx/self.l[i]
                else:
                    Tmax = My / self.b[i] + Mx / self.l[i]
            else:
                if Fx < 0:
                    Tmax = -Fx/2 + My/self.b[i] + Mz/self.l[i]
                else:
                    Tmax = My/self.b[i] + Mz/self.l[i]
        else:
            if self.axis[i] == "Y":
                if Fy < 0:
                    Tmax = -Fy/2 + Mz/self.a[i] + Mx/self.h[i]
                else:
                    Tmax = Mx / self.a[i] + Mz / self.h[i]
            elif self.axis[i] == 'X':
                if Fx < 0:
                    Tmax = -Fx/2 + Mz/self.a[i] + My/self.h[i]
                else:
                    Tmax = Mz / self.a[i] + My / self.h[i]

            else:
                if Fz < 0:
                    Tmax = -Fz/2 + Mx/self.a[i] + My/self.h[i]
                else:
                    Tmax =  Mx / self.a[i] + My / self.h[i]
        return Tmax

    def traction4chev(self,Fx,Fy,Fz,Mx,My,Mz,i):
        # Gives traction for 4 dowels plate
        if self.axis[i] == "X":
            if Fx < 0:
                Tmax = - Fx/4 + abs(My)/(2*self.b[i]) + abs(Mz)/(2*self.a[i])
            else:
                Tmax = abs(My)/(2*self.b[i]) + abs(Mz)/(2*self.a[i])
        elif self.axis[i] == "Y":
            if Fy < 0:
                Tmax = - Fy/4 + abs(Mx)/(2*self.b[i]) + abs(Mz)/(2*self.a[i])
            else:
                Tmax = abs(Mx)/(2*self.b[i]) + abs(Mz)/(2*self.a[i])
        else:
            if Fz < 0:
                Tmax = - Fz/4 + abs(My)/(2*self.b[i]) + abs(Mx)/(2*self.a[i])
            else:
                Tmax =  abs(Mx)/(2*self.b[i]) + abs(Mz)/(2*self.a[i])
        print("Tmax",Tmax)
        return Tmax





