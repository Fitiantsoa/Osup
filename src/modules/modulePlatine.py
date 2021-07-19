from PyQt5.QtCore import QObject

from src.constantes import MATERIAL_DB, PROFILE_DB
from src.utils import read_json

from src.modules.components import ListView, Combobox
from src.models.list_model import PlatineListModel

class ModulePlatine:
    objectName= "modulePlatine"

    def __init__(self,parent):
        self.sibling = parent.findChild(QObject, self.objectName)
        self.material_db = read_json(MATERIAL_DB)
        self.profile_db = read_json(PROFILE_DB)

        self.platine_list_view = ListView("PlatineListView", parent, PlatineListModel([]))
        self.production_cb = Combobox("ProdPlatine", parent)
        self.material_cb = Combobox("MatPlatine", parent)
        self.node = Combobox("DowelNode", parent)

        self.sibling.findChild(QObject, "ProdPlatine").activated.connect(self.update_material)
        self.init_cb()

        self.data = self.platine_list_view._model._data
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
        self.section_database = read_json(PROFILE_DB)
        self.inertieY = []
        self.orientation = []
        self.nbCheville = []
        self.node_list = []

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
        self.inertieY = []
        self.orientation = []
        self.nbCheville = []
        self.prod = []
        self.mat = []
        self.t = []
        self.node_list = []

    def init_cb(self):
        self.set_model("ProdPlatine", list(self.material_db["RCC-M 2016"].keys()))
        self.update_material()

    def update_from_file(self, data):
        self.platine_list_view.set_model_data(data)


    def update_material(self):
        current_text = self.sibling.findChild(QObject, "ProdPlatine").property("currentText")
        self.set_model("MatPlatine", list(self.material_db["RCC-M 2016"][current_text].keys()))


    def set_model(self, objectName, value):
        self.sibling.findChild(QObject, objectName).setProperty("model", value)

    def get_data(self,geo_data):
        self.get_list_value(geo_data)
        return {
            'nbCheville': self.nbCheville,
            'axis':self.axis,
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
            'prod': self.prod,
            'mat':self.mat,
            't': self.t,
            'noeud':self.node_list
        }

    def get_list_value(self,geo_data):
        self.reinitialize_platine()
        node_plat_list = []
        print(self.data)
        for data in self.data:
            self.nbCheville.append(data['dowelsnb'])
            self.axis.append(data['axis'])
            print(self.axis)
            self.orientation.append(data['orientation'])
            self.l.append(float(data['l']))
            self.h.append(float(data['h']))
            self.e.append(float(float(data['e'])))
            self.b.append(float(data['b']))
            self.a.append(float(data['a']))
            self.prod.append(data['prod'])
            self.mat.append(data['mat'])
            self.node_list.append(data['noeud'])
            prod = data['prod']
            mat = data['mat']
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