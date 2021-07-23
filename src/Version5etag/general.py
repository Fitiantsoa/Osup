from src.Version5etag.verifications import Verification
from src.Version5etag.geometries import Geometrie
from src.Version5etag.effortcalculation import CalculationEffort
from src.Version5etag.readinginputdata import ReadingInputData
from src.Version5etag.criteria import Criteria


effort = {"N": -10000,
          "Mx": 500000,
          "Mz": 420000,
          "Vx": -120,
          "Vz": -120,
          "T": 333000
          }


class General:
    def __init__(self, data_dowel):
        self.data_dowel = data_dowel
        self.data = ReadingInputData(self.data_dowel)
        self.dnom = float(self.data.get_dowel_property('Diametre de percage dnom=d0 (mm)'))
        self.readinputdata = self.data.read_input_data()
        self.resultTrac = 0
        self.resultShearing = 0
        self.inertia = 0
        self.geometrie = 0
        self.calculation_effort = 0
        self.run()

    def run(self):
        self.geo_calculation()
        self.check_data()
        #self.inputdataaster = self.input_data_aster()
        #self.effort_calculation()
        #self.criteria_calculation()

    def input_data_aster(self):
        return {"effort": effort,
                "data": self.data,
                "inertia": self.inertia,
                "inputdata": self.readinputdata,
                "dnom": self.dnom,
                "doweldata": self.data_dowel,
                "modele": "{} {} {}".format(self.data_dowel.get("gamme"), self.data_dowel.get("modele"),
                                           self.data_dowel.get("type"))
                }

    def geo_calculation(self):
        self.geometrie = Geometrie(effort, self.dnom, self.readinputdata, self.data_dowel)
        self.inertia = self.geometrie.inertia()

    def check_data(self):
        self.data = self.data.get_dowel_full_property()
        Verification(self.inertia, self.data, self.readinputdata, self.data_dowel)

    def effort_calculation(self):
        self.calculation_effort = CalculationEffort(self.inputdataaster)
        self.resultTrac = self.calculation_effort.traction()
        self.resultShearing = self.calculation_effort.shearing()

    def criteria_calculation(self):
        Criteria(self.inputdataaster, self.resultTrac, self.resultShearing)
