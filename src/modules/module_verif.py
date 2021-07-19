from PyQt5.QtCore import QObject
from src.modules.components import RadioButton, TextField, Combobox


class ModuleVerif:
    objectName = "moduleVerif"

    def __init__(self, parent):
        self.sibling = parent.findChild(QObject, self.objectName)

        self.module_ratio = RadioButton("ModuleRatio", self.sibling)
        self.module_courbe = RadioButton("ModuleCourbe", self.sibling)

        self.load_node = Combobox("NodeLoad", parent)
        self.friction_axis = Combobox("FrictionAxis", parent)

        self.fx = TextField("Fx", self.sibling)
        self.fy = TextField("Fy", self.sibling)
        self.fz = TextField("Fz", self.sibling)
        #self.friction_load = TextField("FrictionLoad", self.sibling)
        self.points = TextField("Points", self.sibling)

        # self.init_cb()


    def get_data(self):
        if self.module_courbe._checked:
            return {
                'methode': "courbe",
                'load_node' : self.load_node._currentText,
                #'friction_load': self.friction_load._text,
                'points': self.points._text,
                'axis': self.friction_axis._currentText
            }
        else:
            return {
                "methode": "ratio",
                'fx': self.fx._text,
                'fy': self.fy._text,
                'fz': self.fz._text,
                'load_node': self.load_node._currentText
            }

    def update_from_file(self, data):
        self.module_ratio.update_qml(data["methode"])

        if self.module_courbe._checked:
            #self.friction_load.update_qml(data["friction_load"])
            self.points.update_qml(data["points"])
            self.friction_axis.update_qml(data["axis"])
        else:
            try:
                self.fx.update_qml(data["Fx"])
                self.fy.update_qml(data["Fy"])
                self.fz.update_qml(data["Fz"])
            except:
                print("Pas de chargement rennseigné dans le fichier Osup")
        #self.load_node.update_qml(data["load_node"])




    def new_file(self):
        self.load_node.reset()
        self.fx.reset()
        self.fy.reset()
        self.fz.reset()
        self.points.reset()

