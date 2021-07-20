from verifications import Verification
from geometries import Geometrie
from effortcalculation import CalculationEffort
from readinginputdata import ReadingInputData
from criteria import Criteria

modele = "HILTI HDA-T M16/60"
TypeCharge = "Statique ou quasi-statique"  # Sismique C2
NbFixa = 4  # Depend du choix de l'utilisateur
norme = "ETAG"
EDF = "Oui"
txt = "Situations permanentes et transitoires"  # Situations accidentelles

hef = 190
tfix = 15

etat = "Fissuré"  # Données Béton saisie par l'utilisateur
armature = "Non"  # Données Béton saisie par l'utilisateur
h = 500  # Données Béton saisie par l'utilisateur epaisseur
typebeton = "C20/25"

data_board_dowel = {"Lx": 400,
                    "Lz": 300,
                    "dx0": 50,
                    "dx1": 50,
                    "dz0": 50,
                    "dz1": 50,
                    "sx0": 300,
                    "sx1": 0,
                    "sz0": 200,
                    "sz1": 0,
                    "cx0": 1000000000000000,
                    "cx1": 1000000000000000,
                    "cz0": 150,
                    "cz1": 1000000000000000}  # 1000000000000000

effort = {"N": -10000,
          "Mx": 500000,
          "Mz": 420000,
          "Vx": -120,
          "Vz": -120,
          "T": 333000
          }


class General:
    def __init__(self):
        self.data = ReadingInputData(hef, tfix, modele, typebeton, norme)
        self.dnom = self.data.get_dowel_property('diametre percage')
        self.readinputdata = self.data.read_input_data()
        self.resultTrac = 0
        self.resultShearing = 0
        self.inertia = 0
        self.geometrie = 0
        self.calculation_effort = 0

    def run(self):
        self.geo_calculation()
        self.check_data()
        self.effort_calculation()
        self.criteria_calculation()

    def geo_calculation(self):
        self.geometrie = Geometrie(NbFixa, data_board_dowel, effort, self.dnom, self.readinputdata, hef)
        self.inertia = self.geometrie.inertia()

    def check_data(self):
        data = self.data.get_dowel_full_property()
        Verification(h, NbFixa, self.inertia, data, tfix, self.readinputdata, data_board_dowel)

    def effort_calculation(self):
        self.calculation_effort = CalculationEffort(NbFixa, self.geometrie, data_board_dowel, effort,
                                                    self.readinputdata,
                                                    self.inertia)
        self.resultTrac = self.calculation_effort.traction()
        self.resultShearing = self.calculation_effort.shearing()

    def criteria_calculation(self):
        Criteria(NbFixa, TypeCharge, effort, modele, hef, tfix, h, etat, armature, typebeton, self.geometrie,
                 self.resultShearing, self.resultTrac, data_board_dowel, self.inertia, self.readinputdata, EDF, txt, norme)
