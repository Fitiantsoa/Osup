from math import pi


class CalculEtrier:
    def __init__(self,  name, materiauxB, Sb, As, d, l, t, pas, Sy, fy, Su, fu, Fub, A, dm, do, tp, pCisaill, fraise, p1u, e1u, e2u, norm, level, coeff):
        """"

        :param name: Nom Etrier (str)
        :param materiauxB: Matériaux du boulon (str)
        :param Sb : Section réelle du noyau du boulon RCC-M (mm²)
        :param As: Section du noyau du boulon EN (mm²)
        :param d: Diamètre nominal du boulon (mm)
        :param l: Distance minimale boulon/bord libre (mm)
        :param t:  Epaisseur du matériau RCCM ou épaisseur de la pièce attachée extérieure la plus mince (mm)
        :param pas : Le pas du boulon (mm)
        :param Sy : Limite élastique RCCM (MPa)
        :param fy : Limite élastique EN (MPa)
        :param Su : Résistance mécanique à la traction RCCM (MPa)
        :param fu : Résistance mécanique à la traction EN (MPa)
        :param Fub : Limite utilme à la traction du boulon EN (MPa)
        :param A : Aire brute du boulon (mm²)
        :param dm: Diamètre moyen (mm)
        :param do: Diamètre nominal des trous (mm)
        :param tp:  Epaisseur de la plaque sous tete (mm)
        :param pCisaill : Le plan de cisaillement est dans la partie : non filetée ou filetée (str)
        :param fraise : Le boulon est fraisé ou non (str)
        :param p1u : entraxe longitudianale donnée par l'utilisateur (mm)
        :param e1u : pince longitudinale donnée par l'utilisateur (mm)
        :param e2u : pince transversale donnée par l'utilisateur (mm)
        """
        self._name = name
        self._materiauxB = materiauxB
        self._pCisaill = pCisaill
        self._fraise = fraise
        self._Sb = self.check(Sb)
        self._As = self.check(As)
        self._d = self.check(d)
        self._l = self.check(l)
        self._t = self.check(t)
        self._Sy = self.check(Sy)
        self._Su = self.check(Su)
        self._fy = self.check(fy)
        self._fu = self.check(fu)
        self._Fub = self.check(Fub)
        self._A = self.check(A)
        self._dm = self.check(dm)
        self._do = self.check(do)
        self._tp = self.check(tp)
        self._p1u = self.check(p1u)
        self._e1u = self.check(e1u)
        self._e2u = self.check(e2u)
        self._pas = float(pas)
        self._omegaM2 = 1.25
        self.rccm = norm == "rccm"
        self.en = not norm == "rccm"
        self.lvlA = level == "oab"
        self.lvlC = level == "c"
        self.lvlD = level == "d"
        self._coeff = coeff
        if self.en:
            self._Fured = self.getFured()
            self._FbRd = self.getFbRd()
            self._k2 = self.getK2()
            self._Bp = self.getBp()
        self._Fy = 0
        self._Fp1 = self.getFp1()
        self._Fp2 = self.getFp2()
        self._Fp = self.getFp()
        self._FtM = self.getFtMateriaux()
        self._Ft1 = self.getFt1()
        self._Ft2 = self.getFt2()
        self._Ft = self.getFt()
        self._FvM = self.getFvMateriaux()
        self._Fv1 = self.getFv1()
        self._Fv2 = self.getFv2()
        self._Fv = self.getFv()
        self.plots = self.filter_result()

# ////////////////////////////////////////////////////////////////////////////////
# /////////////////////////PARAMETRES/////////////////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////

# #///////////////////////////CHECK//////////////////////////////////////////////
    def check(self, value):
        if value != "":
            return float(value)

# ////////////////////////////////////////////////////////////////////////////////
# /////////////////////////CONTRAINTES ADMISSIBLES////////////////////////////////
# ///////////////////////////////////////////////////////////////////////////////

# ///////////////////////////////EN///////////////////////////////////
# ///////////////////////VALEUR REDUITE TRACTION///////////////////////////
    def getFured(self):
        Fured = 0.5 * self._fy + 0.6 * self._fu
        if self._fu > Fured:
            return Fured
        else:
            return self._fu


# //////////////////////////PRESSION LATERALE////////////////////////////////////
    #RCC-M
    # Contrainte de pression latérale admissible MIN_1
    def getFp1(self):
        # Contraine RCC-M
        if self.rccm:
            # Au niveau C
            if self.lvlC:
                Fp1 = ((self._Su * self._l) / (2 * self._d))*(4/3)
            # Au niveau D et OAB
            else:
                Fp1 = ((self._Su * self._l) / (2 * self._d))
            # Obtenir Fp1
            return Fp1

    #RCC- M
    # Contrainte de pression latérale admissible MIN_2
    def getFp2(self):
        # A la réglementation RCC-M
        if self.rccm:
            # Au niveau C
            if self.lvlC:
                Fp2 = (1.5 * self._Su) * (4/3)
            # Au niveau OAB et D
            else:
                Fp2 = (1.5 * self._Su)
            # Obtenir Fp2
            return Fp2

    # Contrainte de pression latérale admissible finale
    def getFp(self):
        #Réglementation RCC-M
        if self.rccm:
            return min(self._Fp1, self._Fp2)

# //////////////////////////PRESSION DIAMETRALE////////////////////////////////////
    def getFbRd(self):
        # A la réglementation EN 13480-3
        return (1.5 * self._Fured * self._d*self._t) / self._omegaM2

# ////////////////////////////TRACTION//////////////////////////////////////////////
    #RCC-M
    # Contrainte de traction admissible MIN_1 au niveau D
    def getFt1(self):
        if self.rccm and self.lvlD:
            return 0.7*self._Su

    #RCC-M
    # Contrainte de traction admissible MIN_2 au niveau D
    def getFt2 (self):
        if self.rccm and self.lvlD:
            return self._Sy

    # RCC-M
    # Contrainte de traction admissible au niveau O,A,B selon le Matériaux
    def getFtMateriaux(self):
        if self.rccm:
            # Calcul de Ft dans le cas où le matériau du boulon est de type ferritique
            if self._materiauxB == "Ferritique":
                return 0.5 * self._Su
            # Calcul de Ft dans le cas où le matériau du boulon est de type austénitique
            else:
                return 0.3 * self._Su

    #EN
    #Coefficient k2
    def getK2(self):
        if self._fraise == "Fraisé":
            return 0.63
        else:
            return 0.9

    #Contrainte de traction admissible finale
    def getFt(self):
        if self.rccm:
            # Au niveau OAB
            if self.lvlA:
                Ft = self._FtM
            # Au niveau C
            elif self.lvlC:
                Ft = self._FtM*(4/3)
            # Au niveau D
            else:
                Ft = min(self._Ft1, self._Ft2)
            return Ft
        # A la réglementation EN 13480-3
        else:
            return (self._k2*self._Fub*self._As)/self._omegaM2

# //////////////////////////CISAILLEMENT//////////////////////////////////////////
    #RCCM
    # Contrainte de cisaillement admissible MIN_1 au niveau D
    def getFv1(self):
        if self.rccm and self.lvlD:
            return 0.42 * self._Su

    #RCCM
    # Contrainte de cisaillement admissible MIN_2 au niveau D
    def getFv2 (self):
        if self.rccm and self.lvlD:
            return 0.6 * self._Sy

    #RCCM
    # Contrainte de cisaillement en fonction du materiaux du boulon
    def getFvMateriaux(self):
        if self.rccm:
            # Calcul de Fv dans le cas où le matériau du boulon est de type ferritique
            if self._materiauxB == "Ferritique":
                FvM = (5 * self._Su) / 24
            # Calcul de Ft dans le cas où le matériau du boulon est de type austénitique
            else:
                FvM = (self._Su / 8)
            # Obtenir FvM
            return FvM

    #RCCM
    #Contrainte admissible de cisaillement finale
    def getFv(self):
        if self.rccm:
            # Au niveau OAB
            if self.lvlA:
                Fv = self._FvM
            # Au niveau C
            elif self.lvlC:
                Fv = self._FvM*(4/3)
            # Au niveau D
            else:
                Fv = min(self._Fv1, self._Fv2)
            # Obtenir Fv
            return Fv
        # A la réglementation EN 13480-3
        else:
            if self._pCisaill == "Filetée":
                alphav = 0.5
                Fv = (alphav*self._Fub*self._As)/self._omegaM2
            else:
                alphav = 0.6
                Fv = (alphav*self._Fub*self._A)/self._omegaM2
            return Fv

#EN
# //////////////////////////POINCONNEMENT//////////////////////////////////////////
    def getBp(self):
        return (0.6*pi*self._dm*self._tp*self._fu)/self._omegaM2

# /////////////////////////////////////////////////////////////////////////////////////////
# /////////////////////////////////CRITERES///////////////////////////////////
# /////////////////////////////////////////////////////////////////////////////////////////

#RCCM et EN
# //////////////////////////////////TRACTION////////////////////////////////////////////
    # Fonction de critère de traction issu de l'équation Z VI 2461.1
    def getFzTraction(self, ratio=1):
        # Norme RCCC-M
        if self.rccm:
            # Fonction Fz constante
            return 2*self._Ft*self._Sb*ratio
        #Norme NF EN 13480-3
        else:
            # Fonction Fz constante
            return self._Ft*2*ratio
            pass

# RCCM et EN
# //////////////////////////////////CISALLEMENT////////////////////////////////////////////
    # Fonction de critère de cisaillement issu de l'équation Z VI 2461.1
    def getFzCisallement(self, Fy, ratio=1):
        #Norme RCCC-M
        if self.rccm:
            x = ((((self._Sb ** 2 * self._Fv ** 2) * ratio ** 2) - (1+self._coeff**2)* Fy ** 2) / self._coeff**2)
        # Norme NF EN 13480-3
        else:
            x = ((((self._Fv ** 2 )* ratio ** 2) - (1+self._coeff**2) * Fy ** 2) / (self._coeff**2))

        # La racine doit être positive
        if x > 0:
            # Fonction Fz en fonction de Fy
            return x ** (1 / 2)
        # Sinon Fz = 0
        else:
            return 0

# RCCM et EN
# //////////////////////////////////TRACTION ET CISAILLEMENT//////////////////////////////////
    # Fonction de critère de cisaillement et de traction issu de l'équation Z VI 2461.4
    def getFzTrac_Cisail(self, Fy, ratio=1):
        # Norme RCCC-M
        if self.rccm:
            x = ((((4 * self._Ft ** 2 * self._Sb ** 2 * self._Fv ** 2) * ratio ** 2) - 4*(1+self._coeff**2) * self._Ft ** 2 * Fy ** 2) /
             (self._Fv ** 2 + 4*self._coeff**2 * self._Ft ** 2))

            # La racine doit être positive
            if x > 0:
                # Fonction Fz en fonction de Fy
                return x ** (1 / 2)
            # Sinon Fz = 0
            else:
                return 0
        # Norme NF EN 13480-3
        else:
            # La racine doit être positive
            if (((2*ratio/(2.8*self._Ft))**2)-4*((self._coeff**2/self._Fv**2)-(1/(2.8*self._Ft))**2)*(((1+self._coeff**2)*Fy**2-(ratio**2)*self._Fv**2)/self._Fv**2)) > 0:
                x = (-(2 * ratio / (2.8 * self._Ft)) + (((2 * ratio / (2.8 * self._Ft)) ** 2 - 4 * (
                        (self._coeff**2/ self._Fv ** 2) - (1 / (2.8 * self._Ft)) ** 2) * (((1+self._coeff**2)* Fy ** 2 - (
                        ratio ** 2) * self._Fv ** 2) / self._Fv ** 2)) ** (1 / 2))) / (
                        2 * ((self._coeff**2 / self._Fv ** 2) - (1 / (2.8 * self._Ft)) ** 2))
                if x > 0:
                     return x
                else:
                    return 0
            # Sinon Fz = 0
            else:
                return 0



#RCCM
# //////////////////////////////////PRESSION LATERALE///////////////////////////////////////////
    # Fonction de critère de pression latérale issu de l'équation Z VI 2461.6
    def getFzPressionL(self, Fy, ratio=1):
        # Norme RCCC-M
        if self.rccm:
            x = ((((self._Fp ** 2 * self._d ** 2 * self._t ** 2) * ratio ** 2) - (1+self._coeff**2) * Fy ** 2) / self._coeff**2)
            # La racine doit être positive
            if x > 0:
                # Fonction Fz en fonction de Fy
                return x**(1/2)
            # Sinon Fz = 0
            else:
                return 0
        else:
            return 0
# EN
# //////////////////////////////////PRESSION DIAMETRALE///////////////////////////////////////////
    # Fonction de critère de pression diamétrale issu de l'équation
    def getFzPressionD(self, Fy, ratio=1):
        if self.en:
            x = ((((self._FbRd**2) * ratio ** 2) - (1+self._coeff**2) * Fy ** 2) / self._coeff**2)
            # La racine doit être positive
            if x > 0:
                # Fonction Fz en fonction de Fy
                return x ** (1 / 2)
            # Sinon Fz = 0
            else:
                return 0
        else:
            return 0

# EN
# //////////////////////////////////POINCONNEMENT///////////////////////////////////////////
    # Fonction de critère de poinconnemnt
    def getFzPoinconnment(self, ratio=1):
        if self.en:
           return self._Bp*2*ratio
        else:
            return 0

#RCCM
# //////////////////////////////////DISTANCE MINIMALE 1 ////////////////////////////////////////////
    # Fonction de critère de distance minimale issu de l'équation Z VI 2462.1
    def getFzDistance1 (self, Fy, ratio=1):
        # Norme RCCC-M
        if self.rccm:
            x = (((((((self._l*self._Su*self._t)*ratio)-0.5*self._Su*self._d*self._t)/1.43)**2)-(1+self._coeff**2)*Fy**2)/self._coeff**2)
            # La racine doit être positive
            if x > 0:
                # Fonction Fz en fonction de Fy
                return x**(1/2)
            # Sinon Fz = 0
            else:
                return 0
        else:
            return 0

#RCCM
# //////////////////////////////////DISTANCE MINIMALE 2////////////////////////////////////////////
    # Fonction de critère de distance minimale issu de l'équation Z VI 2462.2
    def getFzDistance2(self, Fy, ratio=1):
        # Norme RCCC-M
        if self.rccm:
            x = ((2.25*((self._Su**2*self._d**2*self._t**2)*ratio**2)-(1+self._coeff**2)*Fy**2)/self._coeff**2)
            # La racine doit être positive
            if x > 0:
                # Fonction Fz en fonction de Fy
                return x**(1/2)
            # Sinon Fz = 0
            else:
                return 0
        # Norme NF EN 13480-3
        else:
            return 0


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////CALCUL//////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////
    #Incrémentation des calculs des contraintes
    def runCalcul(self, ratio=1):
        plot = {}
        #Pour une plage de Fy avec un pas de 10
        stop1, stop2, stop3, stop4, stop5, stop6 = True, True, True, True, True, True

        if self.rccm:
            plot[self._name] = {'Courbe Minimale': {'DataX': [], 'DataY': []},
                                     'Traction': {'DataX': [], 'DataY': []},
                                     'Cisaillement': {'DataX': [], 'DataY': []},
                                     'Traction et de Cisaillement': {'DataX': [], 'DataY': []},
                                     'Pression Latérale': {'DataX': [], 'DataY': []},
                                     '1er Critere de Distance Minimale': {'DataX': [], 'DataY': []},
                                     '2eme Critere de Distance Minimale': {'DataX': [], 'DataY': []}}
        elif self.en:
            plot[self._name] = {'Courbe Minimale': {'DataX': [], 'DataY': []},
                                     'Traction': {'DataX': [], 'DataY': []},
                                     'Cisaillement': {'DataX': [], 'DataY': []},
                                     'Traction et de Cisaillement': {'DataX': [], 'DataY': []},
                                     'Pression Diamétrale': {'DataX': [], 'DataY': []},
                                     'Poinconnement': {'DataX': [], 'DataY': []}}
        self._FzTraction = None
        self._FzCisaillement = None
        self._FzTrac_Cisail = None
        self._FzPressionL = None
        self._FzDistance1 = None
        self._FzDistance2 = None
        self._minFz = None
        self._FzPressionD = None
        self._FzPoinconnement = None

        i = - 10
        while (self._FzCisaillement != 0 or
                self._FzTrac_Cisail != 0 or
                self._FzPressionL != 0 or
                self._FzDistance1 != 0 or
                self._FzDistance2 != 0 or
               self._FzPressionD != 0):
            i += 10

            #Récupérer valeur des fonctions Fz selon leurs critères RCCM
            self._FzTraction = self.getFzTraction(ratio)
            self._FzCisaillement = self.getFzCisallement(i, ratio)
            self._FzTrac_Cisail = self.getFzTrac_Cisail(i, ratio)
            self._FzPressionL = self.getFzPressionL(i, ratio)
            self._FzDistance1 = self.getFzDistance1(i, ratio)
            self._FzDistance2 = self.getFzDistance2(i, ratio)
            self._FzPressionD = self.getFzPressionD(i, ratio)
            self._FzPoinconnement = self.getFzPoinconnment(ratio)


            #Courbe Min
            #Si les tous les FZ sont égaux alors ils sont à "0"
            if (self._FzCisaillement == self._FzTrac_Cisail == self._FzPressionL == self._FzDistance1 ==
                    self._FzDistance2 == self._FzPressionD):
                #La courbe min est donc égale elle aussi à "0"
                self._minFz = 0
            else:
                try:
                    #Faire le min des critère RCCM
                    if self.rccm:
                        self._minFz = min(self._FzTraction, self._FzCisaillement, self._FzTrac_Cisail,
                              self._FzPressionL, self._FzDistance1, self._FzDistance2)
                    # Faire le min des critère EN
                    else:
                        self._minFz = min(self._FzTraction, self._FzCisaillement, self._FzTrac_Cisail,
                                          self._FzPressionD, self._FzPoinconnement)
                except TypeError:
                    a=1

            # //////////////////////////////////////////////RCC-M et EN///////////////////////////////////////////////
            #Courbe minimale de l'étrier
            if stop1:
                plot[self._name]['Courbe Minimale']['DataX'].append(i)
                plot[self._name]['Courbe Minimale']['DataY'].append(self._minFz)

            #Critère de Traction de l'étrier
            if stop1:
                plot[self._name]['Traction']['DataX'].append(i)
                plot[self._name]['Traction']['DataY'].append(self._FzTraction)

            # Critère de Cisaillement de l'étrier
            if stop2:
                plot[self._name]['Cisaillement']['DataX'].append(i)
                plot[self._name]['Cisaillement']['DataY'].append(self._FzCisaillement)

            # Critère de Traction et de Cisaillement de l'étrier
            if stop3:
                plot[self._name]['Traction et de Cisaillement']['DataX'].append(i)
                plot[self._name]['Traction et de Cisaillement']['DataY'].append(self._FzTrac_Cisail)

            # //////////////////////////////////////////////RCC-M///////////////////////////////////////////////
            # Critère de Pression latérale
            if stop4 and self.rccm:
                plot[self._name]['Pression Latérale']['DataX'].append(i)
                plot[self._name]['Pression Latérale']['DataY'].append(self._FzPressionL)

            # Critère 1  de Distance minimale
            if stop5 and self.rccm:
                plot[self._name]['1er Critere de Distance Minimale']['DataX'].append(i)
                plot[self._name]['1er Critere de Distance Minimale']['DataY'].append(self._FzDistance1)

            # Critère 2  de Distance minimale
            if stop6 and self.rccm:
                plot[self._name]['2eme Critere de Distance Minimale']['DataX'].append(i)
                plot[self._name]['2eme Critere de Distance Minimale']['DataY'].append(self._FzDistance2)

            # //////////////////////////////////////////////EN///////////////////////////////////////////////
            # Critère de Pression latérale
            if stop4 and self.en:
                plot[self._name]['Pression Diamétrale']['DataX'].append(i)
                plot[self._name]['Pression Diamétrale']['DataY'].append(self._FzPressionD)

            # Critère 1  de Distance minimale
            if stop1 and self.en:
                plot[self._name]['Poinconnement']['DataX'].append(i)
                plot[self._name]['Poinconnement']['DataY'].append(self._FzPoinconnement)

            if self._minFz == 0:
                stop1 = False

            if self._FzCisaillement == 0:
                stop2 = False

            if self._FzTrac_Cisail == 0:
                stop3 = False

            if self._FzPressionL == 0 and self._FzPressionD == 0:
                stop4 = False

            if self._FzDistance1 == 0:
                stop5 = False

            if self._FzDistance2 == 0:
                stop6 = False
        return plot

    def filter_result(self):
        value = self.runCalcul()
        negatif = {"DataX":[], "DataY":[]}
        for i in range(1,len(value[self._name]['Courbe Minimale']['DataX'])):
            negatif['DataX'].append(-value[self._name]['Courbe Minimale']['DataX'][-i])
            negatif ['DataY'].append(value[self._name]['Courbe Minimale']['DataY'][-i])
        value[self._name]['Courbe Minimale']['DataX'] = negatif['DataX'] + value[self._name]['Courbe Minimale']['DataX']
        value[self._name]['Courbe Minimale']['DataY'] = negatif['DataY'] + value[self._name]['Courbe Minimale']['DataY']
        return value
