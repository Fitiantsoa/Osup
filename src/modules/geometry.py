from PyQt5.QtCore import QObject

from src.constantes import MATERIAL_DB, PROFILE_DB
from src.utils import read_json
from src.modules.components import ListView, Combobox
from src.models.list_model import NodeListModel, BeamListModel

class Geometry:
    objectName = "moduleGeometry"

    def __init__(self, parent):
        self.sibling = parent.findChild(QObject, self.objectName)
        self.material_db = read_json(MATERIAL_DB)
        self.profile_db = read_json(PROFILE_DB)

        self.node_list_view = ListView("NodeListView", parent, NodeListModel([]))
        self.beam_list_view = ListView("BeamListView", parent, BeamListModel([]))
        self.production_cb = Combobox("ProductionCB", parent)
        self.material_cb = Combobox("MaterialCB", parent)
        self.section_cb = Combobox("SectionCB", parent)
        self.dimension_cb = Combobox("DimensionCB", parent)

        self.sibling.findChild(QObject, "ProductionCB").activated.connect(self.update_material)
        self.sibling.findChild(QObject, "SectionCB").activated.connect(self.update_profile)
        self.init_cb()

        self.beams = self.beam_list_view._model._data
        self.nodes = self.node_list_view._model._data
        self.node_rep_dict = {}
        self.node_orientation_dict = {}

    def update_from_file(self, data):
        self.node_list_view.set_model_data(data['node_init'])
        self.beam_list_view.set_model_data(data['beam_init'])

    def new_file(self):
        self.node_list_view.reset()
        self.beam_list_view.reset()

    def init_cb(self):
        self.set_model("ProductionCB", list(self.material_db["RCC-M 2016"].keys()))
        self.set_model("SectionCB", list(self.profile_db.keys()))
        self.update_material()
        self.update_profile()

    def update_material(self):
        current_text = self.sibling.findChild(QObject, "ProductionCB").property("currentText")
        self.set_model("MaterialCB", list(self.material_db["RCC-M 2016"][current_text].keys()))

    def update_profile(self):
        current_text = self.sibling.findChild(QObject, "SectionCB").property("currentText")
        self.set_model("DimensionCB", list(self.profile_db[current_text].keys()))

    def set_model(self, objectName, value):
        self.sibling.findChild(QObject, objectName).setProperty("model", value)

    def get_models(self):
        return {
            "node_init": self.nodes,
            "beam_init": self.beams,
            "nodes": self.get_node_list(),
            "node_group" : self.get_node_group(),
            "node_rep" : self.get_node_rep(),
            "beam_list": self.get_beam_list(),
            "beam_group": self.get_beam_group()
        }



    def __beam_group(self):
        beam_group = {}
        for (i, beam) in enumerate(self.beams):
            if beam['prod'] not in beam_group.keys():
                beam_group[beam['prod']+" "+beam['t']] = {}
        for beam in self.beams:
            for prod in beam_group.keys():
                if beam['prod'] == prod.split()[0]:
                    if beam['mat'] not in beam_group[prod].keys():
                        beam_group[prod][beam['mat']] = {}

        for beam in self.beams:
            for prod in beam_group.keys():
                for mat in beam_group[prod].keys():
                    if beam['mat'] == mat:
                        if beam['sec'] not in beam_group[prod][mat].keys():
                            beam_group[prod][mat][beam['sec']] = {}
        for beam in self.beams:
            for prod in beam_group.keys():
                for mat in beam_group[prod].keys():
                    for sect in beam_group[prod][mat].keys():
                        if beam['prod'] == prod.split()[0]:
                            if beam['mat'] == mat:
                                if beam['sec'] == sect:
                                    if str(beam['or']) not in beam_group[prod][mat][sect].keys():
                                        beam_group[prod][mat][sect][str(beam['or'])] = [beam['id']]
                                    else:
                                        beam_group[prod][mat][sect][str(beam['or'])].append(beam['id'])

        return beam_group

    def get_beam_group(self):
        gp_dict = self.__beam_group()
        print("gp_dict", gp_dict)
        i = 0
        group_list = []
        for prod in gp_dict.keys():
            for mat in gp_dict[prod].keys():
                for sect in gp_dict[prod][mat]:
                    for orientation in gp_dict[prod][mat][sect]:
                        i += 1
                        if mat != "RIGIDE":
                            id = "gp" + str(i)
                        else:
                            id = "rbe"
                        group_list.append({
                            'id' : id,
                            'production': prod.split()[0],
                            'material' : mat,
                            'temperature': prod.split()[1],
                            'section' : sect,
                            'orientation' : orientation,
                            'beam' : gp_dict[prod][mat][sect][orientation],


                        })
        return group_list

    def __node_rep(self):
        """
        Permet d'avoir un dictionnaire avec la liste des noeuds et leurs occurences
        """
        node_list_dict = {}
        for (i, beam) in enumerate(self.beams):
            if str(beam['n1']) not in node_list_dict.keys():
                node_list_dict[str(beam['n1'])] = 1
            else:
                node_list_dict[str(beam['n1'])] += 1
            if str(beam['n2']) not in node_list_dict.keys():
                node_list_dict[str(beam['n2'])] = 1
            else:
                node_list_dict[str(beam['n2'])] += 1

        return node_list_dict

    def get_node_rep(self):
        rep_dict = self.__node_rep()
        node_rep_dict = {}
        for i in sorted(rep_dict.keys()):
            if i == "1":
                node_rep_dict[i] = list(range(1, rep_dict[i] + 1))

            else:
                node_rep_dict[i] = list(range(node_rep_dict[str(int(i) - 1)][-1] + 1,node_rep_dict[str(int(i) - 1)][-1] + rep_dict[i] + 1))
        return node_rep_dict

    def get_node_list(self):
        node_list_dict = {}
        node_rep_dict = self.get_node_rep()
        for i in node_rep_dict.keys():
            for node_id in node_rep_dict[i]:
                try:
                    x = (self.nodes[int(i)]['cx']-self.nodes[int(i)-1]['cx'])
                    y = (self.nodes[int(i)]['cy'] - self.nodes[int(i) - 1]['cy'])
                    z = (self.nodes[int(i)]['cz']-self.nodes[int(i)-1]['cz'])
                    cl = (x**2 + y**2 + z**2)**0.5
                except:
                    cl = 200
                node_list_dict[str(node_id)] = {'id':str(node_id),'cx':self.nodes[int(i)-1]['cx'], 'cy': self.nodes[int(i)-1]['cy'], 'cz':self.nodes[int(i)-1]['cz'], 'cl': cl,'ap':self.nodes[int(i)-1]['ap']}
        return node_list_dict

    def get_beam_list(self):
        i = 0
        node_rep_dict = self.get_node_rep()
        beam_list = []
        for beam in self.beams:
            n1 = str(beam['n1'])
            n2 = str(beam['n2'])
            beam_list.append({'id':beam['id'],'n1': node_rep_dict[str(beam['n1'])][0],'n2':node_rep_dict[str(beam['n2'])][0],'mat':beam['mat'],'prod': beam['prod'],'sec':beam['sec'],'or':beam['or'],'t':beam['t']})

            del node_rep_dict[n1][0]
            del node_rep_dict[n2][0]
            i += 1
        return beam_list


    def get_node_group(self):
        node_group = {'encas':[]}
        nodes = self.get_node_list()
        for node in nodes.keys():
            if nodes[node]['ap'] == ("Encastrement") and node not in node_group['encas'] :
                node_group['encas'].append(node)
            elif nodes[node]['ap'] != ("Encastrement") and nodes[node]['ap'] != "Libre":
                boundary = nodes[node]['ap'].replace(" ","_")
                if boundary not in node_group.keys():
                    node_group[boundary] = [node]
                else:
                    node_group[boundary].append(node)
        return node_group

    def check_free_node(self):
        beam_node = []
        for beam in self.beams:
            if beam['n1'] not in beam_node:
                beam_node.append(beam['n1'])
            if beam['n2'] not in beam_node:
                beam_node.append(beam['n2'])
        for node in self.nodes:
            if node['id'] not in beam_node:
                return True

    def printImage(self, n1, n2,section,or_poutre):
        try:
            x = abs(float(self.nodes[n1 - 1]['cx']) - float(self.nodes[n2 - 1]['cx']))
            y = abs(float(self.nodes[n1 - 1]['cy']) - float(self.nodes[n2 - 1]['cy']))
            z = abs(float(self.nodes[n1 - 1]['cz']) - float(self.nodes[n2 - 1]['cz']))
            dimMax = max([x,y,z])
            if section[0] == "I" or section[0] == "H":
                sec_type = "I"
            else:
                sec_type = "U"

            if dimMax == x:
                orientation =  "X" + sec_type
            elif dimMax == y:
                orientation = "Y" + sec_type
            else:
                orientation = "Z" + sec_type
            self.node_orientation_dict[str(n1)] = orientation + str(or_poutre)
            self.node_orientation_dict[str(n2)] = orientation + str(or_poutre)
            return orientation
        except:
            return "None"



    def pipe_orientation(self):
        return self.node_orientation_dict

    def get_beam_thickness(self, idx, key):
        beam = list(filter(lambda x: x['id'] != idx, self.beam_list_view._model._data))[0]
        if beam['sec'] != "RIGIDE  ":
            sec, dim = beam['sec'].split()
            return self.profile_db[sec][dim][key]
