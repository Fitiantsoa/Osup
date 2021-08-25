class Data:

    def __init__(self):
        self.torsors = []
        self.plots = {}
        # Plots data architecture :
        # {
        #      "component" : {
        #           "solicitation" : {
        #               dataX : [x1, x2, ...],
        #               dataY : [y1, y2, ...],
        #           }
        #       }
        # }

    def get_torsors(self):
        return self.plots

    def add_torsor(self, fy, fz, name):
        self.torsors.append([name, float(fy), float(fz)])

    def remove_torsor(self, name):
        idx = self.get_torsor_position(name)
        if idx is not None:
            del self.torsors[idx]
            return True
        return False

    def torsor_exist(self, name):
        return self.get_torsor_position(name) is not None

    def get_torsor_position(self, name):
        for i, torsor in enumerate(self.torsors):
            if torsor[0] == name:
                return i
        return None

    def get_plots(self):
        return self.plots

    def get_component_plots(self, component):
        if component in list(self.plots.keys()):
            return self.plots[component]
        return None

    def get_plot(self, component, solicitation):
        if component in list(self.plots.keys()):
            if solicitation in list(self.plots[component].keys()):
                return self.plots[component][solicitation]
        return None

    def load_plots(self, data, part):
        self.plots[part] = {}
        curv_list = list(data.keys())
        if len(curv_list) > 1:
            for key in data.keys():
                self.plots[part][key] = data[key]
        else:
            self.plots[part]["all"] = data[curv_list[0]]

    def add_plot(self, data, key):
        self.plots[key] = data
