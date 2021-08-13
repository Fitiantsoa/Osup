from PyQt5.QtCore import QObject

from src.constantes import MATERIAL_DB, PROFILE_DB, DOWEL_DB
from src.utils import read_json

from src.modules.components import ListView, Combobox
from src.models.list_model import PlatineListModel


class ModulePlatine:
    objectName= "modulePlatine"

    def __init__(self,parent):
        self.sibling = parent.findChild(QObject, self.objectName)
        self.material_db = read_json(MATERIAL_DB)
        self.profile_db = read_json(PROFILE_DB)
        self.dowel_db = read_json(DOWEL_DB)

        self.platine_list_view = ListView("PlatineListView", parent, PlatineListModel([]))
        self.production_cb = Combobox("ProdPlatine", parent)
        self.material_cb = Combobox("MatPlatine", parent)
        self.node = Combobox("DowelNode", parent)

        self.sibling.findChild(QObject, "ProdPlatine").activated.connect(self.update_material)
        self.sibling.findChild(QObject, "GammeCheville").activated.connect(self.update_model)
        self.sibling.findChild(QObject, "ModeleCheville").activated.connect(self.update_model)
        self.sibling.findChild(QObject, "TypeCheville").activated.connect(self.update_model)

        self.init_cb()
        self.init_cd_dowel()

        self.data = self.platine_list_view._model._data
        self.axis = []
        self.l = []
        self.h = []
        self.e = []
        self.b = []
        self.a = []
        self.bprofile = []
        self.hprofile = []
        self.S = []
        self.Sy = []
        self.Su = []
        self.E = []
        self.section_database = read_json(PROFILE_DB)
        self.inertieY = []
        self.orientation = []
        self.nbCheville = []
        self.node_list = []

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
        self.calcul = []

    def reinitialize_platine(self):
        self.axis = []
        self.orientation = []
        self.l = []
        self.h = []
        self.e = []
        self.b = []
        self.a = []
        self.bprofile = []
        self.hprofile = []
        self.S = []
        self.Sy = []
        self.Su = []
        self.E = []
        self.inertieY = []
        self.nbCheville = []
        self.prod = []
        self.mat = []
        self.t = []
        self.node_list = []
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
        self.calcul = []

    def init_cb(self):
        self.set_model("ProdPlatine", list(self.material_db["RCC-M 2016"].keys()))
        self.update_material()

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

    def update_material(self):
        current_text = self.sibling.findChild(QObject, "ProdPlatine").property("currentText")
        self.set_model("MatPlatine", list(self.material_db["RCC-M 2016"][current_text].keys()))

    def set_model(self, objectName, value):
        self.sibling.findChild(QObject, objectName).setProperty("model", value)

    def get_data(self, geo_data):
        self.get_list_value(geo_data)
        return {
            'nbCheville': self.nbCheville,
            'axis': self.axis,
            'orientation': self.orientation,
            'l': self.l,
            'h': self.h,
            'e': self.e,
            'b': self.b,
            'a': self.a,
            'bprofile': self.bprofile,
            'hprofile': self.hprofile,
            'inertieY': self.inertieY,
            'S': self.S,
            'Sy':self.Sy,
            'Su': self.Su,
            'E': self.E,
            'prod': self.prod,
            'mat':self.mat,
            't': self.t,
            'noeud':self.node_list
        }

    def get_dowel_data(self):
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
            'calcul': self.calcul
            }

    def get_list_value(self, geo_data):
        self.reinitialize_platine()
        node_plat_list = []
        print("platine  data",self.data)
        for data in self.data:
            self.nbCheville.append(data['dowelsnb'])
            self.axis.append(data['axis'])
            self.orientation.append(data['orientation'])
            self.l.append(float(data['l']))
            self.h.append(float(data['h']))
            self.e.append(float(data['e']))
            self.b.append(float(data['b']))
            self.a.append(float(data['a']))
            self.prod.append(data['prod'])
            self.mat.append(data['mat'])
            self.node_list.append(data['noeud'])
            prod = data['prod']
            mat = data['mat']
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

            if float(data['t']) >= 20:
                t = str(float(data['t']))
            else:
                t = '20.0'
            self.t.append(t)
            #TODO: mettre message d'erreur qui vérifie les matériaux
            # self.S.append(self.material_db["RCC-M 2016"][prod][mat][t]['S'])
            # self.Sy.append(self.material_db["RCC-M 2016"][prod][mat][t]['Sy'])
            # self.Su.append(self.material_db["RCC-M 2016"][prod][mat][t]['Su'])
            node_plat_list.append(data['noeud'])
        beams = geo_data['beam_list']
        node_rep = geo_data['node_rep']
        node_id_list = []
        beam_id_list = []

        for node_plat in node_plat_list:
            for node in node_rep.keys():
                if str(node_plat) == node:
                    node_id_list.append(node_rep[node])

        for node_id in node_id_list:
            for node in node_id:
                for beam in beams:
                    if node == beam['n1'] or node == beam['n2']:
                        beam_id_list.append(beam['id'])
        print("beam_id_list",beam_id_list)
        for beam_id in beam_id_list:
            for data in beams:
                if data['id'] == beam_id:
                    print("section", data['sec'].split())
                    if data['sec'] != "RIGIDE  " and data['sec'].split()[0] != "REC":
                        sect = data['sec'].split()[0]
                        dim = str(int(data['sec'].split()[1]))
                        prod = data['prod']
                        mat = data['mat']
                        t = str(data['t'])
                        self.Su.append(self.material_db["RCC-M 2016"][prod][mat][t]['Su'])
                        self.Sy.append(self.material_db["RCC-M 2016"][prod][mat][t]['Sy'])
                        self.S.append(self.material_db["RCC-M 2016"][prod][mat][t]['S'])
                        self.E.append(self.material_db["RCC-M 2016"][prod][mat][t]['E'])
                        if data['or'] == 0.0:
                            self.inertieY.append("faible")
                            self.bprofile.append(float(self.profile_db[sect][dim]['b']))
                            self.hprofile.append(float(self.profile_db[sect][dim]['h']))
                        if data['or'] == 90.0:
                            self.inertieY.append("forte")
                            self.bprofile.append(float(self.profile_db[sect][dim]['b']))
                            self.hprofile.append(float(self.profile_db[sect][dim]['h']))
                    else:
                        self.inertieY.append("forte")
                        if data['sec']  == "RIGIDE  ":
                            self.bprofile.append(float(self.profile_db["RIGIDE"][" "]['b']))
                            self.hprofile.append(float(self.profile_db["RIGIDE"][" "]['h']))
                        else:
                            dim = data['sec'].split()[1]
                            self.bprofile.append(float(self.profile_db["REC"][dim]['b']))
                            self.hprofile.append(float(self.profile_db["REC"][dim]['h']))

    def new_file(self):
        self.platine_list_view.reset()