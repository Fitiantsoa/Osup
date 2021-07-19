from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton
import sys
from src.constantes import *

class TableView(QTableWidget):
    def __init__(self, comp):
        self.data = self.getData(comp)
        nb_point = len(self.data["Fx"])
        QTableWidget.__init__(self, nb_point,3)
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def getData(self, comp):
        return self.load(comp)

    def load(self, part):
        content = [[],[],[]]

        path = TEMP + part + '(2).Osup'
        with open(path, 'r') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                data = line.split()
                if len(data) >= 3:
                    try:
                        content[0].append(str(float(data[0])))
                        content[1].append(str(float(data[1])))
                        content[2].append(str(float(data[2])))
                    except:
                        pass
        return {
            "Fx": content[0],
            "Fy": content[1],
            "Fz": content[2]
        }

    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(horHeaders)

