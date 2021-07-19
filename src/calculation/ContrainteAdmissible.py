"""
Les fonctions suivantes permettent d'avoir les contraintes admissibles
"""
from math import *

class AdmissibleProfile():
    def __init__(self, data):
        self.E = data['profile']['mat']['E']
        self.Sy = data['profile']['mat']['Sy']
        self.Su = data['profile']['mat']['Su']
        self.A = data['profile']['sec']['A']
        self.Iy = data['profile']['sec']['Iy']
        self.Iz = data['profile']['sec']['Iz']
        self.lf = data['profile']['sec']['lf']


    def admissibleTraction(self,numPoint):
        Ft = min(0.6 * self.Sy[numPoint],0.55 * self.Su[numPoint])
        return Ft

    def admissibleFlexion(self, numPoint):
        """
        Les valeurs prises
        :return:
        """
        return min(0.6*self.Sy[numPoint],0.5*self.Su[numPoint])

    # def admissibleFlexionY(self):
    #     """
    #     Contrainte adm flexion donnée dans RCC-M Z VI 2215
    #     """
    #     if sv.bprofile/(2*sv.tf) < 170/sv.Sy**0.5:
    #         return min(0.6*sv.Sy,0.5*sv.Su)
    #     elif sv.bprofile/(2*sv.tf) > 170/sv.Sy**0.5 and sv.bprofile/(2*sv.tf) <= 250/sv.Sy**0.5:
    #         facteurSy = 0.79-0.00076*sv.bprofile*sv.Sy**0.5/(2*sv.tf)
    #         return min(facteurSy*sv.Sy,0.5*sv.Su)
    #     else:
    #         return min(0.6*sv.Sy, 0.5*sv.Su)


    # def admissibleFlexionZ():
    #     """
    #     Inertie faible voir manuel Beamstress p84
    #     :return:
    #     """
    #     if sv.bprofile/(2*sv.tf) < 170/sv.Sy**0.5:
    #         return min(0.75*sv.Sy,0.63*sv.Su)
    #     elif sv.bprofile / (2 * sv.tf) > 170 / sv.Sy ** 0.5 and sv.bprofile / (2 * sv.tf) <= 250 / sv.Sy ** 0.5:
    #         facteurSy = 1.075 - 0.0019*sv.bprofile*sv.Sy**0.5/(2*sv.tf)
    #         return min(0.63*sv.Su,facteurSy*sv.Sy)

    def admissibleCisaillement(self, numPoint):
        return min(0.4*self.Sy[numPoint],0.33*self.Su[numPoint])

    def admissibleCompression(self,numPoint):
        #TODO modifier le code pour prendre en compte tous les types de section
        Cc = (2*pi**2*self.E[numPoint]/self.Sy[numPoint])**0.5
        ry = (self.Iy[numPoint]/self.A[numPoint])**0.5
        rz = (self.Iz[numPoint]/self.A[numPoint])**0.5
        lamda = min(self.lf[numPoint]/ry,self.lf[numPoint]/rz)
        if lamda < Cc:
            Fa = (1-(lamda**2/(2*Cc**2)))*self.Sy[numPoint]/(5/3+3*lamda/(8*Cc)-lamda**3/(8*Cc**3))
        else:
            Fa=2*pi**2*self.E[numPoint]/(23*lamda**2)
        print("adm axial",Fa)
        return Fa

    def factAdmissibleD(self, numPoint):
        if self.Su[numPoint] >= 1.2 * self.Sy[numPoint]:
            f = min(1.66, 1.167 * self.Su[numPoint] / self.Sy[numPoint])
        else:
            f = 1.4
        return f

if __name__ == "__main__":
    sv.nodelist = [[0,0,0],[100,0,0]]
    sv.E = 2040000
    sv.Sy = 175
    sv.Su = 215
    print(admissibleCompression())



