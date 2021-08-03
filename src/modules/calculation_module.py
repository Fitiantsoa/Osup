from src.constantes import *
from src.utils import sort_beam_by, read_json


class Calculation_var():

    def __init__(self,prop_data, plat_data, dowel_data):
        self.material_database = read_json(MATERIAL_DB)
        self.section_database = read_json(PROFILE_DB)
        self.beams = prop_data['beam_list']
        self.node = prop_data['nodes']
        self.platine_data = plat_data
        self.dowel_data = dowel_data


    def get_material_val(self):
        E = []
        Sy = []
        Su = []

        for beam in self.beams:
            for i in range(2):
                if beam['prod'] != "RIGIDE":
                    E.append(float(self.material_database['RCC-M 2016'][beam['prod']][beam['mat']][beam['t']]['E'])*10**3)
                    Sy.append(float(self.material_database['RCC-M 2016'][beam['prod']][beam['mat']][beam['t']]['Sy']))
                    Su.append(float(self.material_database['RCC-M 2016'][beam['prod']][beam['mat']][beam['t']]['Su']))
                else:
                    E.append(float(self.material_database['RCC-M 2016'][beam['prod']][beam['mat']]['20.0']['E']) * 10 ** 3)
                    Sy.append(float(self.material_database['RCC-M 2016'][beam['prod']][beam['mat']]['20.0']['Sy']))
                    Su.append(float(self.material_database['RCC-M 2016'][beam['prod']][beam['mat']]['20.0']['Su']))
        return {
            'E': E,
            'Su': Su,
            'Sy': Sy
        }

    def get_section_val(self):
        A = []
        Iy = []
        Iz = []
        for beam in self.beams:
            if beam['sec'] != "RIGIDE  ":
                section = beam['sec'].split()[0]
                dim = beam['sec'].split()[1]
            else:
                section = 'RIGIDE'
                dim = " "
            for i in range(2):
                if beam['or'] == 0.0:
                    A.append(float(self.section_database[section][str(dim)]['aire']))
                    Iy.append(float(self.section_database[section][str(dim)]['iy']) * 10**4)
                    Iz.append(float(self.section_database[section][str(dim)]['iz']) * 10**4)
                elif beam['or'] == 90.0:
                    A.append(float(self.section_database[section][str(dim)]['aire']))
                    Iy.append(float(self.section_database[section][str(dim)]['iz']) * 10 ** 4)
                    Iz.append(float(self.section_database[section][str(dim)]['iy']) * 10 ** 4)
        return {
            'A': A,
            'Iy': Iy,
            'Iz': Iz,
            'lf': self.get_bucking_length()
        }

    def get_bucking_length(self):
        lf = []
        for beam in self.beams:
            for i in range(2):
                x = float(self.node[str(beam['n1'])]['cx']) - float(self.node[str(beam['n2'])]['cx'])
                y = float(self.node[str(beam['n1'])]['cy']) - float(self.node[str(beam['n2'])]['cy'])
                z = float(self.node[str(beam['n1'])]['cz']) - float(self.node[str(beam['n2'])]['cz'])
                lf.append((x**2+y**2+z**2)**0.5)
        return lf

    def get_value(self):
        return{
            'profile':{'beam':self.beams,'mat': self.get_material_val(), 'sec': self.get_section_val()},
            'platine': self.platine_data,
            "chevilles": self.dowel_data
        }
