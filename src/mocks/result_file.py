from src.constantes import *
import glob

class ResultFile:

    def __init__(self, pipe_axis):
        self.axis = pipe_axis
        self.content = []
        self.input_data = []

    def load(self,part):
        self.content = []
        i = 0
        for path in glob.glob(TEMP + part + "*.Osup"):
            i += 1
            self.get_data(path, i)

    def get_data(self, path, j):
        with open(path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                data = line.split()
                if len(data) >= 3:
                    try:
                        self.content.append({"Fx": float(data[0]),
                                             "Fy": float(data[1]),
                                             "Fz": float(data[2]),
                                             "num_curv": str(j)})
                    except:
                        pass
        return True

    def get_plot_data(self):
        data = {}
        for elt in self.content:
            if elt["num_curv"] not in data.keys():
                data[elt["num_curv"]] = {"DataX": [], "DataY": []}
        for num in data.keys():
            for elt in self.content:
                if elt["num_curv"] == num:
                    if self.axis == "Z":
                        data[num]["DataX"].append(elt['Fx'])
                        data[num]["DataY"].append(elt['Fy'])
                    elif self.axis == "Y":
                        data[num]["DataX"].append(elt['Fx'])
                        data[num]["DataY"].append(elt['Fz'])
                    else:
                        data[num]["DataX"].append(elt['Fy'])
                        data[num]["DataY"].append(elt['Fz'])
        return data

    def get_dict_data(self, nbPoint, data):
        result = {}
        if nbPoint == '':
            nbPoint = 10
        try:
            name = list(data.keys())[0]
            pas_iter = int(len(data[name]['Courbe Minimale']['DataX']) / (2 * int(nbPoint)))
            result[name] = {"DataX": [], "DataY": []}
            i = 0
            while i < len(data[name]['Courbe Minimale']['DataX']):
                result[name]["DataX"].append(data[name]['Courbe Minimale']['DataX'][i])
                result[name]["DataY"].append(data[name]['Courbe Minimale']['DataY'][i])
                i += pas_iter
            result[name]["DataX"].append(data[name]['Courbe Minimale']['DataX'][-1])
            result[name]["DataY"].append(data[name]['Courbe Minimale']['DataY'][-1])
            return result
        except:
            print("Données étrier vide")


    def create_result_file(self, path):
        print('path', path)
        try:
            with open(path, "w") as f:
                f.write("\n".join(self.input_data))
                f.write("\n")
        except:
            pass


    def append_material(self, name, E, rho, G, Sy, Su, S):
        self.input_data.append("MAT\t" + name + "\t" + str(E) + "\t" + str(rho) + "\t" + str(G) + "\t" + str(Sy) + "\t" + str(Su) + "\t" + str(S))

    def append_section(self, name, A, IY ,IZ, AY, AZ, JX, Wely, Welz, Igr):
        self.input_data.append(
          "PROF\t" + name + "\t" + str(A) + "\t" + str(IY) + "\t" + str(IZ) + "\t" + str(AY) + "\t" + str(AZ) + "\t" + str(JX) + "\t" + str(Wely) + "\t" + str(Welz) + "\t" + str(Igr))

    def write_load(self, fx, fy, fz, niveau):
        self.input_data.append(
            "LOAD\t" + str(fx) + "\t" + str(fy) + "\t" + str(fz) + "\nNIVEAU\t" + niveau)

    # @staticmethod
    # def void_file():
    #     return os.path.getsize(CHEVILLE_RSLT.replace("'", ""))


