from math import pi
from PyQt5.QtCore import QObject
from src.utils import read_json
from src.constantes import STIRRUP_DB
from src.modules.components import ListView, Combobox
from src.models.list_model import StirrupListModel
from src.calculation.stirrup import CalculEtrier


class Stirrup:

    objectName = "moduleStirrup"

    def __init__(self, parent):
        self.sibling = parent.findChild(QObject, self.objectName)
        self.stirrup_db = read_json(STIRRUP_DB)
        self.bolt_type = Combobox("BoltCB", parent)
        self.stirrup_list_view = ListView("ListViewStirrup", parent, StirrupListModel([]))

        self.sibling.findChild(QObject, "BoltCB").activated.connect(self.update_characteristic)
        self.init_cb()

        self.plot_data = {}

    def get_data(self):
        return{
            "material":self.stirrup_list_view._model._data,
            "plot_data": self.plot_data
        }

    def get_plot_data(self,data):
        self.plot_data = data

    def update_from_file(self, data):
        self.stirrup_list_view.set_model_data(data['material'])
        self.get_plot_data(data['plot_data'])

    def new_file(self):
        self.stirrup_list_view.reset()
        self.update_characteristic()

    def init_cb(self):
        self.set_model("BoltCB", list(self.stirrup_db.keys()))
        self.update_characteristic()

    def set_model(self, objectName, value):
        self.sibling.findChild(QObject, objectName).setProperty("model", value)

    def update_characteristic(self):
        """ Updates mechanical characteristics according to type selection"""
        current_text = self.sibling.findChild(QObject, "BoltCB").property("currentText")
        characteristics = self.stirrup_db[current_text]
        characteristics["Sb"] = round((characteristics["d"] - 1.2268 * characteristics["pas"]) ** 2 * (pi / 4), 2)
        d = characteristics["d"]
        if d > 27:
            characteristics["do"] = d + 3
        elif d > 14:
            characteristics["do"] = d + 2
        else:
            characteristics["do"] = d + 1

        for key in ["As", "Sb", "d", "pas", "A", "dm", "do"]:
            self.sibling.findChild(QObject, "{}TF".format(key)).setProperty("text", characteristics[key])

    def append(self, norm, level, coeff, name, materiauxB, Sb, As, d, l, t, pas, Sy, fy, Su, fu, Fub, A, dm, do, tp, pCisaill, fraise, p1u, e1u, e2u):
        self._err = 0
        if norm != "rccm":
            error = self._win.findChild(QObject, "Erreur")
            self.getPince1(e1u, do, t, error)
            self.getPince2(e2u, do, t, error)
            self.getEntraxe1(p1u, do, t, error)
        if self._err == 0:
            cEtrier = CalculEtrier(name, materiauxB, Sb, As, d, l, t, pas, Sy, fy, Su, fu, Fub, A, dm, do, tp, pCisaill, fraise, p1u, e1u, e2u, norm, level, coeff)

            model = self.sibling.findChild(QObject, "ListViewStirrup").property("model")
            bolt = self.sibling.findChild(QObject, "BoltCB").property("currentText")
            if norm != "rccm":
                model.append(name, bolt, l, d, t, pas, Sb, As, dm, do, tp, A, fu, Fub, fy, Su, Sy, p1u, e1u,
                             e2u, cEtrier._Ft, cEtrier._Fv, cEtrier._Fp, cEtrier._FbRd, cEtrier._Bp, norm=norm)
            else:
                model.append(name, bolt, l, d, t, pas, Sb, As, dm, do, tp, A, fu, Fub, fy, Su, Sy, p1u, e1u,
                             e2u, cEtrier._Ft, cEtrier._Fv, cEtrier._Fp, norm=norm)
            return cEtrier

#EN
# //////////////////////////////////ENTRAXE////////////////////////////////////////////
    # Fonction de critère de l'entraxe 1 issue de l'équation
    def getEntraxe1(self, p1u, do, t, error):
        # Norme EN
        p1min = 2.2 * float(do)
        p1max = min(14 * float(t), 200)
        if p1min <= float(p1u) <= p1max:
            pass
        elif p1min > float(p1u):
            self._err = 1
            error.setProperty("text", "Attention la pince p1 est trop petite. "
                                      "Elle doit être comprise entre %d et %d"%(round(p1min,2), round(p1max,2)))
            error.open()
        elif float(p1u) > p1max:
            self._err = 1
            error.setProperty("text", "Attention la pince p1 est trop garnde. "
                                      "Elle doit être comprise entre %d et %d"%(round(p1min,2), round(p1max,2)))
            error.open()


#EN
# //////////////////////////////////PINCE////////////////////////////////////////////
    # Fonction de critère de la pince 1 issue de l'équation
    def getPince1(self, e1u, do, t, error):
        # Norme EN
        emin = (1.2 * float(do))
        emax = 4 * float(t) + 40
        if emin <= float(e1u) <= emax:
            pass
        elif emin > float(e1u):
            error.setProperty("text", "Attention l'entraxe e1 est trop petit. "
                                      "Il doit être compris entre %d et %d"%(round(emin,2), round(emax,2)))
            error.open()
            self._err = 1
        elif float(e1u) > emax:
            error.setProperty("text", "Attention l'entraxe e1 est trop grand. "
                                      "Il doit être compris entre %d et %d"%(round(emin,2), round(emax,2)))
            error.open()
            self._err = 1

    # Fonction de critère de la pince 2 issue de l'équation
    def getPince2(self, e2u, do, t, error):
        # Norme EN
        emin = 1.2 * float(do)
        emax = 4 * float(t) + 40
        if emin <= float(e2u) <= emax:
            pass
        elif emin > float(e2u):
            self._err = 1
            error.setProperty("text", "Attention l'entraxe e2 est trop petit. "
                                      "Il doit être compris entre %d et %d"%(round(emin,2), round(emax,2)))
            error.open()
        elif float(e2u) > emax:
            self._err = 1
            error.setProperty("text", "Attention l'entraxe e2 est trop grand. "
                                      "Il doit être compris entre %d et %d"%(round(emin,2), round(emax,2)))
            error.open()

