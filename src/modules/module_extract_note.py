from PyQt5.QtCore import QObject
from src.modules.components import TextField, Combobox, ListView
from src.models.list_model import FamilyListModel
from src.modules.note import Note
from src.constantes import *

class NoteDeCalcul():

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.noteDoc = None

        self.general = General(parent)
        self.familles = Familles(parent)
        self.annexe = Annexes(parent)

        # self.rccm = sv.rccm

    def __getstate__(self):
        return (self.general, self.familles, self.annexe)

    def __setstate__(self, state):
        (self.general, self.familles, self.annexe) = state

    def iterator(self):
        return [self.general, self.familles, self.annexe]

    def updateQML(self, parent):
        for elt in self.iterator():
            elt.updateQML(parent)

    def setParent(self, parent):
        self.parent = parent
        for elt in self.iterator():
            elt.parent = parent

    def generateNote(self):
        # if sv.rccm.checked == True:
        # Uniquement RCC-M disponible sur Osup
        self.noteDoc = Note(PATH_TEMPLATE_NOTE_RCCM, self.parent)
        # else:
        #     self.noteDoc = Note(PATH_TEMPLATE_NOTE_EN, self.parent)
        self.noteDoc.setVisible(True)
        self.familles.extractFamille()
        self.general.generateNote(self.noteDoc)
        # self.verifSupport.generateNote(self.noteDoc)
        # self.verifSupport.generateNote(self.noteDoc, 2)

class General():

    def __init__(self, parent):
        self.parent = parent
        self.title = TextField("ndcTitreTextField", parent)
        self.client = TextField("ndcClientTextField", parent, defaultText="SOM CALCUL")
        self.redacteur = TextField("ndcRedacteurTextField", parent)
        self.verificateur = TextField("ndcVerificateurTextField", parent)
        self.approbateur = TextField("ndcApprobateurTextField", parent)
        self.etat = Combobox("ndcEtatComboBox", parent, text="BPO")
        self.indice = Combobox("ndcIndiceComboBox", parent, text="A")
        self.date = TextField("ndcDateTextField", parent)
        self.site = TextField("ndcNomSiteTextField", parent)
        self.reference = TextField("ndcRefTextField", parent)

    def __getstate__(self):
        return (self.title, self.client, self.redacteur, self.verificateur, self.approbateur, self.etat, self.indice, self.date, self.site, self.reference)

    def __setstate__(self, state):
        (self.title, self.client, self.redacteur, self.verificateur, self.approbateur, self.etat, self.indice, self.date, self.site, self.reference) = state

    def iterator(self):
        return [self.title, self.client, self.redacteur, self.verificateur, self.approbateur, self.etat, self.indice, self.date, self.site, self.reference]

    def updateQML(self, parent):
        for elt in self.iterator():
            elt.updateQML(parent)

    def generateNote(self, noteDoc):
        noteDoc.stringToWord("TITLE_1", self.title._text, None)
        noteDoc.stringToWord("TITLE_2", self.title._text, None)

        noteDoc.stringToWord("REF_1", self.reference._text, None)
        noteDoc.stringToWord("REF_2", self.reference._text, None)

        noteDoc.stringToWord("DATE", self.date._text, None)
        noteDoc.stringToWord("REDAC", self.redacteur._text, None)
        noteDoc.stringToWord("VERIF", self.verificateur._text, None)
        noteDoc.stringToWord("APPROBATEUR", self.approbateur._text, None)

        noteDoc.stringToWord("NOM_SITE_1", self.site._text, None)

        # noteDoc.stringToWord("CONTRAT", "Contrat", None)
        # noteDoc.stringToWord("AFFAIRE", "Affaire", None)
        noteDoc.stringToWord("SITES", self.site._text, None)
        # noteDoc.stringToWord("TRANCHES", "Tranches", None)
        for i in range(1, 5):
            if i == 1:
                noteDoc.stringToWord("ETAT_{}".format(str(i)), self.etat._currentText, None)
            noteDoc.stringToWord("INDICE_{}".format(str(i)), self.indice._currentText, None)

class Familles():
    def __init__(self, parent):
        self.parent = parent
        self.dossier = TextField("FamilyFolderPath", parent)
        self.listFamille = ListView("FamilyListView", parent, model=FamilyListModel([]))

    def __getstate__(self):
        return (self.dossier, self.listFamille)

    def __setstate__(self, state):
        (self.dossier, self.listFamille) = state

    def iterator(self):
        return [self.dossier, self.listFamille]

    def updateQML(self, parent):
        for elt in self.iterator():
            elt.updateQML(parent)

    def setPath(self, folderPath):
        self.dossier._text = "/".join([folderPath,"02 - Familles"])
        self.dossier.updateQML(self.parent)
        pass

    def extractFamille(self):
        noteKeys =  ["Localisation", "Familles", "Observation"]
        noteData = []
        dic = {}
        for famille in self.listFamille._model._data:
            pass


class Annexes():

    def __init__(self, parent):
        self.parent = parent

    def __getstate__(self):
        return ()

    def __setstate__(self, state):
        # ( ) = state
        pass

    def iterator(self):
        return []

    def updateQML(self, parent):
        for elt in self.iterator():
            elt.updateQML(parent)

    def generateNote(self):
        pass

    def miseEnFormeNote(self):
        pass

