from PyQt5.QtCore import QObject
from src.modules.components import RadioButton, TextField


class CalculationCondition:
    objectName = "moduleCalculationCondition"

    def __init__(self, parent):
        self.sibling = parent.findChild(QObject, self.objectName)

        self.norm_rccm_rb = RadioButton("RccmRB", self.sibling)
        self.norm_en_rb = RadioButton("EnRB", self.sibling)

        self.niv_oab_rb = RadioButton("NivOABRB", self.sibling)
        self.niv_c_rb = RadioButton("NivCRB", self.sibling)
        self.niv_d_rb = RadioButton("NivDRB", self.sibling)

        self.niv_normal_rb = RadioButton("NivNormalRB", self.sibling)
        self.niv_occ_rb = RadioButton("NivOccRB", self.sibling)

        self.calculation_temperature = TextField("CalculationTemperatureTF", self.sibling)
        self.friction_coefficient = TextField("FrictionCoefficientTF", self.sibling)
        self.ratioProf = TextField("RatioMaxProf", self.sibling)
        self.ratioPlat = TextField("RatioMaxPlat", self.sibling)
        self.portee = TextField("Portee", self.sibling)



    def update_from_file(self, data):
        self.norm_rccm_rb.update_qml(data["norm"])
        # self.norm_en_rb.update_qml(data["norm"] != "en")

        self.niv_oab_rb.update_qml(data["level"] == "oab")
        self.niv_c_rb.update_qml(data["level"] == "c")
        self.niv_d_rb.update_qml(data["level"] == "d")
        self.niv_normal_rb.update_qml(data["level"] == "normal")
        self.niv_occ_rb.update_qml(data["level"] == "occasionelle")

        self.calculation_temperature.update_qml(data['temperature'])
        self.friction_coefficient.update_qml(data['friction_coefficient'])
        self.ratioProf.update_qml(data['ratio_profile'])
        self.ratioPlat.update_qml(data['ratio_platine'])
        self.portee.update_qml(data['portee'])



    def get_data(self):
        return {
            "norm": self.get_norm(),
            "level": self.get_level(),
            "temperature": self.calculation_temperature._text,
            "friction_coefficient": self.friction_coefficient._text,
            "ratio_profile": self.ratioProf._text,
            "ratio_platine": self.ratioPlat._text,
            "portee": self.portee._text
        }


    def get_norm(self):
        if self.norm_rccm_rb._checked:
            return "rccm"
        else:
            return "en"

    def get_level(self):
        if self.norm_rccm_rb._checked:
            if self.niv_oab_rb._checked:
                return 'oab'
            elif self.niv_c_rb._checked:
                return 'c'
            else:
                return 'd'
        else:
            if self.niv_normal_rb:
                return 'normal'
            else:
                return 'occasionelle'

    def new_file(self):
        self.calculation_temperature.reset()
        self.friction_coefficient.reset()
        self.ratioProf.reset()
        self.ratioPlat.reset()
