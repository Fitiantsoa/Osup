# ----------------------------------------------------------------------------------------------------------------------
#                                                Fichier de class d'un treemodel
# ----------------------------------------------------------------------------------------------------------------------


# Ce fichier est le fichier de base d'un treeModel, il est utile lorsque l'on souhaite ajouter un model au fichier
# "tree_model_OApp.py", tout treemodel héritera de cette classe est possèdera chaque fonction
import json
from PyQt5.QtCore import QAbstractItemModel, QVariant
from PyQt5.QtCore import pyqtSlot, QModelIndex, Qt
from src.constantes import MATERIAL_DB, PROFILE_DB
# Un treeModel est l'élement permettant de gérer une arborescence d'élement. Il est utile lorsque l'on
# souhaite afficher une liste de fichiers et dossiers (exactement comme dans votre OS)

# Pour pouvoir utiliser un treeModel, il faut dans un premier temps créer un element du treeModel appelé
# "Node", cet élement sera la racine de notre treeModel, il suffira ensuite de créer d'autres élements pour
# récréer l'arborescence.
#
# ex :

#                                          Un élement de l'arborescence possède :
#        *  *                                 - une liste d'enfant du même type (node)
#     *        *                              - un seul parent du même type (sauf la racine)
#    *   node   *                             - un nom
#     *        *                              - le nom du parent et du grand parent
#        *  *                                 - le valeur de l'étage de l'element (racine._floor = 0)
#
#
#                                                           (*) = 1 node          (*) Racine
#           TreeModel :                                                          /   \
#           Un treemodel est définit uniquement par sa racine                  /       \
#           et les fonctions associés. A partir de cette racine,             (*)       (*) étage n°1
#           on reconstruit toute l'arborescence du treemodel.              /         /     \
#           Il est également possible de modifier l'élement node         (*)       (*)     (*) étage n°2
#           pour personnaliser son treemodel.                           /   \       |     /   \
#                                                                     (*)   (*)    (*)  (*)   (*) étage n°3
#                                                                      |     |      |    |     |

# Classe définissant un élement de l'arborescence


class GroupNode(object):
    """A group node in the tree of databases model."""

    def __init__(self, parent, name,description,floor,data):
        """Create a group node for the tree of databases model."""

        self.children = []
        self.parent = parent
        self.name = name
        self._description = description
        self._floor = floor
        self._data = data

    def __len__(self):
        return len(self.children)

    def insertChild(self, child, position=0):
        """Insert a child in a group node."""
        self.children.insert(position, child)

    def childAtRow(self, row):
        """The row-th child of this node."""
        return self.children[row]

    def childIndex(self, index, row):
        idx = index.sibling(row,1)
        return idx

    def row(self):
        """The position of this node in the parent's list of children."""
        if self.parent:
            var =self.parent.children.index(self)
            return var
        return 0

    def childCount(self):
        return len(self.children)

    def getDescription(self):
        return self._description

    def getFloor(self):
        return self._floor

    def getData(self):
        data = self._data
        return data

    def getChildPosByName(self,name):
        for child in self.children:
            if child.name == name:
                return self.children.index(child)


class TreeModel(QAbstractItemModel):
    def __init__(self, parent=None):
        """Create the model."""
        QAbstractItemModel.__init__(self, parent)
        # Populate the model
        self.root = GroupNode(None, 'root',"root",0,[])
        self.dataHasChanged = False

    def flags(self, index):
        """Returns the item flags for the given index. """
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def data(self, index, role):
        """Returns the data stored under the given role for the item
        referred to by the index."""

        if not index.isValid():
            return QVariant()
        node = self.nodeFromIndex(index)
        if role == Qt.DisplayRole:
            return node.name
        else:
            return node.name

    def setData(self, index, name,description,floor,data, role=Qt.DisplayRole):
        """Sets the role data for the item at index to value."""
        if not index.isValid():
            return False
        node = self.nodeFromIndex(index)
        if role == Qt.DisplayRole:
            node.name = name
            node._description = description
            node._floor = floor
            node._data = data
            self.dataChanged.emit(index, index)
            return True
        else:
            node.name = name
            node._description = description
            node._floor = floor
            node._data = data
            self.dataChanged.emit(index, index)
            return True

    def roleNames(self):
        roles={
            Qt.UserRole + 1: b"name"
        }
        return roles

    def headerData(self, section, orientation, role):
        """Returns the data for the given role and section in the header
        with the specified orientation.
        """

        if (orientation, role) == (Qt.Horizontal, \
                                   Qt.DisplayRole):
            return QVariant(('Sample tree',''))
 # self.root.name(section)
        return QVariant() #None

    def columnCount(self, parent):
        """The number of columns for the children of the given index."""
        return 1

    def rowCount(self, parent):
        """The number of rows of the given index."""

        if not parent.isValid():
            parent_node = self.root
        else:
            parent_node = parent.internalPointer()
        return len(parent_node)

    def hasChildren(self, index):
        """Finds out if a node has children."""

        if not index.isValid():  # self.root fulfils this condition
            return True
        parent = self.nodeFromIndex(index)
        if parent.children != []:
            return True
        else:
            return False

    def index(self, row, column, parent):
        """Creates an index in the model for a given node and returns it."""
        if self.hasIndex(row,column,parent):
            assert self.root
            branch = self.nodeFromIndex(parent)
            assert branch is not None
            return self.createIndex(row, column, branch.childAtRow(row))
        else:
            return QModelIndex()

    def nodeFromIndex(self, index):
        """Retrieves the tree node with a given index."""
        if index.isValid():
            return index.internalPointer()
        else:
            return self.root

    def parent(self, child):
        """The parent index of a given index."""

        node = self.nodeFromIndex(child)
        if not child.isValid():
            return QModelIndex()
        if node is None:
            return QModelIndex()
        parent = node.parent
        if parent is None:
            return QModelIndex()
        grandparent = parent.parent
        if grandparent is None:
            return QModelIndex()
        row = parent.row()
        assert row != -1
        return self.createIndex(row, 0, parent)

    def deleteNode(self, index):
        """Delete a node from the model."""
        self.dataHasChanged = True
        try :
            node = self.nodeFromIndex(index)
            # Deletes the node from the tree of databases model/view
            parent = self.parent(index)
            position = node.row()
            self.removeRows(position, 1, parent)
        except:
            print("Selectionner l'élement à supprimer")

    def addBranch(self, index, childname, description, data, floor=1):
        """Create a new branch under the given parent."""
        self.insertRows(0, 1, index)
        child_idx = self.index(0, 0, index)
        self.setData(child_idx, childname,description,floor,data)
        return True

    def insertRows(self, position=0, count=1, parent=QModelIndex()):
        """Insert `count` rows after the given row."""
        node = self.nodeFromIndex(parent)
        self.beginInsertRows(parent, position,
                             position + count - 1)
        child = GroupNode(node,'Unknown',"",0,[])
        node.insertChild(child, position)
        self.endInsertRows()
        return True

    def insertRowsData(self, data, value, position=0, count=1, parent=QModelIndex()):
        self.dataHasChanged = True
        node = self.nodeFromIndex(parent)
        self.beginInsertRows(parent, position,
                             position + count - 1)
        child = GroupNode(node, value, data[1], data[2], data[3])
        node.insertChild(child, position)
        self.endInsertRows()
        return True

    def removeRows(self, position, count=1, parent=QModelIndex()):
        """Removes `count` rows before the given row."""
        self.dataHasChanged = True
        node = self.nodeFromIndex(parent)
        self.beginRemoveRows(parent, position,
                             position + count - 1)
        for row in range(count):
            del node.children[position + row]
        self.endRemoveRows()
        return True

    @pyqtSlot(QModelIndex, float)
    def addDataTree(self, index, value):
        self.dataHasChanged = True
        node = self.nodeFromIndex(index)
        node._data.append(value)
        self.dataChanged.emit(index, index)
        return True

    @pyqtSlot(QModelIndex, str)
    def addDataTitle(self, index, value):
        self.dataHasChanged = True
        node = self.nodeFromIndex(index)
        node.name = value
        self.dataChanged.emit(index, index)
        return True

    @pyqtSlot(QModelIndex, int)
    def delValue(self, index, pos):
        self.dataHasChanged = True
        node = self.nodeFromIndex(index)
        try:
            del node._data[pos]
            self.dataChanged.emit(index, index)
        except:
            pass
        return True

    @pyqtSlot(QModelIndex)
    def delNode(self, index):
        self.deleteNode(index)

    @pyqtSlot(QModelIndex,result=str)
    def description(self, index):
        node = self.nodeFromIndex(index)
        return node.getDescription()

    @pyqtSlot(QModelIndex, result=list)
    def listData(self, index):
        node = self.nodeFromIndex(index)
        return [node.getData()]

    @pyqtSlot(QModelIndex, result=int)
    def floor(self, index):
        node = self.nodeFromIndex(index)
        return node.getFloor()

    @pyqtSlot(QModelIndex, result=int)
    def brotherCount(self, index):
        node = self.nodeFromIndex(index.parent())
        return node.childCount()

    @pyqtSlot(QModelIndex, result=int)
    def childCount(self, index):
        node = self.nodeFromIndex(index)
        return node.childCount()

    @pyqtSlot(QModelIndex)
    def maJ(self,index):
        self.dataChanged.emit(index,index)
        return True

    @pyqtSlot(str)
    @pyqtSlot(list)
    @pyqtSlot(QModelIndex)
    def print(self, msg):
        print(msg)
        return True


class ProfileTreeModel(TreeModel):
    def __init__(self, name, parent=None, *args):
        super(ProfileTreeModel, self).__init__(parent)
        self._name = name
        self.root = GroupNode(None, 'root', "root", 0, [])
        self.addJson()

    def addJson(self):
        profile_type = []
        with open(PROFILE_DB) as bd:
            f = bd.read()
            donnees = json.loads(f)
            for tpe in donnees.keys():
                self.addBranch(QModelIndex(), tpe, "Type", [])
                profile_type.append(self.root.childAtRow(0))  # parents[0].childCount()-1))
                for sz in donnees[tpe]:
                    x = donnees[tpe][sz]
                    profile_type[-1].insertChild(GroupNode(profile_type[-1], sz, "Dimension", 2, x))
        return True

    @pyqtSlot(QModelIndex,str)
    def ajoutNode(self, index, value):
        DEFAULT = {"h": "0", "b": "0", "tw": "0", "tf": "0", "aire": "0", "sy": "0", "sz": "0", "wy": "0", "wz": "0", "ig": "0", "iy": "0", "iz": "0", "igr": "0", "wely": "0", "wply": "0", "welz": "0", "wplz": "0", "iw": "0", "vy": "0", "vx": "0"}
        self.dataHasChanged = True
        node = self.nodeFromIndex(index)
        padre = node.parent
        flr = node._floor
        if flr == 1:
            self.addBranch(QModelIndex(), value, "Type", [])
            padre.childAtRow(0).insertChild(GroupNode(padre.childAtRow(0), "?", "Dimension", 2, [DEFAULT]))
        else:
            self.insertRowsData(["", "Dimension", 2, [DEFAULT]], value, 0, 1, index.parent())
        return True

    @pyqtSlot(QModelIndex, int, float)
    def setDataTree(self, index, pos, value):
        self.dataHasChanged = True
        node = self.nodeFromIndex(index)
        node._data[pos] = value
        self.dataChanged.emit(index, index)
        return True

    @pyqtSlot()
    def nodeToJson(self):
        str = {}
        for child in self.root.children:
            dn = {}
            for child2 in child.children:
                dn.update({child2.name: child2._data})
            str.update({child.name: dn})
        with open(PROFILE_DB, 'w') as f:
            str = json.dumps(str)
            f.write(str)
        self.dataHasChanged = False
        return True


class MaterialTreeModel(TreeModel):
    def __init__(self, name, parent=None, *args):
        super(MaterialTreeModel, self).__init__(parent)
        self._name = name
        self._root = GroupNode(None, 'root', "root", 0, [])
        self.addJson()

    def addJson(self):
        parents = [self.root]
        Codes = []
        DN = []
        with open(MATERIAL_DB) as bd:
            f = bd.read()
            role_list = {"Réglementation": "Réglementation", "Matériaux": "Matériaux", "Température": "Température"}
            donnees = json.loads(f)
            for code in donnees.keys():
                self.addBranch(QModelIndex(), code, "Réglementation", [])
                Codes.append(parents[0].childAtRow(0))  # parents[0].childCount()-1))
                for materiaux in donnees[code]:
                    Codes[-1].insertChild(GroupNode(Codes[-1], materiaux, "Matériaux",2,[]))
                    DN.append(Codes[-1].childAtRow(0))
                    for temp in donnees[code][materiaux]:
                        x = donnees[code][materiaux][temp]
                        # if isinstance(x, (list)):
                        #     x = x[0]
                        DN[-1].insertChild(GroupNode(DN[-1], temp, "Température", 3, x))
        return True

    @pyqtSlot(QModelIndex, str)
    def ajoutNode(self, index, value):
        self.dataHasChanged = True
        node = self.nodeFromIndex(index)
        padre = node.parent
        temp = [0,20,50,100,150,200,250,300]
        newNode = []
        flr = node._floor
        if flr == 1:
            self.addBranch(QModelIndex(), value, "Réglementation",[])
            padre.childAtRow(0).insertChild(GroupNode(padre.childAtRow(0), "?", "Matériaux",2,[]))
            newparent = padre.childAtRow(0)
            newNode.append(newparent.childAtRow(0))
            padre.childAtRow(0).insertChild(GroupNode(padre.childAtRow(0), "?", "Matériaux",2,[]))
            newNode.append(newparent.childAtRow(0))
            for nodes in newNode:
                for temperature in temp:
                    nodes.insertChild(GroupNode(nodes, temperature, "Température", 3,{"E": 0, "a": 0, "S": 0, "Sy": 0, "Rm":0}))
        else:
            self.insertRowsData(["","Température", 3,{"E": 0, "a": 0, "S": 0, "Sy": 0, "Rm":0}], value, 0, 1, index.parent())
            newparent = padre.childAtRow(0)
            if node.children != []:
                for temperature in temp:
                    newparent.insertChild(GroupNode(newparent, temperature,"Température", 3,{"E": 0, "a": 0, "S": 0, "Sy": 0, "Rm":0}))
                # node.insertChild(GroupNode(node, [value, ""]))
        return True

    @pyqtSlot(QModelIndex, float, float, float, float, float)
    def setDataTree(self, index, E, a, S, Sy, rm):
        self.dataHasChanged = True
        node = self.nodeFromIndex(index)
        node._data = {"E":E,"a":a,"S":S,"Sy":Sy,'Rm':rm}
        self.dataChanged.emit(index, index)
        return True

    @pyqtSlot()
    def nodeToJson(self):
        str = {}
        for child in self.root.children:
            dn = {}
            for child2 in child.children:
                value = {}
                for child3 in child2.children:
                    value.update({child3.name: child3._data})
                dn.update({child2.name: value})
            str.update({child.name: dn})
        with open(MATERIAL_DB, 'w') as f:
            str = json.dumps(str)
            f.write(str)
            print("Modification enregistrée")
        self.dataHasChanged = False
        return True
