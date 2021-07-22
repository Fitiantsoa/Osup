from verifications import Verification
from geometries import Geometrie
from effortcalculation import CalculationEffort
from readinginputdata import ReadingInputData
from criteria import Criteria

TypeCharge = "Statique ou quasi-statique"  # Sismique C2
NbFixa = 4  # Depend du choix de l'utilisateur
norme = "ETAG"
EDF = "Oui"
txt = "Situations permanentes et transitoires"  # Situations accidentelles

dowel_property = {"gamme": "HILTI",
                  "modele": "HDA-T",
                  "type": "M16/60",
                  "deep_dowel": "190.0"
                  }

modele = "{} {} {}".format(dowel_property.get("gamme"), dowel_property.get("modele"), dowel_property.get("type"))
hef = 190

data_concrete = {"etat": "Fissuré",
                 "armature": "Non",
                 "h": 500,
                 "typebeton": "C20/25"
                 }


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
                    "cz1": 1000000000000000, # 1000000000000000
                    "tfix": 15}

effort = {"N": -10000,
          "Mx": 500000,
          "Mz": 420000,
          "Vx": -120,
          "Vz": -120,
          "T": 333000
          }


class General:
    def __init__(self):
        self.data = ReadingInputData(norme, dowel_property, data_board_dowel, data_concrete)
        self.dnom = float(self.data.get_dowel_property('Diametre de percage dnom=d0 (mm)'))
        self.readinputdata = self.data.read_input_data()
        self.resultTrac = 0
        self.resultShearing = 0
        self.inertia = 0
        self.geometrie = 0
        self.calculation_effort = 0

    def run(self):
        self.geo_calculation()
        self.check_data()
        self.inputdataaster = self.input_data_aster()
        self.effort_calculation()
        self.criteria_calculation()

    def input_data_aster(self):
        return {"dowel_property": dowel_property,
                "data_concrete": data_concrete,
                "effort": effort,
                "data_board_dowel": data_board_dowel,
                "data": self.data,
                "inertia": self.inertia,
                "inputdata": self.readinputdata,
                "hef": hef,
                "TypeCharge": TypeCharge,
                "NbFixa": NbFixa,
                "norme": norme,
                "EDF": EDF,
                "txt": txt,
                "dnom": self.dnom
                }

    def geo_calculation(self):
        self.geometrie = Geometrie(NbFixa, data_board_dowel, effort, self.dnom, self.readinputdata, hef)
        self.inertia = self.geometrie.inertia()

    def check_data(self):
        self.data = self.data.get_dowel_full_property()
        Verification(NbFixa, self.inertia, self.data, self.readinputdata, data_board_dowel, data_concrete)

    def effort_calculation(self):
        self.calculation_effort = CalculationEffort(self.inputdataaster)
        self.resultTrac = self.calculation_effort.traction()
        self.resultShearing = self.calculation_effort.shearing()

    def criteria_calculation(self):
        Criteria(self.inputdataaster, self.resultTrac, self.resultShearing)
