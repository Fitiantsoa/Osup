from PyQt5.QtCore import QObject

from src.constantes import DOWEL_DB
from src.utils import read_json

from src.modules.components import ListView, Combobox
from src.models.list_model import PlatineListModel, SofixListModel

#try

class ModulePlatineSofix:
    objectName= "modulePlatineSofix"

    def __init__(self,parent):
        self.sibling = parent.findChild(QObject, self.objectName)
        self.dowel_db = read_json(DOWEL_DB)

        self.platine_list_view = ListView("PlatineListViewSoFix", parent, PlatineListModel([]))
        self.criteria_list_view = ListView("ListViewSoFix", parent, SofixListModel([]))

        self.sibling.findChild(QObject, "GammeCheville").activated.connect(self.update_model)
        self.sibling.findChild(QObject, "ModeleCheville").activated.connect(self.update_model)
        self.sibling.findChild(QObject, "TypeCheville").activated.connect(self.update_model)

        self.init_cd_dowel()

        self.data = self.platine_list_view._model._data
        self.axis = []
        self.l = []
        self.h = []
        self.e = []
        self.b = []
        self.a = []
        self.orientation = []
        self.nbCheville = []

        # DOWEL PROPERTY
        self.dx0 = []
        self.dx1 = []
        self.dz0 = []
        self.dz1 = []
        self.gamme_dowel = []
        self.modele_dowel = []
        self.type_dowel = []
        self.deep_dowel = []
        self.norme = []
        self.type_charge = []
        self.situation_initiale = []
        self.cx0 = []
        self.cx1 = []
        self.cz0 = []
        self.cz1 = []
        self.state_concrete = []
        self.class_concrete = []
        self.thick_concrete = []
        self.armature_concrete = []
        self.edf = []
        self.Vx = []
        self.N = []
        self.Vz = []
        self.Mx = []
        self.T = []
        self.Mz = []
        self.calcul = []

    def test(self):
        pass


    def reinitialize_platine(self):
        self.orientation = []
        self.l = []
        self.h = []
        self.e = []
        self.b = []
        self.a = []
        self.nbCheville = []
        self.dx0 = []
        self.dx1 = []
        self.dz0 = []
        self.dz1 = []
        self.gamme_dowel = []
        self.modele_dowel = []
        self.type_dowel = []
        self.deep_dowel = []
        self.norme = []
        self.type_charge = []
        self.situation_initiale = []
        self.cx0 = []
        self.cx1 = []
        self.cz0 = []
        self.cz1 = []
        self.state_concrete = []
        self.class_concrete = []
        self.thick_concrete = []
        self.armature_concrete = []
        self.edf = []
        self.Vx = []
        self.N = []
        self.Vz = []
        self.Mx = []
        self.T = []
        self.Mz = []
        self.calcul = []

    def update_from_file(self, data_platine, data_cheville):
        self.platine_list_view.set_model_data([data_platine, data_cheville])

    def init_cd_dowel(self):
        self.set_model("GammeCheville", list(self.dowel_db.keys()))
        self.update_model()

    def update_model(self):
        self.current_text_model = self.sibling.findChild(QObject, "GammeCheville").property("currentText")
        self.set_model("ModeleCheville", list(self.dowel_db[self.current_text_model].keys()))
        self.current_text_type = self.sibling.findChild(QObject, "ModeleCheville").property("currentText")
        self.set_model("TypeCheville", list(self.dowel_db[self.current_text_model][self.current_text_type].keys()))
        current_text = self.sibling.findChild(QObject, "TypeCheville").property("currentText")
        self.set_model("ProfondeurCheville",
                       list(self.dowel_db[self.current_text_model][self.current_text_type][current_text].keys()))

    def set_model(self, objectName, value):
        self.sibling.findChild(QObject, objectName).setProperty("model", value)

    def get_dowel_data(self):
        self.get_list_value()
        return {
            'nbCheville': self.nbCheville,
            'Lx': self.l,
            'Lz': self.h,
            'tfix': self.e,
            'dx0': self.dx0,
            'dx1': self.dx1,
            'dz0': self.dz0,
            'dz1': self.dz1,
            'sx0': self.a,
            'sz0': self.b,
            'gamme': self.gamme_dowel,
            'modele': self.modele_dowel,
            'type': self.type_dowel,
            'hef': self.deep_dowel,
            'norme': self.norme,
            'TypeCharge': self.type_charge,
            'txt': self.situation_initiale,
            'cx0': self.cx0,
            'cx1': self.cx1,
            'cz0': self.cz0,
            'cz1': self.cz1,
            'etat': self.state_concrete,
            'typebeton': self.class_concrete,
            'h': self.thick_concrete,
            'armature': self.armature_concrete,
            'EDF': self.edf,
            'axis': self.axis,
            'Vx': self.Vx,
            'N': self.N,
            'Vz': self.Vz,
            'Mx': self.Mx,
            'T': self.T,
            'Mz': self.Mz,
            'calcul': self.calcul,
            'orientation': self.orientation
            }

    def get_list_value(self):
        self.reinitialize_platine()
        print("platine  data",self.data)
        for data in self.data:
            self.nbCheville.append(data['dowelsnb'])
            self.orientation.append(data['orientation'])
            self.l.append(float(data['l']))
            self.h.append(float(data['h']))
            self.e.append(float(data['e']))
            if data['b'] == "" or data['a'] == "":
                if data['b'] == "":
                    self.b.append(data['b'])
                    self.a.append(float(data['a']))
                elif data['a'] == "":
                    self.b.append(float(data['b']))
                    self.a.append(data['a'])
            self.gamme_dowel.append(data['gamme'])
            self.modele_dowel.append(data['modele'])
            self.type_dowel.append(data['type'])
            self.deep_dowel.append(float(data['hef']))
            self.norme.append(data['norme'])
            self.type_charge.append(data['TypeCharge'])
            self.situation_initiale.append(data['txt'])
            self.cx0.append(data['cx0'])
            self.cx1.append(data['cx1'])
            self.cz0.append(data['cz0'])
            self.cz1.append(data['cz1'])

            self.Vx.append(data['Vx'])
            self.N.append(data['N'])
            self.Vz.append(data['Vz'])
            self.Mx.append(data['Mx'])
            self.T.append(data['T'])
            self.Mz.append(data['Mz'])

            self.calcul.append(data['calcul'])

            if data['etat'] == "Fissuré":
                self.state_concrete.append("Fissure")
            else:
                self.state_concrete.append("Non fissure")
            self.class_concrete.append(data['typebeton'])
            self.thick_concrete.append(data['h'])
            self.armature_concrete.append(data['armature'])
            self.edf.append(data['EDF'])

            if float(data['dowelsnb']) == 4:
                self.dx0.append((float(data['l']) - float(data['a']))/2)
                self.dx1.append((float(data['l']) - float(data['a']))/2)
                self.dz0.append((float(data['h']) - float(data['b']))/2)
                self.dz1.append((float(data['h']) - float(data['b']))/2)
            elif float(data['dowelsnb']) == 2 and data['orientation'] == 'Horizontal':
                self.dx0.append((float(data['l']) - float(data['a'])) / 2)
                self.dx1.append((float(data['l']) - float(data['a'])) / 2)
                self.dz0.append((float(data['h'])) / 2)
                self.dz1.append((float(data['h'])) / 2)

            elif float(data['dowelsnb']) == 2 and data['orientation'] == 'Vertical':
                self.dx0.append(float(data['l']) / 2)
                self.dx1.append(float(data['l']) / 2)
                self.dz0.append((float(data['h']) - float(data['b'])) / 2)
                self.dz1.append((float(data['h']) - float(data['b'])) / 2)

    def new_file(self):
        self.platine_list_view.reset()

    def reset_result_sofix(self):
        self.criteria_list_view.reset()

    def get_data(self, critere):
        print("aaaa", critere)

        for i in range(len(critere)):
            dict = {}
            dict['Vx'] = critere[i][10]
            dict['N'] = critere[i][11]
            dict['Vz'] = critere[i][12]
            dict['Mx'] = critere[i][13]
            dict['T'] = critere[i][14]
            dict['Mz'] = critere[i][15]
            dict['ruptacier'] = critere[i][0]
            dict['ruptExtGliss'] = critere[i][1]
            dict['ruptConeBet'] = critere[i][2]
            dict['ruptFendBet'] = critere[i][3]
            dict['ruptAcierSansBrasLevier'] = critere[i][4]
            dict['ruptEffetLevier'] = critere[i][5]
            dict['ruptBordBet'] = critere[i][6]
            dict['ruptCombiAcier'] = critere[i][7]
            dict['ruptCombiBet'] = critere[i][8]
            self.criteria_list_view.set_model_data(dict)



