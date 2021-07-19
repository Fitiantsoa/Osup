from src.constantes import *

class ResultFile:

    def __init__(self, pipe_axis):
        self.axis = pipe_axis
        self.content = []

    def load(self, path, part):
        self.content = []
        if path is None:
            path = TEMP + part + '(2).Osup'
            # path = TEMP + '/profile.Osup'
        with open(path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                data = line.split()
                if len(data) >= 3:
                    try:
                        self.content.append({"Fx": float(data[0]),
                                             "Fy": float(data[1]),
                                             "Fz": float(data[2])})
                    except:
                        pass
        return True

    def get_plot_data(self):
        data = {"DataX": [], "DataY": []}
        for elt in self.content:
            if self.axis == "Z":
                data["DataX"].append(elt['Fx'])
                data["DataY"].append(elt['Fy'])
            elif self.axis == "Y":
                data["DataX"].append(elt['Fx'])
                data["DataY"].append(elt['Fz'])
            else:
                data["DataX"].append(elt['Fy'])
                data["DataY"].append(elt['Fz'])
        return data

    def get_dict_data(self, nbPoint, data):
        if nbPoint == '':
            nbPoint = 10
        try:
            name = list(data.keys())[0]
            pas_iter = int(len(data[name]['Courbe Minimale']['DataX']) / (2 * int(nbPoint)))
            result = {"DataX": [], "DataY": []}
            i = 0
            while i < len(data[name]['Courbe Minimale']['DataX']):
                result["DataX"].append(data[name]['Courbe Minimale']['DataX'][i])
                result["DataY"].append(data[name]['Courbe Minimale']['DataY'][i])
                i += pas_iter
            result["DataX"].append(data[name]['Courbe Minimale']['DataX'][-1])
            result["DataY"].append(data[name]['Courbe Minimale']['DataY'][-1])
            return result
        except:
            print("Données étrier vide")

