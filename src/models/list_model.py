import sys
import json
import os
# import win32com.client as win32
from PyQt5.QtCore import pyqtSlot, pyqtProperty, pyqtSignal, QAbstractListModel, QModelIndex, Qt
from PyQt5.QtGui import QColor
from src.constantes import SETTINGS_PATH


class ListModel(QAbstractListModel):
    def __init__(self, data, parent=None, *args):
        QAbstractListModel.__init__(self, parent, *args)
        self._data = []
        self._roles = None
        self._roles_name_to_int = None
        self.titles = []

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def data(self, index, role):
        if not index.isValid():
            return None
        return self._data[index.row()][self._roles[role].decode('utf-8')]

    def setData(self, index, value, role):
        if not index.isValid():
            return False

        self._data[index.row()] = value
        if value:
            if self._roles is None:
                self._roles = dict(zip(range(Qt.UserRole + 1, Qt.UserRole + 1 + len(value)),
                                       [v.encode('utf-8') for v in value.keys()]))
                self._roles_name_to_int = {v: k for k, v in self._roles.items()}
            self.dataChanged.emit(index, index, self._roles.keys())
        return True

    def insertRows(self, row, count, parent=None):
        super(QAbstractListModel, self).beginInsertRows(QModelIndex(), row, row + count - 1)
        for i in range(count):
            self._data.insert(row + i, None)
        super(QAbstractListModel, self).endInsertRows()
        self.countChanged.emit()
        return True

    def removeRows(self, row, count, parent=None):
        super(QAbstractListModel, self).beginRemoveRows(QModelIndex(), row, row + count - 1)
        for i in range(count):
            del self._data[row]
        super(QAbstractListModel, self).endRemoveRows()
        return True

    def flags(self, index):
        return Qt.ItemIsEditable | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def roleNames(self):
        return self._roles

    countChanged = pyqtSignal()

    @pyqtProperty(int, notify=countChanged)
    def count(self):
        return self.rowCount()

    @pyqtSlot(int, str, result=bool)
    def insert(self, row, value):
        index = self.createIndex(row, 0)
        return self.insertRows(row, 1) and self.setData(index, value, Qt.EditRole)

    @pyqtSlot(int, result=bool)
    def remove(self, index):
        if index == -1:
            index = 0
        super(QAbstractListModel, self).beginRemoveRows(QModelIndex(), index, index)
        del self._data[index]
        super(QAbstractListModel, self).endRemoveRows()
        self.countChanged.emit()
        return True

    @pyqtSlot(int, str, result=str)
    def get(self, index, role_name):
        return str(self._data[index][role_name])

    @pyqtSlot(int, str, QColor)
    @pyqtSlot(int, str, str)
    @pyqtSlot(int, str, int)
    @pyqtSlot(int, str, float)
    def setProperty(self, index, role_name, value):
        try:
            append = False
            if index == len(self._data):
                self._data.append({})
                append = True

            self._data[index][role_name] = value

            if not append:
                self.dataChanged.emit(self.index(int(index)), self.index(int(index)),
                                      [self._roles_name_to_int[role_name.encode('utf-8')]])
            else:
                self.rowsInserted.emit(QModelIndex(), index, index)
        except:
            import sys
            print("ERREUR : Les données n'ont pas été mises à jour", file=sys.stderr)
            print(sys.exc_info())

    def FileScan(self, path):
        dictCase = []
        with open(path) as f:  # ouverture du fichier
            lines = f.readlines()
            for line in lines:
                if "     LOADING CASE NO." in line:
                    ligneTitre = line.lstrip("     LOADING CASE NO.")
                    num_cas = ligneTitre.split(" ")
                    num_cas = list(filter(('').__ne__, num_cas))
                    num_cas = num_cas[0]
                    dictCase.append(int(num_cas))
        return dictCase

    @pyqtSlot()
    def resultExport(self, data=None, MeP=False):
        # print("Exportation des données ( " + data + ") du module vers Excel")
        column = len(self.titles)
        if data == None:
            data = self._data
        # try:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        # except:
        #     return

        wb = excel.Workbooks.Add()
        ws = wb.Worksheets(1)
        for title in self.titles:
            index = 0
            ws.Cells(2, self.titles.index(title) + 2).Value = title
            while index < len(data):
                pos = self.titles.index(title) + 2
                ws.Cells(index + 3, pos).Value = data[index][title]
                ws.Cells(index + 3, pos).Borders.Weight = 2
                ws.Cells(index + 3, pos).HorizontalAlignment = 2
                ws.Cells(index + 3, pos).VerticalAlignment = 2
                index += 1
            # Mise en page Titre
            ws.Range(ws.Cells(2, 2), ws.Cells(2, column + 1)).Interior.Color = 0xE09E00
            ws.Range(ws.Cells(2, 2), ws.Cells(2, column + 1)).Font.Bold = True
            ws.Range(ws.Cells(2, 2), ws.Cells(2, column + 1)).Font.Color = -460552
            ws.Range(ws.Cells(2, 2), ws.Cells(2, column + 1)).Borders.Weight = 3
            # Mise en page Colonne
            ws.Range(ws.Cells(2, 2), ws.Cells(len(data) + 2, 2)).Interior.Color = 0xE09E00
            ws.Range(ws.Cells(2, 2), ws.Cells(len(data) + 2, 2)).Font.Bold = True
            ws.Range(ws.Cells(2, 2), ws.Cells(len(data) + 2, 2)).Font.Color = -460552
            ws.Range(ws.Cells(2, 2), ws.Cells(len(data) + 2, 2)).Borders.Weight = 3

        if MeP == True:
            for i in range(0,len(data),2):
                ws.Range(ws.Cells(i+3,2),ws.Cells(i+4,2)).Merge()
                ws.Range(ws.Cells(i + 3, 3), ws.Cells(i + 4, 3)).Merge()

        excel.Visible = True
        return ws

    def exportValue(self, text, ligne, col, ws, bool):
        ws.Cells(ligne, col).Value = text
        ws.Cells(ligne, col).Borders.Weight = 2
        ws.Cells(ligne, col).HorizontalAlignment = 2
        ws.Cells(ligne, col).VerticalAlignment = 2
        if bool:
            ws.Range(ws.Cells(ligne, col), ws.Cells(ligne, col)).Interior.Color = 0xE09E00
            ws.Range(ws.Cells(ligne, col), ws.Cells(ligne, col)).Font.Bold = True
            ws.Range(ws.Cells(ligne, col), ws.Cells(ligne, col)).Font.Color = -460552
            ws.Range(ws.Cells(ligne, col), ws.Cells(ligne, col)).Borders.Weight = 3

    @pyqtSlot()
    def clear(self):
        self.removeRows(0, self.rowCount())

    def set_model(self, model):
        self.clear()
        try:
            for key in model.keys():
                self.insert(self.count, model[key])
        except:
            try:
                for elt in model:
                    self.insert(self.count, elt)
            except:
                pass

class RecentFileListModel(ListModel):
    def __init__(self, name, parent=None, *args):
        super(RecentFileListModel, self).__init__(parent)
        self._name = name
        self._data = []
        self._roles = None
        self._db = None
        self._roles_name_to_int = None
        self.read_recent_file()

    def append(self, name, mac):
        sec = {}
        sec["numText"] = name
        sec["pathText"] = mac
        return self.insert(self.count, sec)

    def read_recent_file(self):
        try:
            with open(SETTINGS_PATH + "/recentFile.txt", "rb") as f:
                recentfile = json.loads(f.read())
                i = len(recentfile)
                while i > 0:
                    self.append(str(len(recentfile)-i+1)+".", recentfile[i-1])
                    i -= 1
        except:
            print("ERREUR : Aucun fichier recent", file=sys.stderr)


class NodeListModel(ListModel):
    def __init__(self, name, parent=None):
        super(NodeListModel, self).__init__([])
        self._name = name
        self._data = []
        self._roles = None
        self._db = None
        self._roles_name_to_int = None
        self.encas_list = []

    @pyqtSlot(float, float, float, str, result=bool)
    def append(self, x, y, z, ap):
        #TODO modifier le script pour prendre en compte la suppression d'un noeud
        return self.insert(self.count, {"id": self.get_next_id(), "cx": x, "cy": y, "cz": z, "ap": ap })

    @pyqtSlot(result=list)
    def get_encas(self):
        try:
            for x in self._data:
                if x['ap'] != 'Libre':
                    if int(x['id']) not in self.encas_list:
                        self.encas_list.append(int(x['id']))
            return self.encas_list
        except:
            pass

    @pyqtSlot(str,str, result=list)
    def add_encas(self, node_id, app):
        if app == 'Encastrement':
            if int(node_id) not in self.encas_list:
                self.encas_list.append(int(node_id))
        self.encas_list.sort()
        return self.encas_list

    @pyqtSlot(float, float, float, result=bool)
    def contain(self, x, y, z):
        return bool(len(list(filter(lambda elt: elt["cx"] == x and elt["cy"] == y and elt["cz"] == z, self._data))))

    def get_next_id(self):
        if not self._data:
            return 1
        return max(list(int(x["id"]) for x in self._data)) + 1

    @pyqtSlot(result=list)
    def get_ids(self):
        try:
            return list(x["id"] for x in self._data)
        except:
            pass


class PlatineListModel(ListModel):
    def __init__(self, name, parent=None, *args):
        super(PlatineListModel, self).__init__(parent)
        self._name = name
        self._data = []
        self._roles = None
        self._db = None
        self._roles_name_to_int = None

    @pyqtSlot(str,str, int, int, int,str,str,str,int, int, int, str, str, str, str, str, str, str, str, int, int, int, int, str, str, int, str, str, result=bool)
    def append4dw(self, dowelsNumber, axis, l, h, e,noeud, prod, mat, t, gamme_dowel, modele_dowel, type_dowel, deep_dowel, norme, type_charge, situation_initiale, cx0, cx1, cz0, cz1,
                  state_concrete, class_concrete, thick_concrete, armature_concrete, edf, b=None, a=None,orientation=None):

        return self.insert(self.count, {"id": self.get_next_id(),"dowelsnb": dowelsNumber, "axis": axis, "orientation": '', "l": l, "h": h,
                                        "e": e, "a": a, 'b': b, 'noeud': noeud, 'prod':prod, 'mat': mat,'t':t, 'gamme_dowel': gamme_dowel, 'modele_dowel': modele_dowel, 'type_dowel':
                                        type_dowel, 'deep_dowel': deep_dowel, 'norme': norme,
                                        'type_charge': type_charge, 'situation_initiale': situation_initiale,
                                        'cx0': cx0, 'cx1': cx1, 'cz0': cz0, 'cz1': cz1,
                                        'state_concrete': state_concrete, 'class_concrete': class_concrete,
                                        'thick_concrete': thick_concrete, 'armature_concrete': armature_concrete, 'EDF': edf})

    @pyqtSlot(str, str, int, int, int, str, str, str, int, int, str, str, str, str, str, str, str, str, int, int, int, int, str, str, int, str, str,result=bool)
    def append2dwV(self, dowelsNumber, axis, l, h, e,noeud, prod, mat, t, b, orientation, gamme_dowel,
                  modele_dowel, type_dowel, deep_dowel, norme, type_charge, situation_initiale, cx0, cx1, cz0, cz1,
                  state_concrete, class_concrete, thick_concrete, armature_concrete, edf):
        return self.insert(self.count, {"id": self.get_next_id(),"dowelsnb": dowelsNumber, "axis": axis, "orientation": orientation, "l": l, "h": h,
                                        "e": e, "a": '', 'b': b, 'noeud': noeud, 'prod':prod, 'mat': mat,'t':t,
                                        'gamme_dowel': gamme_dowel, 'modele_dowel': modele_dowel, 'type_dowel':
                                        type_dowel, 'deep_dowel': deep_dowel, 'norme': norme,
                                        'type_charge': type_charge, 'situation_initiale': situation_initiale,
                                        'cx0': cx0, 'cx1': cx1, 'cz0': cz0, 'cz1': cz1,
                                        'state_concrete': state_concrete, 'class_concrete': class_concrete,
                                        'thick_concrete': thick_concrete, 'armature_concrete': armature_concrete, 'EDF': edf})

    @pyqtSlot(str, str, int, int, int, str, str, str, int, int, str, str, str, str, str, str, str, str, int, int, int, int, str, str, int, str, str,result=bool)
    def append2dwH(self, dowelsNumber, axis, l, h, e, noeud, prod, mat, t, a, orientation, gamme_dowel,
                  modele_dowel, type_dowel, deep_dowel, norme, type_charge, situation_initiale, cx0, cx1, cz0, cz1,
                  state_concrete, class_concrete, thick_concrete, armature_concrete, edf):
        return self.insert(self.count, {"id": self.get_next_id(),"dowelsnb": dowelsNumber, "axis": axis, "orientation": orientation, "l": l, "h": h,
                                        "e": e, "a": a, 'b': '', 'noeud': noeud, 'prod':prod, 'mat': mat,'t':t,
                                        'gamme_dowel': gamme_dowel, 'modele_dowel': modele_dowel, 'type_dowel':
                                        type_dowel, 'deep_dowel': deep_dowel, 'norme': norme,
                                        'type_charge': type_charge, 'situation_initiale': situation_initiale,
                                        'cx0': cx0, 'cx1': cx1, 'cz0': cz0, 'cz1': cz1,
                                        'state_concrete': state_concrete, 'class_concrete': class_concrete,
                                        'thick_concrete': thick_concrete, 'armature_concrete': armature_concrete, 'EDF': edf})

    def get_next_id(self):
        if not self._data:
            return 1
        return max(list(int(x["id"]) for x in self._data)) + 1


    @pyqtSlot(result=list)
    def get_ids(self):
        return list(x["id"] for x in self._data)

    def set_model(self,model):
        self.clear()
        for i in range(len(model['nbCheville'])):
            elt = {"id": self.get_next_id(), "dowelsnb": model['nbCheville'][i], "axis": model['axis'][i], "orientation": model['orientation'][i], "l": model['l'][i],
             "h": model['h'][i],"e": model['e'][i], "a": model['a'][i], 'b': model['b'][i], 'noeud': model['noeud'][i], 'prod': model['prod'][i], 'mat': model['mat'][i], 't': model['t'][i]}
            self.insert(self.count, elt)



class BeamListModel(ListModel):
    def __init__(self, name, parent=None, *args):
        super(BeamListModel, self).__init__(parent)
        self._name = name
        self._data = []
        self._roles = None
        self._db = None
        self._roles_name_to_int = None


    @pyqtSlot(int, int, str, str, str, float,int, result=bool)
    def append(self, n1, n2, prod, mat, sec, ori,t):
        return self.insert(self.count, {"id": self.get_next_id(), "n1": n1, "n2": n2, "prod": prod, "mat": mat
                                    , "sec": sec, 'or': ori, 't': str(float(t))})


    @pyqtSlot(int, int, result=bool)
    def contain(self, n1, n2):
        return bool(len(list(filter(lambda elt: elt["n1"] == min(n1, n2) and elt["n2"] == max(n1, n2), self._data))))

    @pyqtSlot(int,int,list,result=bool)
    def check_node_beam(self,n1,n2,node_list):
        print(node_list)
        if n1 in node_list and n2 in node_list:
            return True
        else:
            return False



    def get_next_id(self):
        if not self._data:
            return 1
        return max(list(int(x["id"]) for x in self._data)) + 1

    @pyqtSlot(result=list)
    def get_ids(self):
        return list(x["id"] for x in self._data)

    @pyqtSlot(int, result=str)
    def get_name(self, index):
        return self._data[index]['name']


class StirrupListModel(ListModel):
    def __init__(self, name, parent=None, *args):
        super(StirrupListModel, self).__init__(parent)
        self._name = name
        self._data = []
        self._roles = None
        self._db = None
        self._roles_name_to_int = None

    def append(self, nom, Dn, l, d, t, pas, Sb, As, dm, do, tp, A, fu, Fub, fy, Su, Sy, p1u, e1u, e2u, Ft, Fv, Fp, Fb="", Bp="", norm="rccm"):

        mat = {}
        mat["nom"] = nom
        mat["DN"] = Dn
        mat["pas"] = pas
        mat["Sb"] = Sb
        mat["As"] = As
        mat["dm"] = dm
        mat["Do"] = do
        mat["tp"] = tp
        mat["A"] = A
        mat["fu"] = fu
        mat["Fub"] = Fub
        mat["fy"] = fy
        mat["Su"] = Su
        mat["Sy"] = Sy
        mat["P1"] = p1u
        mat["e1"] = e1u
        mat["e2"] = e2u
        mat["Ft"] = round(Ft, 2)
        try:
            mat["Fp"] = round(Fp, 2)
        except:
            mat["Fp"] = ""
        mat["Fv"] = round(Fv, 2)
        try:
            mat["Fb"] = round(Fb, 2)
            mat["Bp"] = round(Bp, 2)
        except:
            mat["Fb"] = Fb
            mat["Bp"] = Bp
        if norm == "rccm":
            mat["l"] = l
        else:
            mat["l"] = ""
        mat["d"] = d
        mat["t"] = t
        return self.insert(self.count, mat)

    @pyqtSlot(str, result=bool)
    def contain(self, name):
        return bool(len(list(filter(lambda elt: elt["nom"] == name, self._data))))

    def set_model(self, mat):
        for i in range(len(mat)):
            elt = {
                "nom": mat[i]["nom"],
                "DN": mat[i]["DN"],
                "pas": mat[i]["pas"],
                "Sb": mat[i]["Sb"],
                "As": mat[i]["As"],
                "dm": mat[i]["dm"],
                "Do": mat[i]["Do"],
                "tp": mat[i]["tp"],
                "A": mat[i]["A"],
                "fu": mat[i]["fu"],
                "Fub": mat[i]["Fub"],
                "fy": mat[i]["fy"],
                "Su": mat[i]["Su"],
                "Sy": mat[i]["Sy"],
                "P1": mat[i]["P1"],
                "e1": mat[i]["e1"],
                "e2": mat[i]["e2"],
                "Ft": mat[i]["Ft"],
                "Fp": mat[i]["Fp"],
                "Fv": mat[i]["Fv"],
                "Fb": mat[i]["Fb"],
                "Bp": mat[i]["Bp"],
                "l": mat[i]["l"],
                "d": mat[i]["d"],
                "t": mat[i]["t"]
            }
            return self.insert(self.count, elt)

    @pyqtSlot(int, result=bool)
    def remove(self, index):
        print("remove")
        if index == -1:
            index = 0
        super(QAbstractListModel, self).beginRemoveRows(QModelIndex(), index, index)
        del self._data[index]
        super(QAbstractListModel, self).endRemoveRows()
        self.countChanged.emit()
        return True

    @pyqtSlot(int, result=str)
    def get_name(self, index):
        return self._data[index]['nom']

class FamilyListModel(ListModel):
    def __init__(self, name, parent=None, *args):
        super(FamilyListModel, self).__init__(parent)
        self._name = name
        self._data = []
        self._roles = None
        self._db = None
        self._roles_name_to_int = None

    @pyqtSlot(str, str, bool)
    def append(self, nb, name, imprt):
        sec = {}
        sec["nb"] = nb
        sec["name"] = name
        sec["imprt"] = imprt
        return self.insert(self.count, sec)

    @pyqtSlot(str)
    def extract(self, path):
        self.removeRows(0, self.rowCount())
        self.append(self.rowCount() + 1, "Famille actuelle", True)
        path = path.replace("file:///", "")
        if not "/02 - Familles" in path:
            path += "/02 - Familles"
        listFolder = [f for f in listdir(path) if not isfile(join(path, f))]
        for folder in listFolder:
            self.append(self.rowCount() + 1, folder, True)

    @pyqtSlot()
    def erase(self):
        self.removeRows(0, self.rowCount())