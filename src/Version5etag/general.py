from src.Version5etag.verifications import Verification
from src.Version5etag.geometries import Geometrie
from src.Version5etag.effortcalculation import CalculationEffort
from src.Version5etag.readinginputdata import ReadingInputData
from src.Version5etag.criteria import Criteria

''' Classe générale qui permet d'appeler toutes les fonctions de SoFix 
    Caractéristique géométrique
'''


class General:
    def __init__(self, data_dowel):
        self.data_dowel = data_dowel
        print("hello", data_dowel)
        self.data1 = 0
        self.readinputdata = 0
        self.resultTrac = 0
        self.dnom = 0
        self.resultShearing = 0
        self.inertia = 0
        self.geometrie = 0
        self.calculation_effort = 0
        self.scrn = []
        self.ccrN = []
        self.scrsp = []
        self.ccrsp = []
        self.hmin = []
        self.nd = []
        self.Ar = []
        self.fck = []
        self.k8 = []
        self.aeq_groupe = []
        self.aeq_isolee = []
        self.PosFix = []
        self.CentreGeo0 = []
        self.CentreGeo1 = []
        self.DistFixBord = []
        self.DistFixFix = []
        self.c = []
        self.s = []
        self.NbFixaBord = []
        self.list_dnom = []
        self.dowelname = []
        self.axis = data_dowel.get('axis')
        self.result_sofix = []

        self.run()

    def run(self):
        """
        Permet de lancer Osup / Sofix
        """
        calcul = self.data_dowel.get("calcul")[0]
        #print(calcul)
        if calcul == "Sofix":
            for i in range(len(self.data_dowel['Lx'])):
                data_dowel_general = self.input_data_general(i)
                self.dowel_name = data_dowel_general.get('dowelname')
                self.data = ReadingInputData(data_dowel_general)
                self.dnom = float(self.data.get_dowel_property('Diametre de percage dnom=d0 (mm)'))
                self.readinputdata = self.data.read_input_data()
                self.get_data_geo(self.dnom, self.readinputdata, self.geo_calculation(i), self.dowel_name)
                if self.check_data(i) is True:
                    geo = self.input_data_aster()
                    #self.effort_calculation(geo, i)
                    Criteria(geo, i)
                    self.result_sofix.append(Criteria(geo, i).calculation_criteria_traction_shearing())
                else:
                    return False

        elif calcul == "Osup":
            for i in range(len(self.data_dowel['Lx'])):
                data_dowel_general = self.input_data_general(i)
                self.dowel_name = data_dowel_general.get('dowelname')
                self.data = ReadingInputData(data_dowel_general)
                self.dnom = float(self.data.get_dowel_property('Diametre de percage dnom=d0 (mm)'))
                self.readinputdata = self.data.read_input_data()
                self.get_data_geo(self.dnom, self.readinputdata, self.geo_calculation(i), self.dowel_name)
                self.check_data(i)
                # if self.check_data(i) is True:
                #     pass
                # else:
                #     return False

    def critere_sofix(self):
        return self.result_sofix

    def input_data_aster(self):
        return {"dnom": self.list_dnom,
                "datadowel": self.data_dowel,
                "scrn": self.scrn,
                "ccrN": self.ccrN,
                "scrsp": self.scrsp,
                "ccrsp": self.ccrsp,
                "hmin": self.hmin,
                "nd": self.nd,
                "Ar": self.Ar,
                "fck": self.fck,
                "k8": self.k8,
                "aeq_groupe": self.aeq_groupe,
                "aeq_isolee": self.aeq_isolee,
                "PosFix": self.PosFix,
                "CentreGeo0": self.CentreGeo0,
                "CentreGeo1": self.CentreGeo1,
                "DistFixBord": self.DistFixBord,
                "DistFixFix": self.DistFixFix,
                "c": self.c,
                "s": self.s,
                "NbFixaBord": self.NbFixaBord,
                "modele": self.dowelname,
                "axis": self.axis
                }

    def get_data_geo(self, val1, list1, list2, dowelname):
        self.scrn.append(list1['scrn'])
        self.ccrN.append(list1['ccrN'])
        self.scrsp.append(list1['scrsp'])
        self.ccrsp.append(list1['ccrsp'])
        self.hmin.append(list1['hmin'])
        self.nd.append(list1['nd'])
        self.Ar.append(list1['Ar'])
        self.fck.append(list1['fck'])
        self.k8.append(list1['k8'])
        self.aeq_groupe.append(list1['aeq_groupe'])
        self.aeq_isolee.append(list1['aeq_isolee'])

        self.list_dnom.append(val1)

        self.PosFix.append(list2['PosFix'])
        self.CentreGeo0.append(list2['CentreGeo0'])
        self.CentreGeo1.append(list2['CentreGeo1'])
        self.DistFixBord.append(list2['DistFixBord'])
        self.DistFixFix.append(list2['DistFixFix'])
        self.c.append(list2['c'])
        self.s.append(list2['s'])
        self.NbFixaBord.append(list2['NbFixaBord'])
        self.dowelname.append(dowelname)

    def input_data_general(self, i):
        try:
            Vx = self.data_dowel['Vx'][i]
            N = self.data_dowel['N'][i]
            Vz = self.data_dowel['Vz'][i]
            Mx = self.data_dowel['Mx'][i]
            T = self.data_dowel['T'][i]
            Mz = self.data_dowel['Mz'][i]

        except:
            Vx = None
            N = None
            Vz = None
            Mx = None
            T = None
            Mz = None

        try:
            orientation = self.data_dowel['orientation'][i]

        except:
            orientation = None

        return {'nbCheville': int(self.data_dowel['nbCheville'][i]),
                'Lx': self.data_dowel['Lx'][i],
                'Lz': self.data_dowel['Lz'][i],
                'tfix': self.data_dowel['tfix'][i],
                'dx0': self.data_dowel['dx0'][i],
                'dx1': self.data_dowel['dx1'][i],
                'dz0': self.data_dowel['dz0'][i],
                'dz1': self.data_dowel['dz1'][i],
                'sx0': self.data_dowel['sx0'][i],
                'sz0': self.data_dowel['sz0'][i],
                'gamme': self.data_dowel['gamme'][i],
                'modele': self.data_dowel['modele'][i],
                'type': self.data_dowel['type'][i],
                'hef': self.data_dowel['hef'][i],
                'norme': self.data_dowel['norme'][i],
                'TypeCharge': self.data_dowel['TypeCharge'][i],
                'txt': self.data_dowel['txt'][i],
                'cx0': self.data_dowel['cx0'][i],
                'cx1': self.data_dowel['cx1'][i],
                'cz0': self.data_dowel['cz0'][i],
                'cz1': self.data_dowel['cz1'][i],
                'etat': self.data_dowel['etat'][i],
                'typebeton': self.data_dowel['typebeton'][i],
                'h': self.data_dowel['h'][i],
                'armature': self.data_dowel['armature'][i],
                'orientation': orientation,
                'EDF': self.data_dowel['EDF'][i],
                'dowelname': "{} {} {}".format(self.data_dowel["gamme"][i], self.data_dowel["modele"][i],
                                            self.data_dowel["type"][i]),
                'Vx': Vx,
                'N': N,
                'Vz': Vz,
                'Mx': Mx,
                'T': T,
                'Mz': Mz,
                }

    def geo_calculation(self, i):
        self.geometrie = Geometrie(self.dnom, self.readinputdata, self.input_data_general(i))
        self.inertia = self.geometrie.inertia()
        return self.inertia

    def check_data(self, i):
        self.data1 = self.data.get_dowel_full_property()
        check = Verification(self.inertia, self.data1, self.readinputdata, self.input_data_general(i))
        return check.verification_anchors()

