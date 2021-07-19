from Utilitai.OsupMAJ.ContrainteAdmissible import AdmissibleProfile
from Utilitai.Osup.constant import *
#Niveau OAB
#TODO calcul ratio pour les autres niveaux

class Ratio():
    """
    Cette classe permet de calculer les ratio
    il est à noter que toutes conraintes sont à multiplier par -1 (signe différent de Beamstress)
    """
    def __init__(self,value, niveau, Sn, Svy, Svz, Smt, Smfy, Smfz):
        # On stocke les valeurs dans les listes pour les réutiliser dans eq20 et pour avoir le max
        self.data = value
        self.adm = AdmissibleProfile(value)
        self.Sn = Sn
        self.Svy = Svy
        self.Svz = Svz
        self.Smt = Smt
        self.Smfy = Smfy
        self.Smfz = Smfz
        self.f = open(resultfile, "a")
        self.f.write(dash)
        self.niveau = niveau
        self.ratioaxial = self.ratioAxial()
        self.ratioflexion = self.ratioFlexion()
        self.ratioCisaillement = self.ratioCisaillement()
        self.ratioeq21 = max(self.ratioEq21())
        self.ratioeq22 = max(self.ratioEq22())
        self.ratioMax = 0




    def ratioAxial(self):
        """
        Calcul ratio compression et traction fait en même temps pour avoir une list de longueur aux autres ratios
        :return:
        """
        if self.niveau == "oab":
            ratio = list(map(lambda x:round(abs(self.Sn[x])/self.adm.admissibleCompression(x),4) if self.Sn[x]<0 else round(abs(self.Sn[x])/self.adm.admissibleTraction(x),4),range(len(self.Sn))))
        elif self.niveau == "d":
            ratio = list(map(lambda x: round(abs(self.Sn[x]) / (self.adm.admissibleCompression(x)*self.adm.factAdmissibleD(x)), 4) if self.Sn[x] < 0 else round(abs(self.Sn[x]) / (self.adm.admissibleTraction(x)*self.adm.factAdmissibleD(x)), 4), range(len(self.Sn))))
        self.f.write(f'Ratio axial          :    {"           ".join(str(item) for item in ratio)}\n')
        return ratio

    def ratioCisaillement(self):
        """
        :param yz: cisaillement  en Z
        Le cisaillement dû à l'effort tranchant et le cisaillement dû à la torsion
        """
        if self.niveau == "oab":
            ratio= list(map(lambda x: round(max((((abs(self.Svz[x])+abs(self.Smt[x]))**2+self.Svy[x]**2))**0.5,(((abs(self.Svy[x])+abs(self.Smt[x]))**2+self.Svz[x]**2))**0.5)/self.adm.admissibleCisaillement(x),3) ,range(len(self.Svz))))
        elif self.niveau == "d":
            ratio= list(map(lambda x: round(max((((abs(self.Svz[x])+abs(self.Smt[x]))**2+self.Svy[x]**2))**0.5,(((abs(self.Svy[x])+abs(self.Smt[x]))**2+self.Svz[x]**2))**0.5)/(self.adm.admissibleCisaillement(x)*self.adm.factAdmissibleD(x)),3) ,range(len(self.Svz))))
        self.f.write(f'Ratio cisaillement   :    {"           ".join(str(item) for item in ratio)}\n')
        return ratio


    def ratioFlexion(self):
        """
        La contrainte prise en compte dans le calcul de la contrainte de flexion est la contrainte de compression due à la flexion
        """
        if self.niveau == "oab":
            ratio = list(map(lambda x: round((abs(self.Smfy[x])+abs(self.Smfz[x])) / self.adm.admissibleFlexion(x), 3) , range(len(self.Smfy))))
        elif self.niveau == "d":
            ratio = list(map(lambda x: round((abs(self.Smfy[x]) + abs(self.Smfz[x])) / (self.adm.admissibleFlexion(x)*self.adm.factAdmissibleD(x)), 3),range(len(self.Smfy))))
        self.f.write(f'Ratio flexion        :    {"           ".join(str(item) for item in ratio)}\n')
        return ratio

    def ratioFlexionYZ(self,yz):
        """
        :param yz: paramètre pour différence flexion autour de l'axe Y ou l'axe Z
        :return:
        """
        if yz == "Y":
            Sv = self.Smfy
            admissible = admissibleFlexionY()
        if yz == "Z":
            Sv = self.Smfz
            admissible = admissibleFlexionZ()
        ratio = list(map(lambda x:round(abs(x)/admissible,3) if x != 0 else 0.000 , Sv))
        return ratio

    def ratioEq21(self):
        if self.niveau == "oab":
            ratio = list(map(lambda x: round(abs(self.Sn[x])/self.adm.admissibleTraction(x)+self.ratioflexion[x],3) if self.Sn[x]>0 else 0,range(len(self.Sn))))
        elif self.niveau == "d":
            ratio = list(map(lambda x: round(abs(self.Sn[x]) / (self.adm.admissibleTraction(x)*self.adm.factAdmissibleD(x)) + self.ratioflexion[x], 3) if self.Sn[x] > 0 else 0,range(len(self.Sn))))
        self.f.write(f'Ratio equation 21    :    {"           ".join(str(item) for item in ratio)}\n')
        return ratio

    def ratioEq22(self):
        if self.niveau == "oab":
            ratio = list(map(lambda x: round(abs(self.Sn[x])/ self.adm.admissibleCompression(x) + self.ratioflexion[x] , 3) if (self.Sn[x]  < 0 and abs(self.Sn[x]) / self.adm.admissibleCompression(x)<0.15) else 0, range(len(self.Sn))))
        elif self.niveau == "d":
            ratio = list(map(lambda x: round(abs(self.Sn[x]) / (self.adm.admissibleCompression(x)*self.adm.factAdmissibleD(x)) + self.ratioflexion[x], 3) if (self.Sn[x] < 0 and abs(self.Sn[x]) / (self.adm.admissibleCompression(x)*self.adm.factAdmissibleD(x)) < 0.15) else 0, range(len(self.Sn))))
        self.f.write(f'Ratio equation 22    :    {"           ".join(str(item) for item in ratio)}\n')
        return ratio

    def maxRatio(self):
        """
        Permet d'avoir tous les ratios de la courbe min dans un seul fichier txt        """
        maxRatio = max([max(self.ratioCisaillement), max(self.ratioaxial), max(self.ratioflexion), self.ratioeq21, self.ratioeq22 ])
        self.f.write(f'Ratio max            :    {round(maxRatio,3)}\n')
        self.f.close()
        self.ratioMax = maxRatio
        return maxRatio

    def writeOsupFile(self,fx,fy,fz):
        """ Fichier oFile est le fichier de stockage des ratios de la courbe min (utile pour la vérification)"""
        oFile = open(curveFile, "a")
        oFile.write(f'{round(fx,2)}		{round(fy,2)}		{round(fz,2)}		{round(max(self.ratioaxial),3)}		{round(max(self.ratioflexion),3)}		{round(max(self.ratioCisaillement),3)}		{round(self.ratioMax,3)}\n')
        oFile.close()