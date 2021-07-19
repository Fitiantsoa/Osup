from PyQt5.QtCore import QObject, QEventLoop
from PyQt5.QtQuick import QQuickImageProvider
# ----------------------------------------------------------------------------------------------------------------------
#                                       Fichier Components listant tout les composants de base
# ----------------------------------------------------------------------------------------------------------------------

# Ce fichier définit définit tout les composants de base utilisé jusqu'à présent dans nos applications
# Chaque composant possède au minimum trois fonctions lui permettant d'être constament à jour avec
# l'interface graphique par le biais de signaux connectés.

# Fonctions communes :

# Mettre à jour l'interface graphique -> update_qml(parentSibling)
# Mettre à jour Python (fonction connectée à un signal QML :
# - par exemple "checkStateChanged" pour une checkbox) -> set_from_qml(parentSibling)

# NOTA : Il est impossible de sauvegarder un objet QML, impossible donc de sauvegarder le parentSibling.
#        Lors d'un setstate, parentSibling est alors None, d'ou la comparaison avant le branchement de signal !
#        Il faut ensuite reconnecter les signaux au bon composant QML (update_qml).

# Réinitialiser le composant -> reset()


class Checkbox:
    """ CheckBox
    :attr objetName: nom necessaire à la recherche du composant QML équivalent
    :attr checked: état du composant
    """
    def __init__(self, objetName, parentSibling, value=False):
        self._objetName = objetName
        self._checked = value
        if parentSibling is not None:  # <==> Constructeur non appelé par setstate
            # On connecte notre composants Python avec le composants QML
            # Pour une checkbox, c'est l'état checked qui nous interresse, on met à jour Python
            # lorsque cet état change (checkStateChanged)
            parentSibling.findChild(QObject, self._objetName).checkStateChanged.connect(lambda: self.set_from_qml(parentSibling))

    def update_qml(self, parentSibling):
        """
        Can update all checkboxes in QML
        :param parentSibling: Checkbox parent objectName
        :return:
        """
        qml = parentSibling.findChild(QObject, self._objetName)
        qml.setProperty("checked", self._checked)
        # Lors du chargement d'un ancien fichier, la reconnection aux composants est nécessaire.
        parentSibling.findChild(QObject, self._objetName).checkStateChanged.connect(lambda: self.set_from_qml(parentSibling))

    def set_from_qml(self, parentSibling):
        """
        Update python object linked with the checkbox
        :param parentSibling: ObjectName of the checkbox
        :return:
        """
        qml = parentSibling.findChild(QObject, self._objetName)
        self._checked = qml.property("checked")

    def reset(self):
        """
        Set the checkState to False.
        :return: Void
        """
        self._checked = False


class RadioButton:
    def __init__(self, object_name, parent_sibling):
        self._object_name = object_name
        self._sibling = parent_sibling.findChild(QObject, object_name)
        self._sibling.checkedChanged.connect(self.set_from_qml)
        self._checked = self._sibling.property("checked")

    def update_qml(self, checked):
        self._checked = checked
        self._sibling.setProperty("checked", self._checked)
        self._sibling.checkedChanged.connect(self.set_from_qml)

    def set_from_qml(self):
        self._checked = self._sibling.property("checked")


class Combobox:
    """ Combobox

    :attr objetName: nom necessaire à la recherche du composant QML équivalent
    :attr currentIndex: correspond à l'index de l'élement choisi dans la combobox
    :attr currentText: correspond au texte de l'élement choisi dans la combobox
    """
    def __init__(self, objetName, parentSibling, index=0, text="", enabled=True):
        self._objetName = objetName
        self._currentIndex = index
        self._currentText = text
        if parentSibling is not None:# <==> Constructeur non appelé par setstate
            # On connecte notre composants Python avec le composants QML
            # Pour une combobox, c'est la propriété currentText qui nous interresse, on met à jour Python
            # lorsque cet état change (currentTextChanged)

            # NOTA : si la connection est faite avec "currentIndexChanged",la fonction est appelée avant de
            # mettre à jour le texte, Python sera donc à jour avec l'ancienne valeur de currentText.
            parentSibling.findChild(QObject,self._objetName).currentTextChanged.connect(lambda: self.set_from_qml(parentSibling))

    def update_qml(self, parentSibling):
        """
        Update combobox in qml from python
        :param parentSibling: parent of checkbox
        :return: Void
        """
        qml = parentSibling.findChild(QObject, self._objetName)
        qml.setProperty("currentText", self._currentText)
        qml.setProperty("currentIndex", self._currentIndex)
        # Lors du chargement d'un ancien fichier, la reconnection aux composants est nécessaire.
        parentSibling.findChild(QObject, self._objetName).currentTextChanged.connect(lambda: self.set_from_qml(parentSibling))

    def set_from_qml(self, parentSibling):
        """
        Set datas from combobox to python
        :param parentSibling: Parent of combobox
        :return: Void
        """
        qml = parentSibling.findChild(QObject, self._objetName)
        self._currentIndex = qml.property("currentIndex")
        self._currentText = qml.property("currentText")

    def reset(self):
        pass


class TextField:
    def __init__(self, object_name, parent_sibling, text="",  defaultText=""):
        self._object_name = object_name
        self._sibling = parent_sibling.findChild(QObject, object_name)
        self._text = text
        self._defaultText = defaultText

        self._sibling.textChanged.connect(self.set_from_qml)
        self._sibling.editingFinished.connect(self.set_from_qml)

    def update_qml(self, text):
        self._text = text
        if self._text != self._defaultText:
            self._sibling.setProperty("text", self._text)
        else:
            pass

    def set_from_qml(self):
        """
        Update python datas from qml textfield
        :param parentSibling:
        :return: 0
        """
        self._text = self._sibling .property("text")
        return 0

    def reset(self):
        """
        Set textfield text to default text
        :return: Void
        """
        self._text = self._defaultText


class TextArea:
    """ TextArea

        :attr objetName: nom necessaire à la recherche du composant QML équivalent
        :attr text: correspond au texte de l'élement choisi dans la combobox
        :attr defaultText: correspond au texte par defaut à mettre dans la combobox
    """
    def __init__(self, objetName, parentSibling, text="", defaultText=""):
        self._objetName = objetName
        self._text = text
        self._color = "#28bd2d"
        self._defaultText = defaultText
        if parentSibling is not None:  # <==> Constructeur non appelé par setstate
            # On connecte notre composants Python avec le composants QML
            # Pour une textarea, c'est la propriété text qui nous interresse, on met à jour Python
            # lorsque l'edition du texte est finie (editingFinished)
            parentSibling.findChild(QObject, self._objetName).editingFinished.connect(
                lambda: self.set_from_qml(parentSibling))

    def update_qml(self, parentSibling):
        """
        Update textArea qml
        :param parentSibling: Parent of component
        :return: Void
        """
        # Lors du chargement d'un ancien fichier, la reconnection aux composants est nécessaire.
        try:
            parentSibling.findChild(QObject, self._objetName).editingFinished.connect(
                lambda: self.set_from_qml(parentSibling))
        except:
            pass

        # Afin de gagner du temps, au compare si la valeur de text est celle par defaut, si oui on passe la fonction.
        if self._text != self._defaultText:
            qml = parentSibling.findChild(QObject, self._objetName)
            qml.setProperty("text", self._text)
        else:
            pass

    def set_from_qml(self, parent=None):
        """
        Set datas from qml to python
        :param parent: Parent of component
        :return: Void
        """
        qml = parent.findChild(QObject, self._objetName)
        self._text = qml.property("text")

    def reset(self):
        """
        Set textarea datas to default data
        :return: Void
        """
        self._text = self._defaultText


class ListView:
    """ Listview

        :attr objetName: nom necessaire à la recherche du composant QML équivalent
        :attr db: correspond au fichier JSON correspondant (uniquement si necessaire)
        :attr data: correspond au données du model correspondant à la listview
        :attr roles: correspond aux roles du model correspondant à la listview
        :attr roles_name_to_int: correspond à la conversion faite par Qt avec les roles
    """
    def __init__(self, object_name, parentSibling=None, model=None):
        self._object_name = object_name
        self._sibling = parentSibling.findChild(QObject, object_name)
        self._model = self._sibling.property("model")
        self._sibling.property("model").dataChanged.connect(self.set_from_qml)

    def set_model_data(self, data):
        self._model.set_model(data)

    def update_qml(self):
        """Update qml data with python data"""
        m = self._sibling.property("model")
        m._data = self._model._data
        m._roles = self._model._roles
        m._roles_name_to_int = self._model._roles_name_to_int
        self._sibling.setProperty("model", [])
        self._sibling.setProperty("model", m)
        m.countChanged.emit()

    def set_from_qml(self):
        """Update python with qml information"""
        m = self._sibling.property("model")
        if not isinstance(m, list):
            m = m._data
        if m != self._model._data:
            self.set_model_data(m)

    def remove(self, idx):
        m = self._sibling.property("model")
        m.remove(idx)

    def reset(self):
        self._model.clear()


class TreeView:
    def __init__(self, name, model=None):
        self.name = name
        self._root = model.root

    def update_qml(self, parent):
        qml = parent.findChild(QObject, self.name)
        m = qml.property("model")
        m._root = self._root
        qml.setProperty("model", [])
        qml.setProperty("model", m)
        m.countChanged.emit()

    def set_from_qml(self, parent):
        qml = parent.findChild(QObject, self.name)
        self.setModel(qml.property("model"))