import math
import numpy as np
from src.Version5etag.arithmetique import Arithmetique
from src.Version5etag.readinginputdata import ReadingInputData


class Criteria:
    def __init__(self, inputdataaster, resultTrac, resultCisail):
        self.NbFixa = inputdataaster.get("NbFixa")
        self.TypeCharge = inputdataaster.get("TypeCharge")
        self.norme = inputdataaster.get("norme")
        self.modele = inputdataaster.get("modele")
        self.hef = inputdataaster.get("hef")
        self.dnom = inputdataaster.get("dnom")
        self.EDF = inputdataaster.get("EDF")
        self.txt = inputdataaster.get("txt")

        self.dowel_property = inputdataaster.get("dowel_property")
        self.gamme = self.dowel_property.get("gamme")

        self.data_board_dowel = inputdataaster.get("data_board_dowel")
        self.sx0 = self.data_board_dowel.get("sx0")
        self.sx1 = 0
        self.sz0 = self.data_board_dowel.get("sz0")
        self.sz1 = 0
        self.cx0 = self.data_board_dowel.get("cx0")
        self.cx1 = self.data_board_dowel.get("cx1")
        self.cz0 = self.data_board_dowel.get("cz0")
        self.cz1 = self.data_board_dowel.get("cz1")
        self.Lx = self.data_board_dowel.get("Lx")
        self.Lz = self.data_board_dowel.get("Ly")
        self.tfix = self.data_board_dowel.get("tfix")

        self.effort = inputdataaster.get("effort")
        self.Mx = self.effort.get('Mx')
        self.Mz = self.effort.get('Mz')
        self.N = self.effort.get('N')
        self.T = self.effort.get('T')
        self.Vx = self.effort.get('Vx')
        self.Vz = self.effort.get('Vz')

        self.data_concrete = inputdataaster.get("data_concrete")
        self.h = self.data_concrete.get("h")
        self.etat = self.data_concrete.get("etat")
        self.armature = self.data_concrete.get("armature")
        self.typebeton = self.data_concrete.get("typebeton")

        self.resultshearing = resultCisail
        self.Ved = self.resultshearing.get('Ved')
        self.VEdg = self.resultshearing.get('VEdg')
        self.Vedx = self.resultshearing.get('Vedx')
        self.Vedz = self.resultshearing.get('Vedz')
        self.VEgdx = self.resultshearing.get('VEdgx')
        self.VEgdz = self.resultshearing.get('VEdgz')
        self.eV0 = self.resultshearing.get("eV0")
        self.eV1 = self.resultshearing.get("eV1")
        self.eV = [self.eV0, self.eV1]

        self.NEd = resultTrac.get("NEd")
        self.NEdg = resultTrac.get("NEdg")
        self.eN = resultTrac.get("eN")
        self.z = resultTrac.get("z")
        self.CEd = resultTrac.get("CEd")

        self.inertia = inputdataaster.get("inertia")
        self.PosFix = self.inertia.get("PosFix")
        self.DistFixBord = self.inertia.get("DistFixBord")
        self.DistFixFix = self.inertia.get("DistFixFix")
        self.Iy = self.inertia.get("Iy")
        self.Tb = self.inertia.get("Tb")
        self.CentreGeo0 = self.inertia.get("CentreGeo0")
        self.CentreGeo1 = self.inertia.get("CentreGeo1")

        self.Recuperationproprietecheville = ReadingInputData(self.norme, self.dowel_property, self.data_board_dowel,
                                                              self.data_concrete)

        self.inputdata = inputdataaster.get("inputdata")
        self.scrn = self.inputdata.get("scrn")
        self.ccrN = self.inputdata.get("ccrN")
        self.scrsp = self.inputdata.get("scrsp")
        self.ccrsp = self.inputdata.get("ccrsp")
        self.hmin = self.inputdata.get("hmin")
        self.fck = self.inputdata.get('fck')
        self.k8 = self.inputdata.get('k8')
        self.aeq_groupe = self.inputdata.get('aeq_groupe')
        self.aeq_isolee = self.inputdata.get('aeq_groupe')

        self.calculation_criteria_traction_shearing()

    def calculation_criteria_traction_shearing(self):
        global ruptbetcombi, ruptaciercombi
        a = self.calculation_criteria_traction()
        b = self.calculation_criteria_shearing()
        print(a, b)

        if a[3] == "Vérification non nécessaire":
            a3 = 0
        else:
            a3 = a[3]

        betaN = max(max(a[0]), a[1], max(a[2]), a3)
        betaV = max(max(b[0]), b[1], b[2])

        if (self.N != 0 or self.Mx != 0 or self.Mz != 0) and (self.Vx != 0 or self.Vz != 0 or self.T != 0):
            if self.TypeCharge == "Statique ou quasi-statique":
                if self.norme == "ETAG":
                    if max(a[0]) < max(a[1], max(a[2]), a3) and max(b[0]) < max(b[1], b[2]):
                        cas = betaN ** 1.5 + betaV ** 1.5
                    else:
                        cas = betaN ** 2 + betaV ** 2
                    ruptaciercombi = min((betaN + betaV) / 1.2, cas)
                    ruptbetcombi = "Non calculé pour l'ETAG"
                else:
                    ruptaciercombi = max(a[0]) ** 2 + max(b[0]) ** 2
                    if self.EDF == "Oui":
                        ruptbetcombi = max(a[1] ** 1.5, (max(a[2])) ** 1.5, a3 ** 1.5) + max(b[2] ** 1.5, b[1] ** 1.5)
                    else:
                        ruptbetcombi = (max(a[1], (max(a[2])), a3) + max(b[2], b[1])) / 1.2

            elif self.TypeCharge == "Sismique C2" or self.TypeCharge == "Sismique C1":
                if self.norme == "ETAG":
                    ruptbetcombi = "Non calculé pour l'ETAG"
                    ruptaciercombi = max(a[0]) + max(b[0])
                else:
                    ruptaciercombi = max(a[0]) + max(b[0])
                    ruptbetcombi = max(a[1], (max(a[2])), a3) + max(b[2], b[1])

        else:
            ruptbetcombi = "Non calculé"
            ruptaciercombi = "Non calculé"
            #for j in range(self.NbFixa):
            #    ctritraccisail0[j, 0] = a[0][j] ** 2 + b[0][j] ** 2
            #ctritraccisail2 = a[1] ** 1.5 + b[2] ** 1.5

        print(ruptbetcombi, ruptaciercombi)
        return ruptbetcombi, ruptaciercombi, a, b

    def calculation_criteria_shearing(self):
        if self.TypeCharge == "Statique ou quasi-statique" or (self.norme == "ETAG" and self.TypeCharge == "Sismique C2" or self.TypeCharge == "Sismique C1"):
            return self.rupture_steel_fixation_without_lever_arm(), self.rupture_concrete_with_lever_arm("", ""), \
                   self.rupture_edge_concrete("", "")
        elif self.TypeCharge == "Sismique C2" and self.norme == "EC2":
            return self.rupture_steel_fixation_without_lever_arm_C2(), self.rupture_concrete_with_lever_arm("", "C2"), \
                   self.rupture_edge_concrete("", "C2")
        elif self.TypeCharge == "Sismique C1" and self.norme == "EC2":
            return self.rupture_steel_fixation_without_lever_arm_C1(), self.rupture_concrete_with_lever_arm("C1", ""), \
                   self.rupture_edge_concrete("C1", "")

    def calculation_criteria_traction(self):
        if self.N == 0 and self.Mx == 0 and self.Mz == 0:
            return [0, 0, 0, 0], 0, [0, 0, 0, 0], 0
        else:
            if self.TypeCharge == "Statique ou quasi-statique" or (self.norme == "ETAG" and self.TypeCharge == "Sismique C2" or self.TypeCharge == "Sismique C1"):
                return self.rupture_steel_fixing(), self.rupture_cone_concrete(), self.rupture_extraction(), \
                    self.rupture_splitting()
            elif self.TypeCharge == "Sismique C2" and self.norme == "EC2":
                return self.rupture_steel_fixing_C2(), self.rupture_cone_concrete_C2(), self.rupture_extraction_C2(), \
                    self.rupture_splitting_C2()
            elif self.TypeCharge == "Sismique C1" and self.norme == "EC2":
                return self.rupture_steel_fixing_C1(), self.rupture_cone_concrete_C1(), self.rupture_extraction_C1(), \
                    self.rupture_splitting_C1()

    def rupture_steel_fixation_without_lever_arm(self):
        gamma = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier sans bras de levier - gamma Ms,V'))
        VRKs = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier sans bras de levier - VRk,s (N)'))
        Ruptureacciersansbraslevier = []
        VedMax = 0

        if self.modele == "HILTI HDA-T M10/20" or self.modele == "HILTI HDA-P M10/20":
            if 10 <= self.tfix < 15:
                VRKs = 65000
            elif 10 <= self.tfix <= 20:
                VRKs = 70000

        if self.modele == "HILTI HDA-T M12/30" or self.modele == "HILTI HDA-T M12/50" or self.modele == \
                "HILTI HDA-P M12/30" or self.modele == "HILTI HDA-P M12/50":
            if 10 <= self.tfix < 20:
                VRKs = 80000
            elif 20 <= self.tfix <= 50:
                VRKs = 100000

        if self.modele == "HILTI HDA-T M16/40" or self.modele == "HILTI HDA-T M16/60" or self.modele == \
                "HILTI HDA-P M16/40" or self.modele == "HILTI HDA-P M16/60":
            if 15 <= self.tfix < 25:
                VRKs = 140000
            elif 25 <= self.tfix <= 60:
                VRKs = 155000

        if self.modele == "HILTI HDA-T M20/50" or self.modele == "HILTI HDA-T M20/100" or self.modele == \
                "HILTI HDA-P M20/50" or self.modele == "HILTI HDA-P M20/100":
            if 20 <= self.tfix < 40:
                VRKs = 205000
            elif 40 <= self.tfix <= 55:
                VRKs = 235000
            elif 55 <= self.tfix <= 100:
                VRKs = 250000
        for j in range(self.NbFixa):
            if self.norme == "ETAG" and self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                Ruptureacciersansbraslevier.append(3.33 * self.Ved[j, 0] / (VRKs / gamma))
            else:
                Ruptureacciersansbraslevier.append(self.Ved[j, 0] / (VRKs / gamma))
            if self.Ved[j, 0] > VedMax:
                VedMax = self.Ved[j, 0]
        #print(gamma, VRKs)
        return Ruptureacciersansbraslevier

    def rupture_concrete_with_lever_arm(self, C1, C2):
        global aeq, VRkcpseis, VRdcpeq
        agap = 0.5
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture du beton par effet de levier - gamma inst'))
        ruptbetonlevierC2 = []
        ruptbetonlevierC1 = []
        ruptbetonlevier = []

        if C1 == "C1" or C2 == "C2":
            if self.NbFixa > 1:
                aeq = self.aeq_groupe
            else:
                aeq = self.aeq_isolee

        if C2 == "C2":
            self.dV_seis_eq = float(self.Recuperationproprietecheville.get_dowel_property('Deplacement deltaV,seis (DLS)'))
            self.dV_seis_req = 3
            rat = self.dV_seis_req / self.dV_seis_eq
            if rat > 1:
                self.dV_seis_eq = self.dV_seis_req

        hef1 = self.calculation_hef(self.scrn, "", self.ccrN)
        scrN1 = self.calculation_scrN(hef1, self.scrn)

        N0 = self.calculation_n0rkc(hef1)
        A0 = scrN1 * scrN1
        a = self.calculation_acn(scrN1, "")
        psisN = self.calculation_psis_n(scrN1, "")
        psireN = self.calculation_psir_eN(hef1)
        if self.norme == "ETAG":
            psiecN = self.calculation_psie_cN(scrN1, self.eV, 2)
        else:
            psiecN = self.calculation_psie_cN(scrN1, self.eV, 2)
        psiMN = 1
        NRkc = self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psiMN, 1)
        if C1 == "C1":
            VRkcp = agap * aeq * self.k8 * NRkc
            VRdcpeq = VRkcp / gamma
            ratio = self.VEdg / VRdcpeq
            self.ruptbetonlevierglob = self.VEdg / VRdcpeq
        elif C2 == "C2":
            VRkcp = agap * aeq * self.k8 * NRkc
            VRdcpeq = VRkcp / gamma
            VRkcpseis = VRdcpeq * (self.dV_seis_req / self.dV_seis_eq)
            ratio = self.VEdg / VRkcpseis
            self.ruptbetonlevierglob = self.VEdg / VRkcpseis

        else:
            VRkcp = self.k8 * NRkc
            ratio = self.VEdg / (VRkcp / gamma)
            if VRkcp == 0:
                self.ruptbetonlevierglob = 0
            else:
                if self.norme == "ETAG" and self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                    self.ruptbetonlevierglob = 3.33 * self.VEdg / (VRkcp / gamma)
                else:
                    self.ruptbetonlevierglob = self.VEdg / (VRkcp / gamma)
        #print(N0, a, A0, psisN, psireN, psiecN, psiMN, NRkc, ratio, k8, VRkcp, gamma, self.VEdg, scrN1, self.ccrN, hef1, self.fck)
        Vedeq = self.VEdg

        # Affichage de VEdg / (VRkcp / gamma)

        if self.NbFixa == 2:
            self.rupture_concrete_with_lever_arm_2_fixing(C1, C2, ratio, agap, gamma, ruptbetonlevierC1,
                                                          ruptbetonlevierC2, ruptbetonlevier)
        if self.NbFixa == 4:
            self.rupture_concrete_with_lever_arm_4_fixing(C1, C2, ratio, agap, gamma, ruptbetonlevierC1,
                                                          ruptbetonlevierC2, ruptbetonlevier)
        return self.ruptbetonlevierglob

    def rupture_concrete_with_lever_arm_2_fixing(self, C1, C2, ratio, agap, gamma, ruptbetonlevierC1, ruptbetonlevierC2,
                                                 ruptbetonlevier):
        for j in range(self.NbFixa):
            if ratio == 0 or np.sign(self.Vedx[0]) != np.sign(self.Vedx[1]) or np.sign(self.Vedz[0]) != \
                    np.sign(self.Vedz[1]):
                hef1 = self.calculation_hef(self.scrn, j, self.ccrN)
                scrN1 = self.calculation_scrN(hef1, self.scrn)
                N0 = self.calculation_n0rkc(hef1)
                A0 = scrN1 * scrN1

                if abs((self.CentreGeo1 - self.PosFix[j, 1]) * self.Tb / self.Iy) > abs(
                        self.Vx / self.NbFixa) and abs(
                    (self.PosFix[j, 0] - self.CentreGeo0) * self.Tb / self.Iy) > abs(self.Vz / self.NbFixa):
                    a = self.calculation_acn_lever(scrN1, j)
                else:
                    a = self.calculation_acn(scrN1, j)
                psisN = self.calculation_psis_n(scrN1, j)
                psireN = self.calculation_psir_eN(hef1)
                psiecN = self.calculation_psie_cN(scrN1, self.eV, 2)
                psiMN = 1
                NRkc = self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psiMN, 1)

                if C1 == "C1":
                    VRkcp = agap * aeq * self.k8 * NRkc
                    VRdcpeq = VRkcp / gamma
                    ruptbetonlevierC1.append(self.Ved[j] / VRdcpeq)
                    if self.Ved[j] / VRdcpeq > ratio:
                        ruptbetonlevierC1glob = self.Ved[j] / VRdcpeq
                        ratio = self.Ved[j] / VRdcpeq
                        Vedeq = self.Ved[j]
                        return ruptbetonlevierC1glob, ruptbetonlevierC1
                    return ruptbetonlevierC1
                elif C2 == "C2":
                    VRkcp = agap * aeq * self.k8 * NRkc
                    VRdcpeq = VRkcp / gamma
                    VRkcpseis = VRdcpeq * (self.dV_seis_req / self.dV_seis_eq)
                    ruptbetonlevierC2.append(self.Ved[j] / VRkcpseis)
                    if self.Ved[j] / VRkcpseis > ratio:
                        ruptbetonlevierC2glob = self.Ved[j] / VRkcpseis
                        ratio = self.Ved[j] / VRkcpseis
                        Vedeq = self.Ved[j]
                        return ruptbetonlevierC2glob, ruptbetonlevierC2
                    return ruptbetonlevierC2
                else:
                    VRkcp = self.k8 * NRkc
                    if a != 0:
                        if self.Ved[j] / (VRkcp / gamma) > ratio:
                            ratio = self.Ved[j] / (VRkcp / gamma)
                            Vedeq = self.Ved[j]
                            if self.norme == "ETAG" and self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                                self.ruptbetonlevierglob = 3.33 * self.Ved[j] / (VRkcp / gamma)
                            else:
                                self.ruptbetonlevierglob = self.Ved[j] / (VRkcp / gamma)
                    else:
                        ruptbetonlevier.append(0)
                        return ruptbetonlevier
        return self.ruptbetonlevierglob

    def rupture_concrete_with_lever_arm_4_fixing(self, C1, C2, ratio, agap, gamma, ruptbetonlevierC1, ruptbetonlevierC2,
                                                 ruptbetonlevier):
        for j in range(self.NbFixa):
            if ratio == 0 or np.sign(self.Vedx[0]) == np.sign(self.Vedx[1]) == np.sign(self.Vedx[2]) == \
                    np.sign(self.Vedx[3]) or np.sign(self.Vedz[0]) == np.sign(self.Vedz[1]) == np.sign(self.Vedz[2]) \
                    == np.sign(self.Vedz[3]):
                pass
            else:
                hef1 = self.calculation_hef(self.scrn, j, self.ccrN)
                scrN1 = self.calculation_scrN(hef1, self.scrn)
                N0 = self.calculation_n0rkc(hef1)
                A0 = scrN1 * scrN1
                if abs((self.CentreGeo1 - self.PosFix[j, 1]) * self.Tb / self.Iy) > abs(
                        self.Vx / self.NbFixa) and abs(
                    (self.PosFix[j, 0] - self.CentreGeo0) * self.Tb / self.Iy) > abs(self.Vz / self.NbFixa):
                    a = self.calculation_acn_lever(scrN1, j)
                else:
                    a = self.calculation_acn(scrN1, j)

                psisN = self.calculation_psis_n(scrN1, "")
                #print(psisN)
                psireN = self.calculation_psir_eN(hef1)
                if self.norme == "ETAG":
                    psiecN = self.calculation_psie_cN(scrN1, self.eV, 2)
                else:
                    psiecN = self.calculation_psie_cN(scrN1, self.eV, 2)
                psiMN = 1
                NRkc = self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psiMN, 1)
                if C1 == "C1":
                    VRkcp = agap * aeq * self.k8 * NRkc
                    VRdcpeq = VRkcp / gamma
                    ruptbetonlevierC1.append(self.Ved[j] / VRdcpeq)
                    if self.Ved[j] / VRdcpeq > ratio:
                        ruptbetonlevierC1glob = self.Ved[j] / VRdcpeq
                        ratio = self.Ved[j] / VRdcpeq
                        Vedeq = self.Ved[j]
                        return ruptbetonlevierC1glob, ruptbetonlevierC1
                    return ruptbetonlevierC1
                elif C2 == "C2":
                    VRkcp = agap * aeq * self.k8 * NRkc
                    VRdcpeq = VRkcp / gamma
                    VRkcpseis = VRdcpeq * (self.dV_seis_req / self.dV_seis_eq)
                    ruptbetonlevierC2.append(self.Ved[j] / VRkcpseis)
                    if self.Ved[j] / VRkcpseis > ratio:
                        ruptbetonlevierC2glob = self.Ved[j] / VRkcpseis
                        ratio = self.Ved[j] / VRkcpseis
                        Vedeq = self.Ved[j]
                        return ruptbetonlevierC2glob, ruptbetonlevierC2
                    return ruptbetonlevierC2
                else:
                    VRkcp = self.k8 * NRkc
                    if a != 0:
                        if self.Ved[j] / (VRkcp / gamma) > ratio:
                            ratio = self.Ved[j] / (VRkcp / gamma)
                            Vedeq = self.Ved[j]
                            if self.norme == "ETAG" and self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                                self.ruptbetonlevierglob = 3.33 * self.Ved[j] / (VRkcp / gamma)
                            else:
                                self.ruptbetonlevierglob = self.Ved[j] / (VRkcp / gamma)
                    else:
                        ruptbetonlevier.append(0)
                        return ruptbetonlevier
                #print(N0, a, A0, psisN, psireN, psiecN, psiMN, NRkc, ratio, k8, VRkcp, gamma, self.VEdg, scrN1,
                      #self.ccrN, hef1, self.fck, self.ruptbetonlevierglob, self.Ved[j] / (VRkcp / gamma), self.Ved[j])
        return self.ruptbetonlevierglob

    def rupture_edge_concrete(self, C1, C2):

        global c1z, c1x, tempx1, tempx2
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture du beton par effet de levier - gamma inst'))
        kt = 1
        agap = 0.5
        if C1 == "C1" or C2 == "C2":
            if self.NbFixa > 1:
                if C1 == "C1" and C2 == "":
                    self.aeq = self.aeq_groupe
                elif C1 == "" and C2 == "C2":
                    self.aeq = 0.85
            else:
                if C1 == "C1" and C2 == "":
                    self.aeq = self.aeq_isolee
                elif C1 == "" and C2 == "C2":
                    self.aeq = 1

        if C2 == "C2":
            self.dV_seis_eq = float(self.Recuperationproprietecheville.get_dowel_property('Deplacement deltaV,seis (DLS)'))
            self.dV_seis_req = 3
            rat = self.dV_seis_req / self.dV_seis_eq
            if rat > 1:
                self.dV_seis_eq = self.dV_seis_req

        ratio1 = 0
        ratio2 = 0
        ratio3 = 0
        ratio4 = 0
        c1 = 0
        if self.NbFixa == 2:
            self.rupture_edge_concrete_2_fixing(C1, C2, gamma, ratio1, ratio2, ratio3, ratio4, c1, agap, kt)
        if self.NbFixa == 4:
            self.rupture_edge_concrete_4_fixing(C1, C2, gamma, ratio1, ratio2, ratio3, ratio4, c1, agap, kt)
        return self.rupturebordbeton

    def rupture_edge_concrete_2_fixing(self, C1, C2, gamma, ratio1, ratio2, ratio3, ratio4, c1, agap, kt):
        global c1z, tempx1, tempx2
        c1z = 0
        if self.cx0 < 500:
            if (self.VEgdx < 0 and self.VEgdz != 0) or (self.VEgdx >= 0 and self.VEgdz != 0) or (
                    self.VEgdx < 0 and self.VEgdz == 0):
                if self.cz0 < 500 and self.cz1 < 500:
                    if max(self.cz0, self.cz1) <= 1.5 * self.cx0 and self.h <= 1.5 * self.cx0:
                        if (self.VEgdx < 0 and self.VEgdz != 0) or (self.VEgdx >= 0 and self.VEgdz != 0):
                            c1x = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5)
                        else:
                            c1x = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5, self.sx0 / 3)
                    else:
                        c1x = self.cx0
                else:
                    c1x = self.cx0
                V0rkcx1 = self.calculation_v0rkc(c1x)

                A0x = 4.5 * c1x ** 2
                Ax = self.calculation_acv("x", c1x)

                psisVx = self.calculation_psis_V(c1x, min(self.cz0, self.cz1))
                psihVx = self.calculation_psih_V(c1x)
                psireVx = 1
                c1z = 0

                if C1 == "C1" or C2 == "C2":
                    if (self.VEgdx < 0 and self.VEgdz != 0) or (self.VEgdx < 0 and self.VEgdz == 0):
                        psiecVx = self.calculation_psie_cN(3 * c1z, np.array([self.eV1, 0]), 4)

                if self.Vedx[0] != 0 and self.Vedx[1] != 0:
                    eV1 = ((self.PosFix[0, 1] - self.CentreGeo1) * self.Vedx[0] + (
                            self.PosFix[1, 1] - self.CentreGeo1) * self.Vedx[
                               1]) / (abs(self.Vedx[0]) + abs(self.Vedx[1]))
                    psiecVx = self.calculation_psie_cN(3 * c1z, np.array([eV1, 0]), 4)
                else:
                    eV1 = 0
                    psiecVx = self.calculation_psie_cN(3 * c1z, np.array([eV1, 0]), 4)

                if ((self.VEgdx < 0 and self.VEgdz != 0) or (
                        self.VEgdx < 0 and self.VEgdz == 0 and (C1 == "C1" or C2 == "C2"))):
                    aV = abs(math.atan(self.Vedz[0, 0] / self.Vx))
                    self.psiaVx = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)

                elif self.VEgdx < 0 and self.VEgdz == 0:
                    aV = abs(math.atan((self.Vedz[0] / 2) / self.Vedx[1]))
                    self.psiaVx = (1 / (math.cos(aV) * math.cos(aV) + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)

                elif self.VEgdx >= 0 and self.VEgdz != 0:
                    self.psiaVx = 2

                tempx1 = self.Ved[0, 0]
                tempx2 = self.Ved[1, 0]

                if tempx1 >= 0:
                    tempx1 = 0
                if tempx2 >= 0:
                    tempx2 = 0

                if C1 == "C1" or C2 == "C2":
                    self.Vrkcx1 = self.calculation_N(V0rkcx1, Ax, A0x, psisVx, psihVx, psiecVx, self.psiaVx,
                                                     psireVx) * agap * self.aeq
                else:
                    self.Vrkcx1 = self.calculation_N(V0rkcx1, Ax, A0x, psisVx, psihVx, psiecVx, self.psiaVx, psireVx)

                if C2 == "C2":
                    VRkcxseis = self.Vrkcx1 * (self.dV_seis_req / self.dV_seis_eq)
                    ratio1 = math.sqrt(self.Vedz[0, 0] ** 2 + (tempx1 + tempx2) ** 2) / (
                            math.sqrt(VRkcxseis ** 2) / gamma)
                else:
                    ratio1 = math.sqrt(self.Vedz[0, 0] ** 2 + (tempx1 + tempx2) ** 2) / (
                            math.sqrt(self.Vrkcx1 ** 2) / gamma)

                Vedeq1 = math.sqrt(self.Vedz[0, 0] ** 2 + (tempx1 + tempx2) ** 2)

                # AFFICHAGE RESULTATS

        if self.cx1 < 500:
            if (self.VEgdx > 0 and self.VEgdz != 0) or (self.VEgdx <= 0 and self.VEgdz != 0) or (
                    self.VEgdx > 0 and self.VEgdz == 0):
                if self.cz0 < 500 and self.cz1 < 500:
                    if max(self.cz0, self.cz1) <= 1.5 * self.cx1 and self.h <= 1.5 * self.cx1:
                        if (self.VEgdx > 0 and self.VEgdz != 0) or (self.VEgdx <= 0 and self.VEgdz != 0):
                            self.c1x = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5)
                        elif self.VEgdx > 0 and self.VEgdz == 0:
                            self.c1x = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5, self.sx0 / 3)
                    else:
                        self.c1x = self.cx1
                else:
                    self.c1x = self.cx1

                V0rkcx2 = self.calculation_v0rkc(self.c1x)

                A0x = 4.5 * self.c1x ** 2
                Ax = self.calculation_acv("x", self.c1x)
                c1z = 0

                psisVx = self.calculation_psis_V(self.c1x, min(self.cz0, self.cz1))
                psihVx = self.calculation_psih_V(self.c1x)
                psireVx = 1

                if self.Vedx[0] != 0 and self.Vedx[1] != 0:
                    eV1 = ((self.PosFix[0, 1] - self.CentreGeo1) * self.Vedx[0] + (
                            self.PosFix[1, 1] - self.CentreGeo1) * self.Vedx[
                               1]) / (abs(self.Vedx[0]) + abs(self.Vedx[1]))
                    self.psiecVx = self.calculation_psie_cN(3 * c1z, np.array([eV1, 0]), 4)
                else:
                    eV1 = 0
                    self.psiecVx = self.calculation_psie_cN(3 * c1z, np.array([eV1, 0]), 4)

                if self.VEgdx <= 0 and self.VEgdz != 0:
                    self.psiaVx = 2

                if C1 == "C1" or C2 == "C2":
                    if (self.VEgdx > 0 and self.VEgdz == 0) or (self.VEgdx > 0 and self.VEgdz != 0):
                        aV = abs(math.atan((self.Vedz[1, 0]) / self.Vx))
                        self.psiaVx = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        self.psiecVx = self.calculation_psie_cN(3 * c1z, np.array([eV1, 0]), 4)
                    elif self.VEgdx <= 0 and self.VEgdz != 0:
                        self.psiecVx = self.calculation_psie_cN(3 * c1z, np.array([eV1, 0]), 4)
                else:
                    if (self.VEgdx > 0 and self.VEgdz == 0) or (self.VEgdx > 0 and self.VEgdz != 0):
                        aV = abs(math.atan((self.Vedz[1, 0]) / self.Vx))
                        self.psiaVx = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)

                if C1 == "C1" or C2 == "C2":
                    self.Vrkcx2 = self.calculation_N(V0rkcx2, Ax, A0x, psisVx, psihVx, self.psiecVx, self.psiaVx,
                                                     psireVx) * agap * self.aeq
                else:
                    self.Vrkcx2 = self.calculation_N(V0rkcx2, Ax, A0x, psisVx, psihVx, self.psiecVx, self.psiaVx,
                                                     psireVx)
                tempx1 = self.Vedx[0]
                tempx2 = self.Vedx[1]

                if tempx1 <= 0:
                    tempx1 = 0
                if tempx2 <= 0:
                    tempx2 = 0

                if C2 == "C2":
                    VRkcxseis = self.Vrkcx2 * (self.dV_seis_req / self.dV_seis_eq)
                    ratio2 = math.sqrt(self.Vedz[0, 0] ** 2 + (tempx1 + tempx2) ** 2) / (
                            math.sqrt(VRkcxseis ** 2) / gamma)
                else:
                    ratio2 = math.sqrt(self.Vedz[1, 0] ** 2 + (tempx1 + tempx2) ** 2) / (
                            math.sqrt(self.Vrkcx2 ** 2) / gamma)
                Vedeq2 = math.sqrt(self.Vedz[1, 0] ** 2 + (tempx1 + tempx2) ** 2)

                if ratio2 > ratio1:
                    # Affichage resultat
                    pass

        if self.cz0 < 500:
            if (self.VEgdx != 0 and self.VEgdz > 0) or (self.VEgdx == 0 and (self.VEgdz < 0 or self.T / 1000 != 0)) or (
                    self.VEgdz < 0 and self.VEgdx != 0):
                if self.cx0 < 500 and self.cx1 < 500:
                    if max(self.cz0, self.cz1) <= 1.5 * self.cz0 and self.h <= 1.5 * self.cz0:
                        c1z = max(max(self.cx0, self.cx1) / 1.5, self.h / 1.5, self.sx0 / 3)
                    else:
                        c1z = self.cz0
                else:
                    c1z = self.cz0

                V0Rkcz = self.calculation_v0rkc(c1z)
                A0z = 4.5 * c1z ** 2

                if self.VEgdz < 0 and self.VEgdx != 0:
                    self.Az = self.calculation_acv("z", self.cz0)
                    self.psisVz = self.calculation_psis_V(self.cz0, min(self.cx0, self.cx1))
                    self.psihVz = self.calculation_psih_V(self.cz0)

                elif (self.VEgdx != 0 and self.VEgdz > 0) or (
                        self.VEgdx == 0 and (self.VEgdz < 0 or self.T / 1000 != 0)):
                    self.Az = self.calculation_acv("z", c1z)
                    self.psisVz = self.calculation_psis_V(c1z, min(self.cx0, self.cx1))
                    self.psihVz = self.calculation_psih_V(c1z)

                eV0 = ((self.PosFix[0, 0] - self.CentreGeo0) * self.Vedz[0, 0] + (
                        self.PosFix[1, 0] - self.CentreGeo0) *
                       self.Vedz[1, 0]) / (
                              abs(self.Vedz[0, 0]) + abs(self.Vedz[1, 0]))
                psiecVz = self.calculation_psie_cN(3 * c1z, np.array([eV0, 0]), 4)

                tempz1 = self.Vedz[0, 0]
                tempz2 = self.Vedz[1, 0]

                if (self.VEgdz < 0 and self.VEgdx != 0) or (self.VEgdx != 0 and self.VEgdz > 0):
                    if tempz1 >= 0:
                        tempz1 = 0
                    if tempz2 >= 0:
                        tempz2 = 0
                elif self.VEgdx == 0 and (self.VEgdz < 0 or self.T / 1000 != 0):
                    if tempz1 <= 0:
                        tempz1 = 0
                    if tempz2 <= 0:
                        tempz2 = 0

                if (self.VEgdx != 0 and self.VEgdz > 0) or (self.VEgdz < 0 and self.VEgdx != 0):
                    aV = abs(math.pi / 2 - math.atan((tempz1 + tempz2) / (self.Vedx[0] + self.Vedx[1])))
                    self.psiaVz = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)

                elif self.VEgdx == 0 and (self.VEgdz < 0 or self.T / 1000 != 0):
                    self.psiaVz = 1

                psireVx = 1

                if C1 == "C1" or C2 == "C2":
                    self.Vrkcz = self.calculation_N(V0Rkcz, self.Az, A0z, self.psisVz, self.psihVz, psiecVz,
                                                    self.psiaVz,
                                                    psireVx) * agap * self.aeq
                else:
                    self.Vrkcz = self.calculation_N(V0Rkcz, self.Az, A0z, self.psisVz, self.psihVz, psiecVz,
                                                    self.psiaVz, psireVx)

                if C2 == "C2":
                    VRkcxseis = self.Vrkcz * (self.dV_seis_req / self.dV_seis_eq)
                    ratio3 = math.sqrt(self.Vedz[0, 0] ** 2 + (tempz1 + tempz1) ** 2) / (
                            math.sqrt(VRkcxseis ** 2) / gamma)
                else:
                    ratio3 = math.sqrt((self.Vedx[0, 0] + self.Vedx[1, 0]) ** 2 + (tempz1 + tempz2) ** 2) / (
                            math.sqrt(self.Vrkcz ** 2) / gamma)

                Vedeq3 = math.sqrt((self.Vedx[0, 0] + self.Vedx[1, 0]) ** 2 + (tempz1 + tempz2) ** 2)

                if ratio3 / kt > max(ratio1, ratio2):
                    # Affichage resultat
                    pass

        if self.cz1 < 500:
            if (self.VEgdz != 0 and self.VEgdx != 0) or ((self.VEgdz > 0 or self.T / 1000 != 0) and self.VEgdx == 0):
                if self.cx0 < 500 and self.cx1 < 500:
                    if max(self.cz0, self.cz1) <= 1.5 * self.cz1 and self.h <= 1.5 * self.cz1:
                        c1z = max(max(self.cx0, self.cx1) / 1.5, self.h / 1.5, self.sx0 / 3)
                    else:
                        c1z = self.cz1
                else:
                    c1z = self.cz1

                V0Rkcz = self.calculation_v0rkc(c1z)
                A0z = 4.5 * c1z ** 2
                Az = self.calculation_acv("z", c1z)
                psisVz = self.calculation_psis_V(c1z, min(self.cx0, self.cx1))
                psihVz = self.calculation_psih_V(c1z)

                eV0 = ((self.PosFix[0, 0] - self.CentreGeo0) * self.Vedz[0, 0] + (
                        self.PosFix[1, 0] - self.CentreGeo0) *
                       self.Vedz[1, 0]) / (
                              abs(self.Vedz[0, 0]) + abs(self.Vedz[1, 0]))
                psiecVz = self.calculation_psie_cN(3 * c1z, np.array([eV0, 0]), 4)

                tempz1 = self.Vedz[0, 0]
                tempz2 = self.Vedz[1, 0]

                if tempz1 <= 0:
                    tempz1 = 0
                if tempz2 <= 0:
                    tempz2 = 0

                if self.VEgdz != 0 and self.VEgdx != 0:
                    aV = abs(math.pi / 2 - math.atan((tempz1 + tempz2) / (self.Vedx[0] + self.Vedx[1])))
                    self.psiaVz = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                elif (self.VEgdz > 0 or self.T / 1000 != 0) and self.VEgdx == 0:
                    self.psiaVz = 1

                psireVx = 1

                if C1 == "C1" or C2 == "C2":
                    Vrkcz = self.calculation_N(V0Rkcz, Az, A0z, psisVz, psihVz, psiecVz, self.psiaVz,
                                               psireVx) * agap * self.aeq
                else:
                    Vrkcz = self.calculation_N(V0Rkcz, Az, A0z, psisVz, psihVz, psiecVz, self.psiaVz, psireVx)

                if C2 == "C2":
                    VRkcxseis = Vrkcz * (self.dV_seis_req / self.dV_seis_eq)
                    ratio4 = math.sqrt(self.Vedz[0, 0] ** 2 + (tempx1 + tempx2) ** 2) / (
                            math.sqrt(VRkcxseis ** 2) / gamma)
                else:
                    ratio4 = math.sqrt((self.Vedx[0] + self.Vedx[1]) ** 2 + (tempz1 + tempz2) ** 2) / (
                            math.sqrt(Vrkcz ** 2) / gamma)

                Vedeq4 = math.sqrt((self.Vedx[0] + self.Vedx[1]) ** 2 + (tempz1 + tempz2) ** 2)

                if ratio4 / kt > max(ratio1, ratio2, ratio3):
                    # Affichage resultat
                    pass

        if max(ratio1, ratio2, ratio3 / kt, ratio4 / kt) == ratio1:
            c1 = self.cx0
            # AFFICHE Vedeq1
        if max(ratio1, ratio2, ratio3 / kt, ratio4 / kt) == ratio2:
            c1 = self.cx1
            # AFFICHE Vedeq2
        if max(ratio1, ratio2, ratio3 / kt, ratio4 / kt) == ratio3:
            c1 = self.cz0
            # AFFICHE Vedeq3
        if max(ratio1, ratio2, ratio3 / kt, ratio4 / kt) == ratio4:
            c1 = self.cz1
            # AFFICHE Vedeq4
        if c1 > 600:
            c1 = 0

        if (c1z == self.cz0 or c1z == self.cz1) and (
                (self.Vedz[0, 0] > 0 > self.Vedz[1, 0]) or (self.Vedz[0, 0] < 0 < self.Vedz[1, 0])):
            kt = self.calculation_kt(c1)
        else:
            kt = 1

        if self.norme == "ETAG":
            if self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                self.rupturebordbeton = 3.33 * max(ratio1, ratio2, ratio3, ratio4)
            else:
                self.rupturebordbeton = max(ratio1, ratio2, ratio3, ratio4)
        else:
            self.rupturebordbeton = max(ratio1, ratio2, ratio3 / kt, ratio4 / kt)

        return self.rupturebordbeton

    def rupture_edge_concrete_4_fixing(self, C1, C2, gamma, ratio1, ratio2, ratio3, ratio4, c1, agap, kt):
        c1z = 0
        c1x = 0
        if self.cx0 < 10 * self.hef and self.cx0 < 60 * self.dnom:
            if (self.VEgdx < 0 and self.VEgdz != 0) or (self.VEgdx < 0 and self.VEgdz == 0) or (
                    self.VEgdx >= 0 and (self.VEgdz != 0 or self.T != 0)):
                if self.cz0 < 10 * self.hef and self.cz0 < 60 * self.dnom and self.cz1 < 10 * self.hef and self.cz1 < 60 * self.dnom:
                    if max(self.cz0, self.cz1) <= 1.5 * self.cx0 and self.h <= 1.5 * self.cx0:
                        if (self.VEgdx < 0 and self.VEgdz != 0) or (
                                self.VEgdx >= 0 and (self.VEgdz != 0 or self.T != 0)):
                            c1x = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5)
                        elif self.VEgdx < 0 and self.VEgdz == 0:
                            c1x = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5, self.sx0 / 3)
                    else:
                        if self.cx0 < self.cx1:
                            c1x = self.cx0
                        else:
                            c1x = self.cx1
                else:
                    c1x = self.cx0

                V0rkcx1 = self.calculation_v0rkc(c1x)
                A0x = 4.5 * c1x ** 2
                Ax = self.calculation_acv("x", c1x)
                psisVx = self.calculation_psis_V(c1x, min(self.cz0, self.cz1))
                psihVx = self.calculation_psih_V(c1x)

                if self.norme == "ETAG":
                    if self.VEgdx < 0 and self.VEgdz != 0:
                        aV = abs(math.atan((self.Vedz[0, 0] + self.Vedz[3, 0]) / self.Vx))
                        self.psiaVx = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                    elif self.VEgdx >= 0 and (self.VEgdz != 0 or self.T != 0):
                        if self.Vx != 0:
                            eVz = ((self.PosFix[0, 1] - self.CentreGeo1) * self.Vedx[0, 0] + (
                                    self.PosFix[2, 1] - self.CentreGeo1) * self.Vedx[2, 0]) / (
                                    (abs(self.Vedx[0, 0]) + abs(self.Vedx[1, 0]) + abs(self.Vedx[2, 0]) + abs(
                                      self.Vedx[3, 0])) * 4)
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([eVz, 0]), 4)
                        else:
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                        if self.Vedx[0, 0] < 0:
                            aV = abs(math.atan(self.Vedz[0, 0] / self.Vedx[0, 0]))
                            self.psiaVx = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        elif self.Vedx[2, 0] < 0:
                            aV = abs(math.atan(self.Vedz[2, 0] / self.Vedx[2, 0]))
                            self.psiaVx = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        else:
                            self.psiaVx = 2.5

                    elif self.VEgdx < 0 and self.VEgdz == 0:
                        self.psiaVx = 1
                        self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)
                else:
                    if self.VEgdx < 0 and self.VEgdz != 0:
                        aV = abs(math.atan((self.Vedz[0, 0] + self.Vedz[3, 0]) / self.Vx))
                        self.psiaVx = (1 / (math.cos(aV) * math.cos(aV) + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                    elif self.VEgdx >= 0 and (self.VEgdz != 0 or self.T != 0):
                        if self.Vx != 0:
                            eVz = ((self.PosFix[0, 1] - self.CentreGeo1) * self.Vedx[0, 0] + (
                            self.PosFix[2, 1] - self.CentreGeo1) * self.Vedx[2, 0]) / (
                                  (abs(self.Vedx[0, 0]) + abs(self.Vedx[1, 0]) + abs(self.Vedx[2, 0]) + abs(
                                      self.Vedx[3, 0])) * 4)
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([eVz, 0]), 4)
                        else:
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                        if self.Vedx[0, 0] < 0:
                            aV = abs(math.atan(self.Vedz[0, 0] / self.Vedx[0, 0]))
                            self.psiaVx = (1 / (math.cos(aV) * math.cos(aV) + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        elif self.Vedx[2, 0] < 0:
                            aV = abs(math.atan(self.Vedz[2, 0] / self.Vedx[2, 0]))
                            self.psiaVx = (1 / (math.cos(aV) * math.cos(aV) + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        else:
                            self.psiaVx = 2

                    elif self.VEgdx < 0 and self.VEgdz == 0:
                        self.psiaVx = 1
                        self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                if C1 == "C1" or C2 == "C2":
                    if self.VEgdx >= 0 and (self.VEgdz != 0 or self.T != 0):
                        if self.Vedx[0, 0] != 0 and self.Vedx[1, 0] != 0 and self.Vedx[2, 0] != 0 and self.Vedx[3, 0] != 0:
                            eVz = ((self.PosFix[0, 1] - self.CentreGeo1) * self.Vedx[0, 0] + (
                                self.PosFix[2, 1] - self.CentreGeo1) * self.Vedx[2, 0]) / (
                                      (abs(self.Vedx[0, 0]) + abs(self.Vedx[1, 0]) + abs(self.Vedx[2, 0]) + abs(
                                          self.Vedx[3, 0])) * 4)
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([eVz, 0]), 4)
                        else:
                            self.psiecVx = 1

                        if self.Vedx[0] < 0:
                            aV = abs(math.atan(self.Vedz[0, 0] / self.Vedx[0, 0]))
                            self.psiaVx = (1 / (math.cos(aV) * math.cos(aV) + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        elif self.Vedx[2] < 0:
                            aV = abs(math.atan(self.Vedz[2, 0] / self.Vedx[2, 0]))
                            self.psiaVx = (1 / (math.cos(aV) * math.cos(aV) + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        else:
                            self.psiaVx = 2

                psireVx = 1

                if C1 == "C1" or C2 == "C2":
                    self.Vrkcx1 = self.calculation_N(V0rkcx1, Ax, A0x, psisVx, psihVx, self.psiecVx, self.psiaVx,
                                                 psireVx) * agap * self.aeq
                else:
                    self.Vrkcx1 = self.calculation_N(V0rkcx1, Ax, A0x, psisVx, psihVx, self.psiecVx, self.psiaVx,
                                                 psireVx)
                #print(V0rkcx1, Ax, A0x, psisVx, psihVx, self.psiecVx, self.psiaVx, psireVx, gamma, self.Vrkcx1 / gamma, self.Vx, self.Vz)
                tempx1 = self.Vedx[0, 0]
                tempx2 = self.Vedx[1, 0]
                tempx3 = self.Vedx[2, 0]
                tempx4 = self.Vedx[3, 0]

                if tempx1 >= 0:
                    tempx1 = 0
                if tempx2 >= 0:
                    tempx2 = 0
                if tempx3 >= 0:
                    tempx3 = 0
                if tempx4 >= 0:
                    tempx4 = 0

                if C2 == "C2":
                    VRkcxseis = self.Vrkcx1 * (self.dV_seis_req / self.dV_seis_eq)
                    ratio1 = math.sqrt(
                    (self.Vedz[0, 0] + self.Vedz[2, 0]) ** 2 + (tempx1 + tempx2 + tempx3 + tempx4) ** 2) / (
                                 math.sqrt(VRkcxseis ** 2) / gamma)
                else:
                    ratio1 = math.sqrt(
                    (self.Vedz[1, 0] + self.Vedz[3, 0]) ** 2 + (tempx1 + tempx2 + tempx3 + tempx4) ** 2) / (
                                 math.sqrt(self.Vrkcx1 ** 2) / gamma)
                Vedeq1 = math.sqrt((self.Vedz[1, 0] + self.Vedz[3, 0]) ** 2 + (tempx1 + tempx2 + tempx3 + tempx4) ** 2)
                #print(Vedeq1, self.Vedz, self.PosFix, self.Iy)

        if self.cx1 < 10 * self.hef and self.cx1 < 60 * self.dnom:
            if (self.VEgdx > 0 and self.VEgdz != 0) or (self.VEgdx <= 0 and self.VEgdz != 0) or (
                    self.VEgdx > 0 and self.VEgdz == 0):
                if self.cz0 < 10 * self.hef and self.cz0 < 60 * self.dnom and self.cz1 < 10 * self.hef and self.cz1 < 60 * self.dnom:
                    if max(self.cz0, self.cz1) <= 1.5 * self.cx1 and self.h <= 1.5 * self.cx1:
                        if (self.VEgdx > 0 and self.VEgdz != 0) or (self.VEgdx <= 0 and self.VEgdz != 0):
                            c1x = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5)
                        elif self.VEgdx > 0 and self.VEgdz == 0:
                            c1x = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5, self.sx0 / 3)
                    else:
                        c1x = self.cx1
                else:
                    c1x = self.cx1

                V0rkcx2 = self.calculation_v0rkc(c1x)
                A0x = 4.5 * c1x ** 2
                Ax = self.calculation_acv("x", c1x)
                psisVx = self.calculation_psis_V(c1x, min(self.cz0, self.cz1))
                psihVx = self.calculation_psih_V(c1x)

                if self.norme == "ETAG":
                    if self.VEgdx > 0 and self.VEgdz != 0:
                        aV = abs(math.atan((self.Vedz[0, 0] + self.Vedz[2, 0]) / self.Vx)) # abs(math.atan((self.Vedz[1, 0] + self.Vedz[3, 0]) / self.Vx))
                        self.psiaVx = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        if self.Vedx[0, 0] < 0 or self.Vedx[2, 0] < 0:
                            eVz = ((self.PosFix[1, 1] - self.CentreGeo1) * self.Vedx[1, 0] + (
                                self.PosFix[3, 1] - self.CentreGeo1) * self.Vedx[3, 0]) / (
                                    abs(self.Vedx[1, 0]) + abs(self.Vedx[3, 0]))
                            #eVz = math.sqrt((((self.Vedz[0, 0] + self.Vedz[2, 0])-(self.Vedz[1, 0] + self.Vedz[3, 0])) ** 2) / (self.Vedz[2, 0] ** 2 + self.Vedx[2, 0] ** 2))
                            #eVz = math.cos(aV) * self.Vedz[1, 0]
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([eVz, 0]), 4)
                        else:
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                    elif self.VEgdx <= 0 and self.VEgdz != 0:
                        if self.Vedx[1, 0] > 0:
                            aV = abs(math.atan(self.Vedz[1, 0] / self.Vedx[1, 0]))
                            self.psiaVx = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        elif self.Vedx[3, 0] > 0:
                            aV = abs(math.atan(self.Vedz[3, 0] / self.Vedx[3, 0]))
                            self.psiaVx = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        else:
                            self.psiaVx = 2.5
                        self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                    elif self.VEgdx > 0 and self.VEgdz == 0:
                        self.psiaVx = 1
                        self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)
                else:
                    if self.VEgdx > 0 and self.VEgdz != 0:
                        aV = abs(math.atan((self.Vedz[0, 0] + self.Vedz[2, 0]) / self.Vx))
                        self.psiaVx = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        if self.Vedx[0, 0] < 0 or self.Vedx[2, 0] < 0:
                            eVz = ((self.PosFix[1, 1] - self.CentreGeo1) * self.Vedx[1, 0] + (
                                self.PosFix[3, 1] - self.CentreGeo1) * self.Vedx[3, 0]) / (
                                    abs(self.Vedx[1, 0]) + abs(self.Vedx[3, 0]))
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([eVz, 0]), 4)
                        else:
                            self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                    elif self.VEgdx <= 0 and self.VEgdz != 0:
                        if self.Vedx[1] > 0:
                            aV = abs(math.atan(self.Vedz[1, 0] / self.Vedx[1, 0]))
                            self.psiaVx = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        elif self.Vedx[3] > 0:
                            aV = abs(math.atan(self.Vedz[3, 0] / self.Vedx[3, 0]))
                            self.psiaVx = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        else:
                            self.psiaVx = 2
                        self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)

                    elif self.VEgdx > 0 and self.VEgdz == 0:
                        self.psiaVx = 1
                        self.psiecVx = self.calculation_psie_cN(3 * c1x, np.array([self.eV1, 0]), 4)
                psireVx = 1

                if C1 == "C1" or C2 == "C2":
                    Vrkcx2 = self.calculation_N(V0rkcx2, Ax, A0x, psisVx, psihVx, self.psiecVx, self.psiaVx,
                                            psireVx) * agap * self.aeq
                else:
                    Vrkcx2 = self.calculation_N(V0rkcx2, Ax, A0x, psisVx, psihVx, self.psiecVx, self.psiaVx, psireVx)
                #print(V0rkcx2, Ax, A0x, psisVx, psihVx, self.psiecVx, self.psiaVx, psireVx, c1x, Vrkcx2)
                tempx1 = self.Vedx[0, 0]
                tempx2 = self.Vedx[1, 0]
                tempx3 = self.Vedx[2, 0]
                tempx4 = self.Vedx[3, 0]
                if tempx1 <= 0:
                    tempx1 = 0
                if tempx2 <= 0:
                    tempx2 = 0
                if tempx3 <= 0:
                    tempx3 = 0
                if tempx4 <= 0:
                    tempx4 = 0

                if C2 == "C2":
                    VRkcxseis = Vrkcx2 * (self.dV_seis_req / self.dV_seis_eq)
                    ratio2 = math.sqrt(
                    (self.Vedz[1, 0] + self.Vedz[3, 0]) ** 2 + (tempx1 + tempx2 + tempx3 + tempx4) ** 2) / (
                                 math.sqrt(VRkcxseis ** 2) / gamma)
                else:
                    ratio2 = math.sqrt(
                    (self.Vedz[0, 0] + self.Vedz[2, 0]) ** 2 + (tempx1 + tempx2 + tempx3 + tempx4) ** 2) / (
                                 math.sqrt(Vrkcx2 ** 2) / gamma)
                Vedeq2 = math.sqrt((self.Vedz[0, 0] + self.Vedz[2, 0]) ** 2 + (tempx1 + tempx2 + tempx3 + tempx4) ** 2)
                #print(Vedeq2)

        if self.cz0 < 10 * self.hef and self.cz0 < 60 * self.dnom:
            if (self.VEgdz < 0 and self.VEgdx != 0) or (self.VEgdx != 0 and self.VEgdz > 0) or (self.VEgdx == 0 and (self.VEgdz < 0 or self.T / 1000 != 0)):
                if self.cx0 < 10 * self.hef and self.cx0 < 60 * self.dnom and self.cx1 < 10 * self.hef and self.cx1 < 60 * self.dnom:
                    if max(self.cz0, self.cz1) <= 1.5 * self.cz0 and self.h <= 1.5 * self.cz0:
                        c1z = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5, self.sx0 / 3)
                    else:
                        if self.cz0 < self.cz1:
                            c1z = self.cz0
                        else:
                            c1z = self.cz1
                else:
                    c1z = self.cz0

                V0rkcz1 = self.calculation_v0rkc(c1z)
                A0z = 4.5 * c1z ** 2
                Az = self.calculation_acv("z", c1z)

                if self.VEgdz < 0 and self.VEgdx != 0:
                    self.psisVz = self.calculation_psis_V(self.cz0, min(self.cx0, self.cx1))
                    self.psihVz = self.calculation_psih_V(self.cz0)

                elif (self.VEgdx != 0 and self.VEgdz > 0) or (self.VEgdx == 0 and (self.VEgdz < 0 or self.T / 1000 != 0)):
                    self.psisVz = self.calculation_psis_V(c1z, min(self.cx0, self.cx1))
                    self.psihVz = self.calculation_psih_V(c1z)

                if self.norme == "ETAG":
                    if self.VEgdz < 0 and self.VEgdx != 0 and C1 == "" and C2 == "":
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / self.VEgdx))
                        eVx = abs(((self.PosFix[0, 0] - self.CentreGeo1) * self.Vedz[0, 0] * 2 + (
                                self.PosFix[1, 0] - self.CentreGeo1) * self.Vedz[1, 0] * 2) / (
                                      self.T / math.sqrt((self.sx0 / 2) ** 2 + (self.sz0 / 2) ** 2)))          # Changement de self.eV0 en eVx
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([eVx, 0]), 4)

                        #print(aV, self.eV0, eVx)

                    elif self.VEgdz < 0 and self.VEgdx != 0 and (C1 == "C1" or C2 == "C2"):
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / (self.Vedx[0, 0] + self.Vedx[1, 0])))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV0, 0]), 4)

                    elif self.VEgdx != 0 and self.VEgdz > 0:
                        self.psiaVz = 2.5
                        self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV0, 0]), 4)

                    elif self.VEgdx == 0 and (self.VEgdz < 0 or self.T / 1000 != 0):
                        self.psiecVz = 1 / (1 + (2 * (abs(self.eV0) / (c1z * 3))))
                        if self.Vedz[0, 0] < 0 or self.Vedz[1, 0] < 0:
                            eVx = ((self.PosFix[0, 0] - self.CentreGeo1) * self.Vedz[0, 0] * 2 + (
                                self.PosFix[1, 0] - self.CentreGeo1) * self.Vedz[1, 0] * 2) / (
                                      self.T / math.sqrt((self.sx0 / 2) ** 2 + (self.sz0 / 2) ** 2))
                            self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([eVx, 0]), 4)
                        else:
                            self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV1, 0]), 4)

                        if C1 == "C1" or C2 == "C2":
                            aV = abs(
                            math.pi / 2 - math.atan(abs((self.Vedx[0, 0] + self.Vedx[1, 0])) / abs(self.Vedz[1, 0])))
                            self.psiaVz = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        else:
                            aV = abs(math.atan(abs((self.Vedx[0, 0] + self.Vedx[1, 0]) / 2) / abs(self.Vedz[1, 0])))
                            self.psiaVz = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                else:
                    if self.VEgdz < 0 and self.VEgdx != 0 and C1 == "" and C2 == "":
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / self.VEgdx))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV0, 0]), 4)

                    elif self.VEgdz < 0 and self.VEgdx != 0 and (C1 == "C1" or C2 == "C2"):
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / (self.Vedx[0] + self.Vedx[1])))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                        self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV0, 0]), 4)

                    elif self.VEgdx != 0 and self.VEgdz > 0:
                        self.psiaVz = 2
                        self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV0, 0]), 4)

                    elif self.VEgdx == 0 and (self.VEgdz < 0 or self.T / 1000 != 0):
                        self.psiecVz = 1 / (1 + (2 * (abs(self.eV0) / (c1z * 3))))
                        if self.Vedz[0, 0] < 0 or self.Vedz[1, 0] < 0:
                            eVx = ((self.PosFix[0, 0] - self.CentreGeo1) * self.Vedz[0, 0] * 2 + (
                            self.PosFix[1, 0] - self.CentreGeo1) * self.Vedz[1, 0] * 2) / (
                                  self.T / math.sqrt((self.sx0 / 2) ** 2 + (self.sz0 / 2) ** 2))
                            self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([eVx, 0]), 4)
                            #print(eVx)
                        else:
                            self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV1, 0]), 4)

                    if C1 == "C1" or C2 == "C2":
                        aV = abs(
                        math.pi / 2 - math.atan(abs((self.Vedx[0, 0] + self.Vedx[1, 0])) / abs(self.Vedz[1, 0])))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                    else:
                        aV = abs(math.atan(abs((self.Vedx[0, 0] + self.Vedx[1, 0]) / 2) / abs(self.Vedz[1, 0])))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                eVx = ((self.PosFix[0, 0] - self.CentreGeo1) * self.Vedz[0, 0] * 2 + (
                        self.PosFix[1, 0] - self.CentreGeo1) * self.Vedz[1, 0] * 2) / (
                              self.T / math.sqrt((self.sx0 / 2) ** 2 + (self.sz0 / 2) ** 2))
                self.psiecVz = self.calculation_psie_cN(3 * c1z, np.array([eVx, 0]), 4)
                #print(eVx)
                psireVz = 1
                if C1 == "C1" or C2 == "C2":
                    Vrkcz = self.calculation_N(V0rkcz1, Az, A0z, self.psisVz, self.psihVz, self.psiecVz, self.psiaVz,
                                           psireVz) * agap * self.aeq
                else:
                    Vrkcz = self.calculation_N(V0rkcz1, Az, A0z, self.psisVz, self.psihVz, self.psiecVz,
                                           self.psiaVz, psireVz)

                tempz1 = self.Vedz[0, 0]
                tempz2 = self.Vedz[1, 0]
                tempz3 = self.Vedz[2, 0]
                tempz4 = self.Vedz[3, 0]
                #print(V0rkcz1, Az, A0z, self.psisVz, self.psihVz, self.psiecVz, self.psiaVz, psireVz, self.cx0, self.cx1)
                if tempz1 >= 0:
                    tempz1 = 0
                if tempz2 >= 0:
                    tempz2 = 0
                if tempz3 >= 0:
                    tempz3 = 0
                if tempz4 >= 0:
                    tempz4 = 0

                if C2 == "C2":
                    VRkczseis = Vrkcz * (self.dV_seis_req / self.dV_seis_eq)
                    ratio3 = math.sqrt(
                    (self.Vedx[1] + self.Vedx[0]) ** 2 + (tempz1 + tempz2 + tempz3 + tempz4) ** 2) / (
                                 math.sqrt(VRkczseis ** 2) / gamma)
                else:
                    ratio3 = math.sqrt(
                    (self.Vedx[1, 0] + self.Vedx[0, 0]) ** 2 + (tempz1 + tempz2 + tempz3 + tempz4) ** 2) / (
                                 math.sqrt(Vrkcz ** 2) / gamma)
                Vedeq3 = math.sqrt((self.Vedx[1, 0] + self.Vedx[0, 0]) ** 2 + (tempz1 + tempz2 + tempz3 + tempz4) ** 2)

        if self.cz1 < 10 * self.hef and self.cz1 < 60 * self.dnom:
            if (self.VEgdz > 0 and self.VEgdx != 0) or (self.VEgdz < 0 and self.VEgdx != 0) or (
                    self.VEgdx == 0 and (self.VEgdz > 0 or self.T / 1000 != 0)):
                if self.cx0 < 10 * self.hef and self.cx0 < 60 * self.dnom and self.cx1 < 10 * self.hef and self.cx1 < 60 * self.dnom:
                    if max(self.cz0, self.cz1) <= 1.5 * self.cz1 and self.h <= 1.5 * self.cz1:
                        c1z = max(max(self.cz0, self.cz1) / 1.5, self.h / 1.5, self.sx0 / 3)
                    else:
                        c1z = self.cz1
                else:
                    c1z = self.cz1

                V0rkcz2 = self.calculation_v0rkc(c1z)
                A0z = 4.5 * c1z ** 2
                Az = self.calculation_acv("z", c1z)
                psisVz = self.calculation_psis_V(c1z, min(self.cx0, self.cx1))
                psihVz = self.calculation_psih_V(c1z)
                psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV0, 0]), 4)

                if self.norme == "ETAG":
                    if self.VEgdz > 0 and self.VEgdx != 0 and C1 == "" and C2 == "":
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / (self.Vedx[2, 0] + self.Vedx[3, 0])))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                        #eVx = abs(((self.PosFix[0, 0] - self.CentreGeo1) * self.Vedz[0, 0] * 2 + (
                        #        self.PosFix[1, 0] - self.CentreGeo1) * self.Vedz[1, 0] * 2) / (
                        #                  self.T / math.sqrt((self.sx0 / 2) ** 2 + (self.sz0 / 2) ** 2)))
                        psiecVz = self.calculation_psie_cN(3 * c1z, np.array([self.eV0, 0]), 4)

                    elif (self.VEgdz < 0 and self.VEgdx != 0) or (
                        self.VEgdx == 0 and (self.VEgdz > 0 or self.T / 1000 != 0)):
                        #self.psiaVz = 2.5
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / (self.Vedx[2, 0] + self.Vedx[3, 0])))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                    elif self.VEgdz > 0 and self.VEgdx != 0 and (C1 == "C1" or C2 == "C2"):
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / (self.Vedx[2, 0] + self.Vedx[3, 0])))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (math.sin(aV) / 2.5) ** 2)) ** (1 / 2)
                else:
                    if self.VEgdz > 0 and self.VEgdx != 0 and C1 == "" and C2 == "":
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / self.VEgdx))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)
                    elif (self.VEgdz < 0 and self.VEgdx != 0) or (self.VEgdx == 0 and (self.VEgdz > 0 or self.T / 1000 != 0)):
                        self.psiaVz = 2
                    elif self.VEgdz > 0 and self.VEgdx != 0 and (C1 == "C1" or C2 == "C2"):
                        aV = abs(math.pi / 2 - math.atan(self.VEgdz / (self.Vedx[2, 0] + self.Vedx[3, 0])))
                        self.psiaVz = (1 / (math.cos(aV) ** 2 + (0.5 * math.sin(aV)) ** 2)) ** (1 / 2)

                psireVz = 1
                if C1 == "C1" or C2 == "C2":
                    Vrkcz = self.calculation_N(V0rkcz2, Az, A0z, psisVz, psihVz, psiecVz, self.psiaVz,
                                           psireVz) * agap * self.aeq
                else:
                    Vrkcz = self.calculation_N(V0rkcz2, Az, A0z, psisVz, psihVz, psiecVz, self.psiaVz, psireVz)

                tempz1 = self.Vedz[0, 0]
                tempz2 = self.Vedz[1, 0]
                tempz3 = self.Vedz[2, 0]
                tempz4 = self.Vedz[3, 0]
                #print(V0rkcz2, Az, A0z, psisVz, psihVz, psiecVz, self.psiaVz, psireVz)
                if tempz1 <= 0:
                    tempz1 = 0
                if tempz2 <= 0:
                    tempz2 = 0
                if tempz3 <= 0:
                    tempz3 = 0
                if tempz4 <= 0:
                    tempz4 = 0
                #print(Vrkcz, V0rkcz2, Az, A0z, psisVz, psihVz, psiecVz, self.psiaVz, psireVz)
                if C2 == "C2":
                    VRkczseis = Vrkcz * (self.dV_seis_req / self.dV_seis_eq)
                    ratio4 = math.sqrt(
                    (self.Vedx[2, 0] + self.Vedx[3, 0]) ** 2 + (tempz1 + tempz2 + tempz3 + tempz4) ** 2) / (
                                 math.sqrt(VRkczseis ** 2) / gamma)
                else:
                    ratio4 = math.sqrt(
                    (self.Vedx[2, 0] + self.Vedx[3, 0]) ** 2 + (tempz1 + tempz2 + tempz3 + tempz4) ** 2) / (
                                 math.sqrt(Vrkcz ** 2) / gamma)
                Vedeq4 = math.sqrt((self.Vedx[2, 0] + self.Vedx[3, 0]) ** 2 + (tempz1 + tempz2 + tempz3 + tempz4) ** 2)

        if (c1z == self.cz0 or c1z == self.cz1) and (
                (self.Vedz[0, 0] > 0 > self.Vedz[1, 0]) or (self.Vedz[0, 0] < 0 < self.Vedz[1, 0]) or (
                self.Vedz[0, 0] < 0 < self.Vedz[2, 0]) or (self.Vedz[2, 0] < 0 < self.Vedz[1, 0])):
            kt = self.calculation_kt(c1)
        else:
            kt = 1
        #print(ratio1, ratio2, ratio3, ratio4)
        if self.norme == "ETAG":
            if self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                self.rupturebordbeton = 1.5 * max(ratio1, ratio2, ratio3, ratio4)
            else:
                self.rupturebordbeton = max(ratio1, ratio2, ratio3, ratio4)
        else:
            self.rupturebordbeton = max(ratio1, ratio2, ratio3 / kt, ratio4 / kt)

        if max(ratio1, ratio2, ratio3 / kt, ratio4 / kt) == ratio1:
            c1 = self.cx0
            # AFFICHE Vedeq1
        if max(ratio1, ratio2, ratio3 / kt, ratio4 / kt) == ratio2:
            c1 = self.cx1
            # AFFICHE Vedeq2
        if max(ratio1, ratio2, ratio3 / kt, ratio4 / kt) == ratio3:
            c1 = self.cz0
            # AFFICHE Vedeq3
        if max(ratio1, ratio2, ratio3 / kt, ratio4 / kt) == ratio4:
            c1 = self.cz1
            # AFFICHE Vedeq4
        if c1 > 600:
            c1 = 0
        return self.rupturebordbeton

    def rupture_steel_fixation_without_lever_arm_C1(self):
        global V0Rks
        gamma = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier sans bras de levier - gamma Ms,seis C1'))
        V0Rks = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier sans bras de levier - VRk,s,seis C1'))
        ruptacierfixasansbraslevierC1 = []
        Vedmax = 0
        agap = 0.5

        if self.NbFixa > 1:
            aeq = 0.85
        else:
            aeq = 1

        if self.modele == "HILTI HDA-T M10/20":
            if 10 <= self.tfix < 15:
                V0Rks = 65000
            elif 10 <= self.tfix <= 20:
                V0Rks = 70000

        if self.modele == "HILTI HDA-T M12/30" or self.modele == "HILTI HDA-T M12/50":
            if 10 <= self.tfix < 20:
                V0Rks = 80000
            elif 20 <= self.tfix <= 50:
                V0Rks = 100000

        if self.modele == "HILTI HDA-T M16/40" or self.modele == "HILTI HDA-T M16/60":
            if 15 <= self.tfix < 25:
                V0Rks = 140000
            elif 25 <= self.tfix <= 30:
                V0Rks = 155000
            elif 30 <= self.tfix <= 35:
                V0Rks = 170000
            elif 35 <= self.tfix <= 60:
                V0Rks = 190000

        if self.modele == "HILTI HDA-T M20/50" or self.modele == "HILTI HDA-T M20/100":
            if 20 <= self.tfix < 40:
                V0Rks = 205000
            elif 40 <= self.tfix <= 55:
                V0Rks = 235000
            elif 55 <= self.tfix <= 100:
                V0Rks = 250000

        if self.modele == "HILTI HDA-P M10/20":
            V0Rks = 22000
        if self.modele == "HILTI HDA-P M12/30" or self.modele == "HILTI HDA-P M12/50":
            V0Rks = 30000
        if self.modele == "HILTI HDA-P M16/40" or self.modele == "HILTI HDA-P M16/60":
            V0Rks = 62000
        if self.modele == "HILTI HDA-P M20/50" or self.modele == "HILTI HDA-P M20/100":
            V0Rks = 92000

        VRKs = agap * aeq * V0Rks

        VRdseq = VRKs / gamma

        for j in range(self.NbFixa):
            a = self.Ved[j] / VRdseq
            ruptacierfixasansbraslevierC1.append(a[0])
            if self.Ved[j] > Vedmax:
                Vedmax = self.Ved[j]

        return ruptacierfixasansbraslevierC1

    def rupture_steel_fixation_without_lever_arm_C2(self):
        global V0Rks
        gamma = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier sans bras de levier - gamma Ms,seis C2'))
        V0Rks = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier sans bras de levier - VRk,s,seis C2'))
        ruptacierfixasansbraslevierC2 = []
        Vedmax = 0
        agap = 0.5

        if self.NbFixa > 1:
            aeq = 0.85
        else:
            aeq = 1

        dV_seis_eq = float(self.Recuperationproprietecheville.get_dowel_property('Deplacement deltaV,seis (DLS)'))
        dV_seis_req = 3
        rat = dV_seis_req / dV_seis_eq
        if rat > 1:
            dV_seis_eq = dV_seis_req

        if self.modele == "HILTI HDA-T M10/20":
            if 10 <= self.tfix < 15:
                V0Rks = 39000
            elif 10 <= self.tfix <= 20:
                V0Rks = 42000

        if self.modele == "HILTI HDA-T M12/30" or self.modele == "HILTI HDA-T M12/50":
            if 10 <= self.tfix < 20:
                V0Rks = 56000
            elif 20 <= self.tfix <= 50:
                V0Rks = 70000

        if self.modele == "HILTI HDA-T M16/40" or self.modele == "HILTI HDA-T M16/60":
            if 15 <= self.tfix < 25:
                V0Rks = 84000
            elif 25 <= self.tfix <= 30:
                V0Rks = 93000
            elif 30 <= self.tfix <= 35:
                V0Rks = 102000
            elif 35 <= self.tfix <= 60:
                V0Rks = 114000

        if self.modele == "HILTI HDA-T M20/50" or self.modele == "HILTI HDA-T M20/100":
            if 20 <= self.tfix < 40:
                V0Rks = 144000
            elif 40 <= self.tfix <= 55:
                V0Rks = 165000
            elif 55 <= self.tfix <= 100:
                V0Rks = 175000

        if self.modele == "HILTI HDA-P M10/20":
            V0Rks = 20000
        if self.modele == "HILTI HDA-P M12/30" or self.modele == "HILTI HDA-P M12/50":
            V0Rks = 24000
        if self.modele == "HILTI HDA-P M16/40" or self.modele == "HILTI HDA-P M16/60":
            V0Rks = 56000
        if self.modele == "HILTI HDA-P M20/50" or self.modele == "HILTI HDA-P M20/100":
            V0Rks = 83000

        VRKs = agap * aeq * V0Rks

        VRdseq = VRKs / gamma

        VRKsseis = VRdseq * (dV_seis_req / dV_seis_eq)

        for j in range(self.NbFixa):
            a = self.Ved[j] / VRKsseis
            ruptacierfixasansbraslevierC2.append(a[0])
            if self.Ved[j] > Vedmax:
                Vedmax = self.Ved[j]
        return ruptacierfixasansbraslevierC2

    def rupture_steel_fixing(self):
        gamma = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier - gamma Ms,N'))
        NRks = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier - NRk,s (N)'))
        Nedmax = 0
        ruptureacierfixa = []

        for j in range(self.NbFixa):
            if self.norme == "ETAG" and self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                rupture = 1.5 * round(self.NEd[j, 0] / (NRks / gamma), 3)
            else:
                rupture = round(self.NEd[j, 0] / (NRks / gamma), 3)
            if self.NEd[j] > Nedmax:
                Nedmax = self.NEd[j, 0]
            ruptureacierfixa.append(rupture)
        return ruptureacierfixa

    def rupture_cone_concrete(self):
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par cone beton et par fendage - gamma inst'))
        hef1c = self.calculation_hef(self.scrn, "", self.ccrN)
        scrN1 = self.calculation_scrN(hef1c, self.scrn)
        N0 = self.calculation_n0rkc(hef1c)
        a = self.calculation_acn(scrN1, "")
        A0 = scrN1 * scrN1
        psisN = self.calculation_psis_n(scrN1, "")
        psireN = self.calculation_psir_eN(hef1c)
        psiecN = self.calculation_psie_cN(scrN1, self.eN, 0)
        psiMN = self.calculation_psi_MN(hef1c, "")
        NRkc = self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psiMN, 1)
        if self.norme == "ETAG" and self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
            ruptureconebeton = 1.5 * self.NEdg / (NRkc / gamma)
        else:
            ruptureconebeton = self.NEdg / (NRkc / gamma)
        #print(N0, a, A0, psisN, psireN, psiecN, psiMN, NRkc, scrN1, hef1c, self.NEdg, gamma)
        return ruptureconebeton

    def rupture_extraction(self):
        #print(self.typebeton)
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par extraction glissement - gamma inst beton C20/25'))
        NRkp = self.calculation_NRkp()
        psic = float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par extraction glissement - facteur acroissement pour beton psi c {}'.format(self.typebeton)))
        NRkp = NRkp * psic
        ratio = 0
        ruptureextrac = []
        #print(NRkp, psic, gamma, self.NEd)
        for j in range(self.NbFixa):
            if NRkp == 0:
                ruptureextrac.append(0)
            else:
                if self.norme == "ETAG" and self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                    ruptureextrac.append(1.5 * round(self.NEd[j, 0] / (NRkp / gamma), 3))
                else:
                    ruptureextrac.append(round(self.NEd[j, 0] / (NRkp / gamma), 3))
                if self.NEd[j, 0] / (NRkp / gamma) > ratio:
                    ratio = self.NEd[j, 0] / (NRkp / gamma)
                    Nedeq = self.NEd[j, 0]
        return ruptureextrac

    def rupture_splitting(self):
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par cone beton et par fendage - gamma inst'))
        cmin = self.calculation_cmin("")
        hef1 = self.calculation_hef(self.scrsp, "", self.ccrsp)
        scrsp1 = self.calculation_scrN(hef1, self.scrsp)
        hef1c = self.calculation_hef(self.scrn, "", self.ccrN)
        if (cmin >= 1.2 * (scrsp1 / 2) and self.h >= self.hmin and self.norme == "EC2") or (cmin >= 1.2 *
                    (self.scrsp / 2) and self.h >= 2 * self.hef and self.norme == "ETAG"):

            if self.NbFixa == 2:
                self.textresult = "Vérification non nécessaire"
            elif self.NbFixa == 4:
                self.textresult = "Vérification non nécessaire"
            return self.textresult

        else:
            if self.NbFixa == 2:
                self.textresult = ""
            elif self.NbFixa == 4:
                self.textresult = ""

        if self.norme == "ETAG":
            N0 = self.calculation_n0rkc(hef1)
        else:
            N0 = self.calculation_N0Rksp(hef1c)
        A0 = scrsp1 * scrsp1
        a = self.calculation_acn(scrsp1, "")
        psireN = self.calculation_psir_eN(hef1)
        psisN = self.calculation_psis_n(scrsp1, "")
        psiecN = self.calculation_psie_cN(scrsp1, self.eN, 1)
        psihsp = self.calculation_psih_sp()
        NRksp = self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psihsp, 1)
        #print(N0, a, A0, psisN, psireN, psiecN, psihsp, hef1, hef1c, scrsp1, "he")
        cmin = self.calculation_cmin("")
        if cmin < 1.2 * self.ccrsp:
            if self.norme == "ETAG" and self.TypeCharge == "Sismique C1" or self.TypeCharge == "Sismique C2":
                ruptfendgroupe = 1.5 * self.NEdg / (NRksp / gamma)
            else:
                ruptfendgroupe = self.NEdg / (NRksp / gamma)
        else:
            ruptfendgroupe = 0
        return ruptfendgroupe

    def rupture_steel_fixing_C1(self):
        ratio = 0
        agap = 1
        aeq = 1
        gamma = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier - gamma Ms,seis C1'))
        N0Rks = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier - NRk,s,seis (N) C1'))
        NRks = agap * aeq * N0Rks
        NRdseq = NRks / gamma
        NEdeq = self.NEd[0, 0]
        ruptacierfixac1 = []

        for j in range(self.NbFixa):
            ruptacierfixac1.append(self.NEd[j, 0] / NRdseq)
            if self.NEd[j, 0] / NRdseq > ratio:
                ratio = self.NEd[j, 0]
                NEdeq = self.NEd[j, 0]
        return ruptacierfixac1

    def rupture_cone_concrete_C1(self):
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par cone beton - gamma inst C1'))
        agap = 1
        tempaeq = 0

        for j in range(self.NbFixa):
            if self.NEd[j, 0] != 0:
                tempaeq = tempaeq + 1

        if tempaeq > 1:
            aeq = self.aeq_groupe
        else:
            aeq = self.aeq_isolee

        hef1c = self.calculation_hef(self.scrn, "", self.ccrN)
        scrN1 = self.calculation_scrN(hef1c, self.scrn)
        N0 = self.calculation_n0rkc(hef1c)
        a = self.calculation_acn(scrN1, "")

        A0 = scrN1 * scrN1

        psisN = self.calculation_psis_n(scrN1, "")
        psireN = self.calculation_psir_eN(hef1c)
        psiecN = self.calculation_psie_cN(scrN1, self.eN, 0)
        psiMN = self.calculation_psi_MN(hef1c, "")
        NRkc = agap * aeq * self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psiMN, 1)
        NRdc = NRkc / gamma
        ruptureconebetonC1 = self.NEdg / NRdc

        return ruptureconebetonC1

    def rupture_extraction_C1(self):
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par extraction glissement - gamma inst C1'))
        agap = 1
        tempaeq = 0
        ruptureextraC1 = []
        ratio = 0

        for j in range(self.NbFixa):
            if self.NEd[j, 0] != 0:
                tempaeq = tempaeq + 1

        if tempaeq > 1:
            aeq = 0.85
        else:
            aeq = 1

        NRkp = self.calculation_NRkp_C1()
        psic = float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par extraction glissement - facteur acroissement pour beton psi c {}'.format(self.typebeton)))
        NRkpeq = NRkp * agap * aeq

        NRdp = (NRkpeq * psic) / gamma

        for j in range(self.NbFixa):
            if NRkp == 0:
                ruptureextraC1.append(0)
            else:
                ruptureextraC1.append(self.NEd[j, 0] / NRdp)
                if (self.NEd[j, 0] / NRdp) > ratio:
                    ratio = self.NEd[j, 0] / NRdp
                    NEdeq = self.NEd[j, 0]

        return ruptureextraC1

    def rupture_splitting_C1(self):
        global textresult
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par cone beton - gamma inst C1'))
        agap = 1
        tempaeq = 0
        hef1c = self.calculation_hef(self.scrn, "", self.ccrN)

        for j in range(self.NbFixa):
            if self.NEd[j, 0] != 0:
                tempaeq = tempaeq + 1

        if tempaeq > 1:
            aeq = 0.85
        else:
            aeq = 1

        cmin = self.calculation_cmin("")

        hef1 = self.calculation_hef(self.scrsp, "", self.ccrsp)
        scrsp1 = self.calculation_scrN(hef1, self.scrsp)

        if cmin >= 1.2 * (scrsp1 / 2) and self.h >= self.hmin:

            if self.NbFixa == 2:
                textresult = "Vérification non nécessaire"
            elif self.NbFixa == 4:
                textresult = "Vérification non nécessaire"
            return textresult

        else:
            if self.NbFixa == 2:
                textresult = ""
            elif self.NbFixa == 4:
                textresult = ""

        if self.calculation_N0Rksp_C1(hef1c) < self.calculation_n0rkc(hef1c):
            N0 = self.calculation_N0Rksp_C1(hef1c)
        else:
            N0 = self.calculation_n0rkc(hef1c)

        A0 = scrsp1 * scrsp1
        a = self.calculation_acn(scrsp1, "")
        psireN = self.calculation_psir_eN(hef1)
        psisN = self.calculation_psis_n(scrsp1, "")
        psiecN = self.calculation_psie_cN(scrsp1, self.eN, 1)
        psihsp = self.calculation_psih_sp()
        dictio = [{"modele": "HILTI HSL 3-G M10", "valeur1": 90.67, "valeur2": 49.38},
                  {"modele": "HILTI HSL 3-G M12", "valeur1": 164.27, "valeur2": 82.97},
                  {"modele": "HILTI HSL 3-G M16", "valeur1": 193.8, "valeur2": 138.43},
                  {"modele": "HILTI HSL 3-G M20", "valeur1": 227.23, "valeur2": 162.31},
                  {"modele": "HILTI HDA-T M10/20", "valeur1": 141.67, "valeur2": 101.19},
                  {"modele": "HILTI HDA-P M10/20", "valeur1": 94.4},
                  {"modele": "HILTI HDA-T M12/30", "valeur1": 198.33, "valeur2": 141.67},
                  {"modele": "HILTI HDA-T M12/50", "valeur1": 198.33, "valeur2": 141.67},
                  {"modele": "HILTI HDA-T M16/40", "valeur1": 425, "valeur2": 303.57},
                  {"modele": "HILTI HDA-T M16/60", "valeur1": 425, "valeur2": 303.57},
                  {"modele": "HILTI HDA-T M20/50", "valeur1": 538.33, "valeur2": 384.52},
                  {"modele": "HILTI HDA-T M20/100", "valeur1": 538.33, "valeur2": 384.52}]

        malist1 = []
        for g in dictio:
            malist1.append(g.get("{}".format("modele")))

        if self.etat == "Fissuré":
            if (
                    self.gamme == "HSL 3-G" or self.gamme == "HDA-T" or self.modele == "HILTI HDA-P M10/20") and self.modele != "HILTI HSL 3-G M8":
                valeur1 = dictio[malist1.index(self.modele)]['valeur1']
                N0 = min(N0, 7.5 * self.fck * valeur1)
        elif self.etat == "Non fissuré":
            if (self.gamme == "HSL 3-G" or self.gamme == "HDA-T") and self.modele != "HILTI HSL 3-G M8":
                valeur2 = dictio[malist1.index(self.modele)]['valeur2']
                N0 = min(N0, 10.5 * self.fck * valeur2)

        NRksp = agap * aeq * self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psihsp, 1)
        NRdsp = NRksp / gamma
        cmin = self.calculation_cmin("")

        if cmin < 1.2 * self.ccrsp:
            rupturefendC1 = self.NEdg / NRdsp

        else:
            rupturefendC1 = 0

        return rupturefendC1

    def rupture_steel_fixing_C2(self):
        ratio = 0
        agap = 1
        aeq = 1

        dN_seis_eq = float(self.Recuperationproprietecheville.get_dowel_property('Deplacement deltaN,seis (DLS)'))
        if self.norme == "ETAG":
            dN_seis_req = 3.95
        else:
            dN_seis_req = 3
        rat = dN_seis_req / dN_seis_eq
        if rat > 1:
            dN_seis_eq = dN_seis_req

        gamma = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier - gamma Ms,seis C2'))
        N0Rks = float(self.Recuperationproprietecheville.get_dowel_property('Rupture acier - NRk,s,seis (N) C2'))
        NRks = agap * aeq * N0Rks
        NRdseq = NRks / gamma
        NRKsseis = NRdseq * (dN_seis_req / dN_seis_eq)
        ruptacierfixac2 = []
        #print(gamma, N0Rks, NRks, NRdseq, NRKsseis, dN_seis_eq)
        NEdeq = self.NEd[0, 0]

        for j in range(self.NbFixa):
            rupture = self.NEd[j, 0] / NRKsseis
            if self.NEd[j, 0] / NRKsseis > ratio:
                ratio = self.NEd[j, 0] / NRKsseis
                NEdeq = self.NEd[j, 0]
            ruptacierfixac2.append(rupture)
        return ruptacierfixac2

    def rupture_cone_concrete_C2(self):
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par cone beton - gamma inst C2'))

        tempaeq = 0

        for j in range(self.NbFixa):
            if self.NEd[j, 0] != 0:
                tempaeq = tempaeq + 1

        if tempaeq > 1:
            aeq = self.aeq_groupe
        else:
            aeq = self.aeq_groupe

        agap = 1

        dN_seis_eq = float(self.Recuperationproprietecheville.get_dowel_property('Deplacement deltaN,seis (DLS)'))
        dN_seis_req = 3
        rat = dN_seis_req / dN_seis_eq

        if rat > 1:
            dN_seis_eq = dN_seis_req

        hef1c = self.calculation_hef(self.scrn, "", self.ccrN)
        scrN1 = self.calculation_scrN(hef1c, self.scrn)
        N0 = self.calculation_n0rkc(hef1c)
        a = self.calculation_acn(scrN1, "")
        A0 = scrN1 * scrN1
        psisN = self.calculation_psis_n(scrN1, "")
        psireN = self.calculation_psir_eN(hef1c)
        psiecN = self.calculation_psie_cN(scrN1, self.eN, 0)
        psiMN = self.calculation_psi_MN(hef1c, "")
        NRkc = agap * aeq * self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psiMN, 1)
        NRdc = NRkc / gamma
        NRKcseis = NRdc * (dN_seis_req / dN_seis_eq)
        ruptconebetonC2 = self.NEdg / NRKcseis

        return ruptconebetonC2

    def rupture_extraction_C2(self):
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par extraction glissement - gamma inst C2'))
        agap = 1
        tempaeq = 0
        ruptureextraC2 = []
        ratio = 0

        for j in range(self.NbFixa):
            if self.NEd[j, 0] != 0:
                tempaeq = tempaeq + 1

        if tempaeq > 1:
            aeq = 0.85
        else:
            aeq = 1

        dN_seis_eq = float(self.Recuperationproprietecheville.get_dowel_property('Deplacement deltaN,seis (DLS)'))
        dN_seis_req = 3
        rat = dN_seis_req / dN_seis_eq
        if rat > 1:
            dN_seis_eq = dN_seis_req

        NRkp = self.calculation_NRkp_C2()
        psic = float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par extraction glissement - facteur acroissement pour beton psi c {}'.format(self.typebeton)))
        NRkpeq = NRkp * agap * aeq
        NRdp = (NRkpeq * psic) / gamma
        NRkpseis = NRdp * (dN_seis_req / dN_seis_eq)

        for j in range(self.NbFixa):
            if NRkp == 0:
                ruptureextraC2.append(0)
            else:
                ruptureextraC2.append(self.NEd[j, 0] / NRkpseis)
                if self.NEd[j, 0] / NRkpseis > ratio:
                    ratio = self.NEd[j, 0] / NRkpseis
                    NEdeq = self.NEd[j, 0]

        return ruptureextraC2

    def rupture_splitting_C2(self):
        global textresult
        gamma = self.calculation_gamma_c() * float(self.Recuperationproprietecheville.get_dowel_property(
            'Rupture par cone beton - gamma inst C2'))
        agap = 1
        tempaeq = 0
        hef1c = self.calculation_hef(self.scrn, "", self.ccrN)

        for j in range(self.NbFixa):
            if self.NEd[j, 0] != 0:
                tempaeq = tempaeq + 1

        if tempaeq > 1:
            aeq = 0.85
        else:
            aeq = 1

        dN_seis_eq = self.Recuperationproprietecheville.get_dowel_property('Deplacement deltaN,seis (DLS)')
        dN_seis_req = 3
        rat = dN_seis_req / dN_seis_eq
        if rat > 1:
            dN_seis_eq = dN_seis_req

        cmin = self.calculation_cmin("")

        hef1 = self.calculation_hef(self.scrsp, "", self.ccrsp)
        scrsp1 = self.calculation_scrN(hef1, self.scrsp)

        if cmin >= 1.2 * (scrsp1 / 2) and self.h >= self.hmin:

            if self.NbFixa == 2:
                textresult = "Vérification non nécessaire"
            elif self.NbFixa == 4:
                textresult = "Vérification non nécessaire"
            return textresult

        else:
            if self.NbFixa == 2:
                textresult = ""
            elif self.NbFixa == 4:
                textresult = ""

        if self.calculation_N0Rksp_C1(hef1c) < self.calculation_n0rkc(hef1c):
            N0 = self.calculation_N0Rksp_C2(hef1c)
        else:
            N0 = self.calculation_n0rkc(hef1c)

        A0 = scrsp1 * scrsp1
        a = self.calculation_acn(scrsp1, "")
        psireN = self.calculation_psir_eN(hef1)
        psisN = self.calculation_psis_n(scrsp1, "")
        psiecN = self.calculation_psie_cN(scrsp1, self.eN, 1)
        psihsp = self.calculation_psih_sp()

        dictio = [{"modele": "HILTI HSL 3-G M10", "valeur1": 69.13, "valeur2": 49.38},
                  {"modele": "HILTI HSL 3-G M12", "valeur1": 164.27, "valeur2": 82.97},
                  {"modele": "HILTI HSL 3-G M16", "valeur1": 193.8, "valeur2": 138.43},
                  {"modele": "HILTI HSL 3-G M20", "valeur1": 227.23, "valeur2": 162.31},
                  {"modele": "HILTI HDA-T M10/20", "valeur1": 141.67, "valeur2": 101.19},
                  {"modele": "HILTI HDA-T M12/30", "valeur1": 198.33, "valeur2": 141.67},
                  {"modele": "HILTI HDA-T M12/50", "valeur1": 198.33, "valeur2": 141.67},
                  {"modele": "HILTI HDA-T M16/40", "valeur1": 425, "valeur2": 303.57},
                  {"modele": "HILTI HDA-T M16/60", "valeur1": 425, "valeur2": 303.57},
                  {"modele": "HILTI HDA-T M20/50", "valeur1": 538.33, "valeur2": 384.52},
                  {"modele": "HILTI HDA-T M20/100", "valeur1": 538.33, "valeur2": 384.52}]

        malist1 = []
        for g in dictio:
            malist1.append(g.get("{}".format("modele")))

        if self.etat == "Fissuré":
            if (self.gamme == "HSL 3-G" or self.gamme == "HDA-T") and self.modele != "HILTI HSL 3-G M8":
                valeur1 = dictio[malist1.index(self.modele)]['valeur1']
                N0 = min(N0, 7.5 * self.fck * valeur1)
        elif self.etat == "Non fissuré":
            if (self.gamme == "HSL 3-G" or self.gamme == "HDA-T") and self.modele != "HILTI HSL 3-G M8":
                valeur2 = dictio[malist1.index(self.modele)]['valeur2']
                N0 = min(N0, 10.5 * self.fck * valeur2)

        NRksp = agap * aeq * self.calculation_N(N0, a, A0, psisN, psireN, psiecN, psihsp, 1)
        NRdsp = NRksp / gamma
        NRKspseis = NRdsp * (dN_seis_req / dN_seis_eq)
        cmin = self.calculation_cmin("")
        if cmin < 1.2 * self.ccrsp:
            ruptfendageC2 = self.NEdg / NRKspseis
        else:
            ruptfendageC2 = 0

        return ruptfendageC2

    def calculation_gamma_c(self):

        if self.txt == "Situations permanentes et transitoires":
            calculation_gamma_c = 1.5
        else:
            calculation_gamma_c = 1.2

        return calculation_gamma_c

    def calculation_hef(self, scrN, j, ccrN): ####  GROSSE MODIF enlever le if j == "":
        NbBord = self.calculation_number_edge(scrN)
        cmax = self.calculation_cmax(scrN, "")
        smax = self.calculation_smax(scrN)
        if NbBord >= 3:
            if cmax / ccrN >= smax / scrN:
                self.hef1 = (cmax / ccrN) * self.hef
            else:
                self.hef1 = (smax / scrN) * self.hef
        else:
            self.hef1 = self.hef
        return self.hef1

    def calculation_cmax(self, scrN, j):
        ccrN = 0.5 * scrN
        cmax = 0

        if j == "":
            if ccrN >= self.cx0 >= cmax:
                cmax = self.cx0

            if ccrN >= self.cx1 >= cmax:
                cmax = self.cx1

            if ccrN >= self.cz0 >= cmax:
                cmax = self.cz0

            if ccrN >= self.cz1 >= cmax:
                cmax = self.cz1

        else:
            if ccrN >= self.DistFixBord[j, 0, 0] >= cmax:
                cmax = self.DistFixBord[j, 0, 0]

            if ccrN >= self.DistFixBord[j, 0, 1] >= cmax:
                cmax = self.DistFixBord[j, 0, 1]

            if ccrN >= self.DistFixBord[j, 1, 0] >= cmax:
                cmax = self.DistFixBord[j, 1, 0]

            if ccrN >= self.DistFixBord[j, 1, 1] >= cmax:
                cmax = self.DistFixBord[j, 1, 1]

        if cmax >= ccrN or cmax == 0:
            cmax = ccrN
        #print(cmax)
        return cmax

    def calculation_smax(self, scrN):
        global scrN1
        smin = self.calculation_smin()
        smax = smin
        NbBord = self.calculation_number_edge(scrN)
        scrN1 = 0

        if NbBord == 3:
            if smin == self.sx0 or smin == self.sx1:
                smax = self.sz0 + self.sz1
                scrN1 = np.sign(self.sz0) * scrN + np.sign(self.sz1) * scrN

            elif smin == self.sz0 or smin == self.sz1:
                smax = self.sx0 + self.sx1
                scrN1 = np.sign(self.sx0) * scrN + np.sign(self.sx1) * scrN
        else:
            if np.sign(self.sx0) * scrN + np.sign(self.sx1) * scrN >= self.sx0 + self.sx1 >= smax:
                smax = self.sx0 + self.sx1
                scrN1 = np.sign(self.sx0) * scrN + np.sign(self.sx1) * scrN

            if np.sign(self.sz0) * scrN + np.sign(self.sz1) * scrN >= self.sz0 + self.sz1 >= smax:
                smax = self.sz0 + self.sz1
                scrN1 = np.sign(self.sz0) * scrN + np.sign(self.sz1) * scrN

        if smax >= scrN1:
            smax = scrN1

        return smax

    def calculation_smin(self):
        smin = self.sx0

        if smin >= self.sx1 != 0:
            smin = self.sx1

        if smin >= self.sz0 != 0:
            smin = self.sz0

        if smin >= self.sz1 != 0:
            smin = self.sz1

        return smin

    def calculation_cmin(self, j):
        if j == "":
            cmin = self.cx0

            if self.cx1 <= cmin:
                cmin = self.cx1

            if self.cz0 <= cmin:
                cmin = self.cz0

            if self.cz1 <= cmin:
                cmin = self.cz1
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

    def calculation_scrN(self, hef1, scrN):
        return (hef1 / self.hef) * scrN

    def calculation_n0rkc(self, hef1):
        k1 = self.calculation_k1()
        return k1 * (self.fck ** 0.5) * (hef1 ** 1.5)

    def calculation_k1(self):
        if self.norme == "ETAG":
            if self.etat == "Fissuré":
                if self.gamme == "HDA-T" or self.gamme == "HDA-P":
                    k1 = 8.3
                else:
                    k1 = 7.2
            else:
                if self.gamme == "HDA-T" or self.gamme == "HDA-P":
                    k1 = 11.6
                else:
                    k1 = 10.1
        else:
            if self.etat == "Fissuré":
                k1 = float(self.Recuperationproprietecheville.get_dowel_property('Rupture par cone beton et par fendage - kcr,N'))
            else:
                k1 = float(self.Recuperationproprietecheville.get_dowel_property('Rupture par cone beton et par fendage - kucr,N'))
        return k1

    def calculation_acn(self, scrN1, j):
        ccrN1 = 0.5 * scrN1
        Ax = 0
        Az = 0
        S1 = np.zeros((4, 2))
        S2 = np.zeros((4, 2))
        S3 = np.zeros((4, 2))
        S4 = np.zeros((4, 2))

        if j == "":
            if self.cx0 >= ccrN1:
                Ax = ccrN1
            else:
                Ax = self.cx0

            if self.sx0 >= scrN1:
                Ax = Ax + scrN1
            else:
                Ax = Ax + self.sx0

            if self.sx1 >= scrN1:
                Ax = Ax + scrN1
            else:
                Ax = Ax + self.sx1

            if self.cx1 >= ccrN1:
                Ax = Ax + ccrN1
            else:
                Ax = Ax + self.cx1

            if self.cz0 >= ccrN1:
                Az = ccrN1
            else:
                Az = self.cz0

            if self.sz0 >= scrN1:
                Az = Az + scrN1
            else:
                Az = Az + self.sz0

            if self.sz1 >= scrN1:
                Az = Az + scrN1
            else:
                Az = Az + self.sz1

            if self.cz1 >= ccrN1:
                Az = Az + ccrN1
            else:
                Az = Az + self.cz1

        else:
            if self.DistFixFix[j, 0, 0] == 0:
                if self.DistFixBord[j, 0, 0] >= ccrN1:
                    Ax = ccrN1
                else:
                    Ax = self.DistFixBord[j, 0, 0]

            else:
                if self.DistFixFix[j, 0, 0] >= scrN1:
                    Ax = scrN1
                else:
                    Ax = self.DistFixFix[j, 0, 0] / 2

            if self.DistFixFix[j, 0, 1] == 0:
                if self.DistFixBord[j, 0, 1] >= ccrN1:
                    Ax = Ax + ccrN1
                else:
                    Ax = Ax + self.DistFixBord[j, 0, 1]

            else:
                if self.DistFixFix[j, 0, 1] >= scrN1:
                    Ax = Ax + scrN1
                else:
                    Ax = Ax + self.DistFixFix[j, 0, 1] / 2

            if self.DistFixFix[j, 1, 0] == 0:
                if self.DistFixBord[j, 1, 0] >= ccrN1:
                    Az = ccrN1
                else:
                    Az = self.DistFixBord[j, 1, 0]

            else:
                if self.DistFixFix[j, 1, 0] >= scrN1:
                    Az = scrN1
                else:
                    Az = self.DistFixFix[j, 1, 0] / 2

            if self.DistFixFix[j, 1, 1] == 0:
                if self.DistFixBord[j, 1, 1] >= ccrN1:
                    Az = Az + ccrN1
                else:
                    Az = Az + self.DistFixBord[j, 1, 1]

            else:
                if self.DistFixFix[j, 1, 1] >= scrN1:
                    Az = Az + scrN1
                else:
                    Az = Az + self.DistFixFix[j, 1, 1] / 2

        calculation_acn = Ax * Az
        #print(calculation_acn, ccrN1)

        if self.NbFixa == 2:
            AcN = Ax * Az
            if self.NEd[0] <= 0:
                AcN = AcN - (self.sx0 - ccrN1 + min(ccrN1, self.cx0)) * (min(ccrN1, self.cz0) + min(ccrN1, self.cz1))
                if self.NEd[1] <= 0:
                    AcN = 0
            if self.NEd[1] <= 0:
                AcN = AcN - (self.sx0 - ccrN1 + min(ccrN1, self.cx1)) * (min(ccrN1, self.cz0) + min(ccrN1, self.cz1))
                if self.NEd[0] <= 0:
                    AcN = 0

            calculation_acn = AcN

        if self.NbFixa == 4:

            if self.NEd[0] <= 0:
                calcChev1 = False
            else:
                calcChev1 = True

            if self.NEd[1] <= 0:
                calcChev2 = False
            else:
                calcChev2 = True

            if self.NEd[2] <= 0:
                calcChev3 = False
            else:
                calcChev3 = True

            if self.NEd[3] <= 0:
                calcChev4 = False
            else:
                calcChev4 = True

            if not calcChev1 and not calcChev2 and not calcChev3 and not calcChev4:
                return calculation_acn
            else:
                pass

            if calcChev1:
                if calcChev2:
                    S1[0, 0] = -min(ccrN1, self.cx0)
                    S1[1, 0] = min(ccrN1, self.sx0 / 2)
                    S1[2, 0] = -min(ccrN1, self.cx0)
                    S1[3, 0] = min(ccrN1, self.sx0 / 2)
                else:
                    S1[0, 0] = -min(ccrN1, self.cx0)
                    S1[1, 0] = ccrN1
                    S1[2, 0] = -min(ccrN1, self.cx0)
                    S1[3, 0] = ccrN1

                if calcChev3:
                    S1[0, 1] = -min(ccrN1, self.cz0)
                    S1[1, 1] = -min(ccrN1, self.cz0)
                    S1[2, 1] = min(ccrN1, self.sz0 / 2)
                    S1[3, 1] = min(ccrN1, self.sz0 / 2)
                else:
                    S1[0, 1] = -min(ccrN1, self.cz0)
                    S1[1, 1] = -min(ccrN1, self.cz0)
                    S1[2, 1] = ccrN1
                    S1[3, 1] = ccrN1

            else:
                S1[0, 0] = 0
                S1[1, 0] = 0
                S1[2, 0] = 0
                S1[3, 0] = 0
                S1[0, 1] = 0
                S1[1, 1] = 0
                S1[2, 1] = 0
                S1[3, 1] = 0

            AcN1 = Arithmetique().Surface(S1)

            if calcChev2:
                if calcChev1:
                    S2[0, 0] = self.sx0 - min(ccrN1, self.sx0 / 2)
                    S2[1, 0] = self.sx0 + min(ccrN1, self.cx1)
                    S2[2, 0] = self.sx0 - min(ccrN1, self.sx0 / 2)
                    S2[3, 0] = self.sx0 + min(ccrN1, self.cx1)
                else:
                    S2[0, 0] = self.sx0 - ccrN1
                    S2[1, 0] = self.sx0 + min(ccrN1, self.cx1)
                    S2[2, 0] = self.sx0 - ccrN1
                    S2[3, 0] = self.sx0 + min(ccrN1, self.cx1)

                if calcChev4:
                    S2[0, 1] = -min(ccrN1, self.cz0)
                    S2[1, 1] = -min(ccrN1, self.cz0)
                    S2[2, 1] = min(ccrN1, self.sz0 / 2)
                    S2[3, 1] = min(ccrN1, self.sz0 / 2)
                else:
                    S2[0, 1] = -min(ccrN1, self.cz0)
                    S2[1, 1] = -min(ccrN1, self.cz0)
                    S2[2, 1] = ccrN1
                    S2[3, 1] = ccrN1

            else:
                S2[0, 0] = 0
                S2[1, 0] = 0
                S2[2, 0] = 0
                S2[3, 0] = 0
                S2[0, 1] = 0
                S2[1, 1] = 0
                S2[2, 1] = 0
                S2[3, 1] = 0

            AcN2 = Arithmetique().Surface(S2)

            if calcChev3:
                if calcChev4:
                    S3[0, 0] = -min(ccrN1, self.cx0)
                    S3[1, 0] = min(ccrN1, self.sx0 / 2)
                    S3[2, 0] = -min(ccrN1, self.cx0)
                    S3[3, 0] = min(ccrN1, self.sx0 / 2)
                else:
                    S3[0, 0] = -min(ccrN1, self.cx0)
                    S3[1, 0] = ccrN1
                    S3[2, 0] = -min(ccrN1, self.cx0)
                    S3[3, 0] = ccrN1

                if calcChev1:
                    S3[0, 1] = self.sz0 - min(ccrN1, self.sz0 / 2)
                    S3[1, 1] = self.sz0 - min(ccrN1, self.sz0 / 2)
                    S3[2, 1] = self.sz0 + min(ccrN1, self.cz1)
                    S3[3, 1] = self.sz0 + min(ccrN1, self.cz1)
                else:
                    S3[0, 1] = self.sz0 - ccrN1
                    S3[1, 1] = self.sz0 - ccrN1
                    S3[2, 1] = self.sz0 + min(ccrN1, self.cz1)
                    S3[3, 1] = self.sz0 + min(ccrN1, self.cz1)

            else:
                S3[0, 0] = 0
                S3[1, 0] = 0
                S3[2, 0] = 0
                S3[3, 0] = 0
                S3[0, 1] = 0
                S3[1, 1] = 0
                S3[2, 1] = 0
                S3[3, 1] = 0

            AcN3 = Arithmetique().Surface(S3)

            if calcChev4:
                if calcChev3:
                    S4[0, 0] = self.sx0 - min(ccrN1, self.sx0 / 2)
                    S4[1, 0] = self.sx0 + min(ccrN1, self.cx1)
                    S4[2, 0] = self.sx0 - min(ccrN1, self.sx0 / 2)
                    S4[3, 0] = self.sx0 + min(ccrN1, self.cx1)
                else:
                    S4[0, 0] = self.sx0 - ccrN1
                    S4[1, 0] = self.sx0 + min(ccrN1, self.cx1)
                    S4[2, 0] = self.sx0 - ccrN1
                    S4[3, 0] = self.sx0 + min(ccrN1, self.cx1)

                if calcChev2:
                    S4[0, 1] = self.sz0 - min(ccrN1, self.sz0 / 2)
                    S4[1, 1] = self.sz0 - min(ccrN1, self.sz0 / 2)
                    S4[2, 1] = self.sz0 + min(ccrN1, self.cz1)
                    S4[3, 1] = self.sz0 + min(ccrN1, self.cz1)
                else:
                    S4[0, 1] = self.sz0 - ccrN1
                    S4[1, 1] = self.sz0 - ccrN1
                    S4[2, 1] = self.sz0 + min(ccrN1, self.cz1)
                    S4[3, 1] = self.sz0 + min(ccrN1, self.cz1)

            else:
                S4[0, 0] = 0
                S4[1, 0] = 0
                S4[2, 0] = 0
                S4[3, 0] = 0
                S4[0, 1] = 0
                S4[1, 1] = 0
                S4[2, 1] = 0
                S4[3, 1] = 0

            AcN4 = Arithmetique().Surface(S4)
            #print(AcN1, AcN2, AcN3, AcN4)
            #print(S1, S2, S3, S4)
            if j == "":
                calculation_acn = AcN1 + AcN2 + AcN3 + AcN4
            elif j == 0:
                calculation_acn = AcN1
            elif j == 1:
                calculation_acn = AcN2
            elif j == 2:
                calculation_acn = AcN3
            elif j == 3:
                calculation_acn = AcN4
            if calcChev1 is True and calcChev4 is True:
                calculation_acn = calculation_acn - Arithmetique().Intersection(S4, S1)

            if calcChev2 is True and calcChev3 is True:
                calculation_acn = calculation_acn - Arithmetique().Intersection(S3, S2)
        return calculation_acn

    def calculation_psis_n(self, scrN1, j):

        if j == "":
            cmin = self.calculation_cmin("")

            psisN = 0.7 + 0.3 * (cmin / (scrN1 / 2))
        else:
            cmin = self.calculation_cmin(j)

            psisN = 0.7 + 0.3 * (cmin / (scrN1 / 2))
            #print(scrN1, "je", psisN)

        if psisN >= 1:
            psisN = 1
        #print(psisN)
        return psisN

    def calculation_psir_eN(self, hef1):
        if self.armature == "Oui":
            if hef1 < 100:
                psireN = 0.5 + (hef1 / 200)

            else:
                psireN = 1
        else:
            psireN = 1

        return psireN

    def calculation_psie_cN(self, scrN1, eN, a):
        if self.norme == "ETAG" :#or self.norme == "EC2":
            if scrN1 < 300:
                scrN1 = 300
        if eN[0] != 0:
            psiecN1 = 1 / (1 + (2 * (abs(eN[0] / scrN1))))
        else:
            psiecN1 = 1

        if eN[1] != 0:
            psiecN2 = 1 / (1 + (2 * (abs(eN[1] / scrN1))))
        else:
            psiecN2 = 1

        if a == 0:
            pass  # Affichage de resultat

        elif a == 1:
            pass  # Affichage de resultat

        elif a == 2:
            pass  # Affichage de resultat
        #print(psiecN2, psiecN1)
        return psiecN1 * psiecN2

    def calculation_N(self, N0, a, A0, psi1, psi2, psi3, psi4, psi5):
        N = N0 * (a / A0) * psi1 * psi2 * psi3 * psi4 * psi5
        return N

    def calculation_acn_lever(self, scrN1, j):
        Ax = 0
        Az = 0
        ccrN1 = 0.5 * scrN1

        if self.DistFixFix[j, 0, 0] == 0:
            if self.DistFixBord[j, 0, 0] >= ccrN1:
                Ax = ccrN1
            else:
                Ax = self.DistFixBord[j, 0, 0]
        else:
            if self.DistFixFix[j, 0, 0] / 2 >= scrN1 / 2:
                Ax = scrN1 / 2
            else:
                Ax = self.DistFixFix[j, 0, 0] / 2

        if self.DistFixFix[j, 0, 1] == 0:
            if self.DistFixBord[j, 0, 1] >= ccrN1:
                Ax = Ax + ccrN1
            else:
                Ax = Ax + self.DistFixBord[j, 0, 1]
        else:
            if self.DistFixFix[j, 0, 1] / 2 >= scrN1 / 2:
                Ax = Ax + scrN1 / 2
            else:
                Ax = Ax + self.DistFixFix[j, 0, 1] / 2

        if self.DistFixFix[j, 1, 0] == 0:
            if self.DistFixBord[j, 1, 0] >= ccrN1:
                Az = ccrN1
            else:
                Az = self.DistFixBord[j, 1, 0]
        else:
            if self.DistFixFix[j, 1, 0] / 2 >= scrN1 / 2:
                Az = scrN1 / 2
            else:
                Az = self.DistFixFix[j, 1, 0] / 2

        if self.DistFixFix[j, 1, 1] == 0:
            if self.DistFixBord[j, 1, 1] >= ccrN1:
                Az = Az + ccrN1
            else:
                Az = Az + self.DistFixBord[j, 1, 1]
        else:
            if self.DistFixFix[j, 1, 1] / 2 >= scrN1 / 2:
                Az = Az + scrN1 / 2
            else:
                Az = Az + self.DistFixFix[j, 1, 1] / 2

        return Ax * Az

    def calculation_v0rkc(self, c1):
        dnom = self.dnom
        k9 = self.calculation_k9()

        if dnom <= 24:
            lf = self.hef
            if lf >= 12 * dnom:
                lf = 12 * dnom

        else:
            lf = self.hef
            if 8 * dnom >= 300:
                max = 8 * dnom
            else:
                max = 300

            if lf >= max:
                lf = max

        if self.modele == "HILTI HDA-T M10/20" or self.modele == "HILTI HDA-P M10/20":
            lf = 70
            dnom = 19
        if self.modele == "HILTI HDA-T M12/30" or self.modele == "HILTI HDA-T M12/50" or self.modele == "HILTI HDA-P M12/30" or self.modele == "HILTI HDA-P M12/50":
            lf = 88
            dnom = 21
        if self.modele == "HILTI HDA-T M16/40" or self.modele == "HILTI HDA-T M16/60" or self.modele == "HILTI HDA-P M16/40" or self.modele == "HILTI HDA-P M16/60":
            lf = 90
            dnom = 29
        if self.modele == "HILTI HDA-T M20/50" or self.modele == "HILTI HDA-T M20/100" or self.modele == "HILTI HDA-P M20/50" or self.modele == "HILTI HDA-P M20/100":
            lf = 120
            dnom = 35
        #print(lf, c1)
        aa = 0.1 * ((lf / c1) ** 0.5)
        bb = 0.1 * ((dnom / c1) ** 0.2)
        calculation_v0rkc = k9 * (dnom ** aa) * (lf ** bb) * (self.fck ** 0.5) * (c1 ** 1.5)
        return calculation_v0rkc

    def calculation_k9(self):
        if self.etat == "Fissuré":
            k9 = 1.7
        else:
            k9 = 2.4
        return k9

    def calculation_acv(self, dir, c1):

        if dir == "x":
            if self.cz0 <= 1.5 * c1:
                self.A1 = self.cz0
            else:
                self.A1 = 1.5 * c1

            if self.sz0 + self.sz1 <= np.sign(self.sz0) * 3 * c1 + np.sign(self.sz1) * 3 * c1:
                self.A1 = self.A1 + self.sz0 + self.sz1
            else:
                self.A1 = self.A1 + np.sign(self.sz0) * 3 * c1 + np.sign(self.sz1) * 3 * c1

            if self.cz1 <= 1.5 * c1:
                self.A1 = self.A1 + self.cz1
            else:
                self.A1 = self.A1 + 1.5 * c1

        elif dir == "z":
            if self.cx0 <= 1.5 * c1:
                self.A1 = self.cx0
            else:
                self.A1 = 1.5 * c1

            if self.sx0 + self.sx1 <= np.sign(self.sx0) * 3 * c1 + np.sign(self.sx1) * 3 * c1:
                self.A1 = self.A1 + self.sx0 + self.sx1
            else:
                self.A1 = self.A1 + np.sign(self.sx0) * 3 * c1 + np.sign(self.sx1) * 3 * c1

            if self.cx1 <= 1.5 * c1:
                self.A1 = self.A1 + self.cx1
            else:
                self.A1 = self.A1 + 1.5 * c1

            #if self.norme == "ETAG":
                #    if self.sx0 <= 3 * c1 and self.cx0 <= 1.5 * c1:
                #    self.A1 = 1.5 * c1 + self.sx0 + self.cx0
                #elif self.sx0 <= 3 * c1 and self.cx1 <= 1.5 * c1:
            #    self.A1 = 1.5 * c1 + self.sx0 + self.cx1

        if self.h <= 1.5 * c1:
            Ay = self.h
        else:
            Ay = 1.5 * c1
        #print(self.A1, Ay, c1, self.sz0, self.cz0)
        return self.A1 * Ay

    def calculation_psis_V(self, c1, c2):
        psisV = 0.7 + 0.3 * c2 / (1.5 * c1)
        if psisV >= 1:
            psisV = 1
        return psisV

    def calculation_psih_V(self, c1):
        psihV = (1.5 * c1 / self.h) ** 0.5
        if psihV <= 1:
            psihV = 1
        return psihV

    def calculation_kt(self, c1):
        scrit = 1.5 * c1
        if self.sx0 <= scrit:
            kt = 0.8
        else:
            kt = 1
        return kt

    def calculation_psi_MN(self, hef1, j):
        if j == "":
            c = self.calculation_cmin("")
            if self.NEdg != 0:
                if c < 1.5 * hef1:
                    psiMN = 1
                elif c >= 1.5 * hef1 and abs(self.CEd / self.NEdg) < 0.8:
                    psiMN = 1
                elif abs(self.z / hef1) >= 1.5:
                    psiMN = 1
                else:
                    psiMN = 2 - (self.z / (1.5 * hef1))
            else:
                psiMN = 1
        else:
            c = self.calculation_cmin(j)
            if self.NEdg != 0:
                if c < 1.5 * hef1:
                    psiMN = 1
                elif c >= 1.5 * hef1 and abs(self.CEd / self.NEd[j, 0]) < 0.8:
                    psiMN = 1
                elif abs(self.z / hef1) >= 1.5:
                    psiMN = 1
                else:
                    psiMN = 2 - (self.z / (1.5 * hef1))
            else:
                psiMN = 1

        return psiMN

    def calculation_NRkp(self):
        if self.etat == "Non fissuré":
            if self.Recuperationproprietecheville.get_dowel_property(
                    'Rupture par extraction glissement - NRk,p,uncr (N) beton C20/25') == "non determinante":
                self.NRkp = 0
            else:
                self.NRkp = float(self.Recuperationproprietecheville.get_dowel_property(
                    'Rupture par extraction glissement - NRk,p,uncr (N) beton C20/25'))

        elif self.etat == "Fissuré":
            if self.Recuperationproprietecheville.get_dowel_property(
                    'Rupture par extraction glissement - NRk,p,cr (N) beton C20/25') == "non determinante":
                self.NRkp = 0
            else:
                self.NRkp = float(self.Recuperationproprietecheville.get_dowel_property(
                    'Rupture par extraction glissement - NRk,p,cr (N) beton C20/25'))
        return self.NRkp

    def calculation_N0Rksp(self, hef1):
        NRkp = self.calculation_NRkp()

        N0Rkc = self.calculation_n0rkc(hef1)

        if NRkp <= N0Rkc and NRkp != 0:
            calculation_N0Rksp = NRkp
        else:
            calculation_N0Rksp = N0Rkc
        return calculation_N0Rksp

    def calculation_psih_sp(self):
        c1 = self.calculation_cmin("")
        if self.norme == "EC2":
            max = ((self.hef + 1.5 * c1) / self.hmin) ** (2 / 3)
            if max <= 1:
                max = 1
            elif max >= 2:
                max = 2
        else:
            max = 1.5

        psihsp = (self.h / self.hmin) ** (2 / 3)

        if psihsp >= max:
            psihsp = max
        elif psihsp <= 1:
            psihsp = 1
        return psihsp

    def calculation_NRkp_C1(self):
        if self.Recuperationproprietecheville.get_dowel_property(
                'Rupture par extraction glissement - NRk,p,seis (N) C1') == "non determinante":
            NRkpC1 = 0
        else:
            NRkpC1 = float(self.Recuperationproprietecheville.get_dowel_property('Rupture par extraction glissement - NRk,p,seis (N) C1'))
        return NRkpC1

    def calculation_N0Rksp_C1(self, hef1):
        NRkp = self.calculation_NRkp_C1()

        N0Rkc = self.calculation_n0rkc(hef1)
        if NRkp <= N0Rkc and NRkp != 0:
            calculation_N0Rksp_C1 = NRkp
        else:
            calculation_N0Rksp_C1 = N0Rkc
        return calculation_N0Rksp_C1

    def calculation_NRkp_C2(self):
        if self.Recuperationproprietecheville.get_dowel_property(
                'Rupture par extraction glissement - NRk,p,seis (N) C2') == "non determinante":
            NRkpC2 = 0
        else:
            NRkpC2 = float(self.Recuperationproprietecheville.get_dowel_property('Rupture par extraction glissement - NRk,p,seis (N) C2'))

        return NRkpC2

    def calculation_N0Rksp_C2(self, hef1):
        NRkp = self.calculation_NRkp_C2()
        N0Rkc = self.calculation_n0rkc(hef1)
        if NRkp <= N0Rkc and NRkp != 0:
            calculation_N0Rksp_C2 = NRkp
        else:
            calculation_N0Rksp_C2 = N0Rkc

        return calculation_N0Rksp_C2

    def calculation_number_edge(self, scrn):
        NbBord = 0
        ccrN = 0.5 * scrn
        if self.cx0 <= ccrN:
            NbBord = NbBord + 1

        if self.cx1 <= ccrN:
            NbBord = NbBord + 1

        if self.cz0 <= ccrN:
            NbBord = NbBord + 1

        if self.cz1 <= ccrN:
            NbBord = NbBord + 1

        return NbBord
