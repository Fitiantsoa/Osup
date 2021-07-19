import win32com.client as win32
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from som.constantes import *
from win32com.client import constants as c

class Note():
    def __init__(self, tempPath, parent, app):
        self.nbrTableau = 0
        self.wordApp = win32.gencache.EnsureDispatch('Word.Application')
        self.constant = win32.constants
        self.wordApp.Visible = False

        # splashNoteFlexPix = QPixmap("qml/images/Otau_SS.png")
        # self.splashNoteFlex = QSplashScreen(splashNoteFlexPix, Qt.WindowStaysOnTopHint)
        # self.splashNoteFlex.setMask(splashNoteFlexPix.mask())
        # self.splashNoteFlex.show()
        self.bar = parent.findChild(QObject, "stateNoteProgressBar")
        self.stateText = parent.findChild(QObject, "stateNoteTextField")
        self.app = app

        self.state = 0
        self.setSSText("Ouverture Word")

        self.doc = self.wordApp.Documents.Open(tempPath)
        self.pathFinalDoc = None
        self.nomFinalDoc = None

        self.path = None

    def modelToWord(self,signet, data, indexTableau):
        '''
        Fonction qui va écrire un tableau des data au signet précis.
        data doit etre impérativement une liste de dictionnaire
        Les dictionnaires doivent avoir les memes clés
        L'entete du tableau sera les clés du dictionnaire data
        Le style du tableau est Otau_Style_Table
        '''
        print(data)

        rng = self.doc.Bookmarks(signet).Range
        keys = list(data[0].keys())
        nbrCol = len(keys)
        nbrLig = 1 + len(data) 
        indexTableau += self.nbrTableau
        table = self.doc.Tables.Add(rng, NumRows=nbrLig, NumColumns=nbrCol)
        title = table.Cell(1, 1).Range.Text
        for i in range(0, nbrCol):
            self.stringToCell(table.Cell(1,i+1).Range,keys[i],8)
        for i in range(0, nbrLig - 1):
            for j in range(0, nbrCol):
                self.stringToCell(table.Cell(i+2, j + 1).Range, data[i][keys[j]][0], data[i][keys[j]][1])

        table.Style = self.doc.Styles("Otau_tab")
        table.AutoFitBehavior(self.constant.wdAutoFitContent)
        table.Rows.Alignment = self.constant.wdAlignRowCenter
        # self.doc.Tables(indexTableau).AutoFitBehavior(2)

        if indexTableau - self.nbrTableau == TAB_ANNEXE_SPECTRE[1]:
            rng = self.doc.Range(table.Range.End,table.Range.End)
            rng.Text = "\f"




        self.nbrTableau += 1
        print("Tableau "+signet+" ajouté avec succès")

    def MepRequisSismique(self,fonctionnel,integrite,indexTableau):
        indexTableau += self.nbrTableau
        tableau = self.doc.Tables(indexTableau)
        if not fonctionnel:
            tableau.Rows(3).Delete()
        if not integrite:
            tableau.Rows(2).Delete()
        return True

    def MePWordArray(self,data, indexTableau, passage):

        AllCas = ["V1","V2","V3","V4",
                  "V10","V11","V12","V13","V14","V15","V16","V17","V18","V19",
                  "V20", "V21", "V22", "V23", "V24", "V25", "V26", "V27", "V28", "V29",
                  "V40","V41","V50","V51","V60","V61","V80","V81","V90","V91","V140","V141",
                  "C110","C120","C130","C140","C141","C150","C151","C160",
                  "C200","C220","C230","C300","C400","C500",
                  "C205","C305", "C405", "C505"]

        indexTableau += self.nbrTableau
        tableau = self.doc.Tables(indexTableau)
        boolAcc = False
        if passage == 1 or passage == 0 :
            for cas in AllCas:
                if not cas in data :
                    #Recherche de la ligne voulue
                    for i in range(0,tableau.Rows.Count):
                        Range = tableau.Cell(i+1, 1).Range
                        if cas in Range.Text:
                            #Supprimer ligne tableau
                            if cas == "V140":
                                a=1
                            self.doc.Tables(indexTableau).Rows(i+1).Delete()
                            # i-=1
                            # i=tableau.Rows.Count
                            break

                    if "V90" in data or "V91" in data:
                        boolAcc = True

        elif passage == 2:
            for cas in AllCas:
                if not cas in data :
                    #Recherche de la ligne voulue
                    for i in range(0,tableau.Rows.Count):
                        Range = tableau.Cell(i+1, 3).Range
                        if cas in Range.Text:
                            #Supprimer ligne tableau
                            self.doc.Tables(indexTableau).Rows(i+1).Delete()
                            i-=1

        if passage == 0 and boolAcc == False :
            self.supPartie("Acc_Cas_Charg_Signet")

    def ChoosePart(self,data,signetNonDDS, signetDDS):
        bool = True
        for cas in data:
            if cas == "V140" or cas == "V141":
                bool = bool & False
            else:
                bool = bool & True

        if bool == False:
            self.supPartie(signetNonDDS[0])
            self.supPartie(signetNonDDS[1])
        else:
            self.supPartie(signetDDS[0])
            self.supPartie(signetDDS[1])

    def MepAllTableau(self):
        for tableau in self.doc.Tables:
            tableau.AutoFitBehavior(2)

    def addSignet(self, signet, signetAjoute):

        rngSignet = self.doc.Bookmarks(signet).Range
        rngEnd = self.doc.Range(rngSignet.End+1,rngSignet.End+1)
        self.doc.Bookmarks.Add(signetAjoute, rngEnd)
        rngSignetAjoute = self.doc.Bookmarks(signetAjoute).Range
        rngSignetAjoute.Text = "\n"

    def stringToCell(self, range, string, color):
        '''
        ecris a un range renseigné, la chaine string de la couleur renseigné
        '''
        range.Font.ColorIndex = color
        range.Text = string

    def goToBegining(self):
        self.doc.Bookmarks("DebutNote").Select()
        self.wordApp.Selection.Delete()

        return True

    def stringToWord(self, signet, text, style):
        '''
        Ecris un texte au signet précis du style renseigné
        Si style est none le style du document est utilisé
        '''
        rng = self.doc.Bookmarks(signet).Range
        rng.Text = text
        if style is not None:
            rng.Style = style

    def supPartie(self, signet):
        '''
        Supprime une partie inutile dans la note de calcul
        '''
        self.doc.Bookmarks(signet).Select()
        self.wordApp.Selection.Delete()

    def majSommaire(self):
        '''
        Mise à jour du sommaire
        '''

        self.doc.TablesOfContents(1).Update()
        return True

    def imgToWord(self, signet, imgPath):
        '''
        Insère l' image situé au path renseigné au signet précisé
        '''
        rng = self.doc.Bookmarks(signet).Range
        pic = rng.InlineShapes.AddPicture(imgPath.replace("/","\\"))
        pic.Width = self.doc.PageSetup.PageWidth - self.doc.PageSetup.RightMargin*2
        return pic

    def save(self, option):
        '''
        sauvegarde la note final au path indiqué
        le nom du document est rensigné pour pouvoir fermé le document si il est ouvert afin d'éviter des conflits
        '''
        print("Sauvegarde du fichier" + self.nomFinalDoc + " : " +self.pathFinalDoc)
        if self.pathFinalDoc is not None and self.nomFinalDoc is not None:
            try:
                if option == 0:
                    self.doc.SaveAs(self.pathFinalDoc)
                else:
                    self.doc.Save(self.pathFinalDoc)
            except:
                import sys
                print("ERREUR : Impossible de sauvegarder la Note de calcul", file=sys.stderr)
                print(sys.exc_info())
        else:
            raise Exception("Nom de la note ou chemin final non renseigné")

    def closeDoc(self):
        if self.nomFinalDoc is not None:
            try:
                self.wordApp.Documents(self.nomFinalDoc).Close(0)
            except Exception as excep:
                print("Le document n'est pas ouvert")

    def setNomFinalDoc(self, nom):
        self.nomFinalDoc = nom

    def setPathFinalDoc(self, path):
        self.pathFinalDoc = path + '/' +self.nomFinalDoc

    def setVisible(self, bool):
        self.wordApp.Visible = bool

    def setSSText(self,displayText):
        # self.splashNoteFlex.showMessage("ECRITURE DE LA NOTE DE CALCUL\n" + displayText + " (" + str(self.state) +
        #                                 "/" + str(MAX_STATE_NOTE_FLEX) + ")", Qt.AlignBottom + Qt.AlignCenter, QColor(0,158,224))
        self.stateText.setProperty("visible", True)
        self.bar.setProperty("visible", True)

        self.stateText.setProperty("text", displayText)
        self.bar.setProperty("value", self.state/MAX_STATE_NOTE_FLEX)
        self.state += 1
        if self.state == MAX_STATE_NOTE_FLEX:
            self.bar.setProperty("value", 1)
        self.app.processEvents()

    def closeSS(self):
        # self.splashNoteFlex.finish(QWidget())
        self.stateText.setProperty("visible", False)
        self.bar.setProperty("visible", False)
        self.app.processEvents()

