import win32com.client as win32
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
from src.constantes import *
from os import listdir
from os.path import isfile, join
#from som.file_read_fun import checkImg
from win32com.client import constants as c

class Note():
    def __init__(self, tempPath, nameFinalDoc=None, pathFinalDoc=None):
        self.nbrTableau = 0
        self.wordApp = win32.gencache.EnsureDispatch('Word.Application')
        self.constant = win32.constants
        self.wordApp.Visible = False

        self.state = 0
        self.doc = self.wordApp.Documents.Open(PATH_TEMPLATE_NOTE_RCCM)
        self.pathFinalDoc = pathFinalDoc
        self.nomFinalDoc = nameFinalDoc

        self.path = None

    def parseModelToWord(self, indexTableau, listData, img=True):
        indexTableau += self.nbrTableau
        tab = self.doc.Tables(indexTableau)
        title = tab.Cell(1, 1).Range.Text
        for elt in listData:
            self.stringToCell(tab.Cell(elt[0], elt[1]).Range, elt[2], "Référence intense")
        if img:
            self.stringToCell(tab.Cell(listData[0][0], listData[0][1]).Range, "", None)
            self.imgToCell(tab.Cell(1, 1).Range,listData[0][2], listData[0][3] )

    def modelsToWord(self, signet, data, indexTableau, title=None):
        tpSignet = signet
        for i in range(0, len(data)):
            if len(data[i]):
                self.addSignet(tpSignet,"subModel{}".format(i))
                tpSignet = "subModel{}".format(i)

        for i,sub in enumerate(data):
            if len(sub):
                title[0][0] = (title[0][0][0], sub[0]["Famille"])
                for lig in sub:
                    lig.pop("Famille")
                self.modelToWord("subModel{}".format(i),sub,indexTableau, title=title)
        for i in range(0, len(data)):
            if len(data[i]):
                self.doc.Bookmarks("subModel{}".format(i)).Delete()
        self.stringToWord(signet, "", None)

    def modelToWord(self,signet, data, indexTableau, title=None, col=1, isModaleTab=False):

        '''
        Fonction qui va écrire un tableau des data au signet précis.
        data doit etre impérativement une liste de dictionnaire
        Les dictionnaires doivent avoir les memes clés
        L'entete du tableau sera les clés du dictionnaire data
        Le style du tableau est Otau_Style_Table
        '''
        print(data)
        listIdx = []
        rng = self.doc.Bookmarks(signet).Range
        keys = list(data[0].keys())

        if title is None:
            title = keys
        nbrCol = len(keys)
        titleSize = 1
        if isinstance(title[0], list):
            titleSize += 1
        nbrLig = len(data) + titleSize
        indexTableau += self.nbrTableau

        tab = self.doc.Tables.Add(rng, NumRows=nbrLig, NumColumns=nbrCol)

        # title = self.doc.Tables(indexTableau).Cell(1,1).Range.Text
        # title = self.doc.Tables(indexTableau+1).Cell(1, 1).Range.Text
        # title1 = self.doc.Tables(indexTableau+2).Cell(1, 1).Range.Text
        tit = self.doc.Tables(indexTableau).Cell(1, 1).Range.Text
        print(tit)
        if isinstance(title[0], list):
            idx = 0
            for tt in title[0]:
                if isinstance(tt, str):
                    self.stringToCell(tab.Cell(1, idx + 1).Range, tt, 1)
                    idx += 1
                else:
                    self.doc.Tables(indexTableau).Cell(1, idx + 1).Merge(MergeTo=self.doc.Tables(indexTableau).Cell(1, idx + tt[0] ))
                    self.stringToCell(self.doc.Tables(indexTableau).Cell(1, idx + 1).Range, tt[1], 1)
                    idx += 1
            idx = 1
            dif = 0
            detectMerge = False
            for tit in title[1]:
                if isinstance(tit, str):
                    if tit in title[0]:
                        if detectMerge:
                            dif -= 1
                            detectMerge = False
                        self.doc.Tables(indexTableau).Cell(1, idx - dif).Merge(MergeTo=self.doc.Tables(indexTableau).Cell(2, idx))
                    else:
                        self.stringToCell(self.doc.Tables(indexTableau).Cell(2, idx).Range, tit, 1)
                        listIdx.append((2, idx))
                        detectMerge = True
                        dif += 1
                idx += 1
        else:
            for i in range(0, nbrCol):
                self.stringToCell(self.doc.Tables(indexTableau).Cell(1, i+1).Range,title[i],1)
        for i in range(0, nbrLig - titleSize):
            # self.stringToCell(self.doc.Tables(indexTableau).Cell(i+titleSize+1, 1).Range, str(i+1), 1)
            for j in range(1, nbrCol+1):
                self.stringToCell(self.doc.Tables(indexTableau).Cell(i+titleSize+1, j).Range, data[i][keys[j-1]][0], data[i][keys[j-1]][1])



        # self.doc.Tables(indexTableau).AutoFitBehavior(self.constant.wdAutoFitContent)


        if isModaleTab:
            self.doc.Tables(indexTableau).Columns(1).Delete()
        try:
            self.doc.Tables(indexTableau).Rows.SetHeight(17)
            # time.sleep(0.5)
        except:
            pass

        # self.MepWordTable(self.doc.Tables(indexTableau), titleSize, nbrLig, col)
        self.MepTableau(self.doc.Tables(indexTableau))
        self.doc.Tables(indexTableau).Style = self.doc.Styles("OSup")
        for i, j in listIdx:
            self.doc.Tables(indexTableau).Cell(i, j).Shading.BackgroundPatternColor = 15773696
            self.doc.Tables(indexTableau).Cell(i, j).Range.Font.Bold = True

        self.doc.Tables(indexTableau).AutoFitBehavior(1)
        self.doc.Tables(indexTableau).AutoFitBehavior(2)
        self.doc.Tables(indexTableau).PreferredWidthType = self.constant.wdPreferredWidthPercent
        time.sleep(0.5)
        self.doc.Tables(indexTableau).PreferredWidth = 100
        time.sleep(0.5)
        self.doc.Tables(indexTableau).PreferredWidthType = self.constant.wdPreferredWidthPoints
        time.sleep(0.5)
        try:
            if not isModaleTab:
                self.doc.Tables(indexTableau).Columns(1).SetWidth(19)
                time.sleep(0.5)
        except:
            pass
        self.doc.Tables(indexTableau).Rows.Alignment = self.constant.wdAlignRowCenter
        self.nbrTableau += 1
        print("Tableau "+signet+" ajouté avec succès")

    def modelToWordTabSec(self, signet, data, indexTableau, col=1, isModaleTab=False):
        """
        Fonction qui va écrire un tableau des data au signet précis.
        data doit etre impérativement une liste de dictionnaire
        Les dictionnaires doivent avoir les memes clés
        L'entete du tableau sera les clés du dictionnaire data
        Le style du tableau est Otau_Style_Table
        """
        title = ["Family", "Support Name", "Sections"]
        print(data)
        listIdx = []
        rng = self.doc.Bookmarks(signet).Range

        nbrCol = data["Section Max"]
        titleSize = 1
        if isinstance(title[0], list):
            titleSize += 1
        nbrLig = 0
        for famille in data:
            if famille != "Section Max":
                 nbrLig += len(data[famille]["Support Name"])

        indexTableau += self.nbrTableau
        self.doc.Tables.Add(rng, NumRows=nbrLig, NumColumns=nbrCol)
        # title = self.doc.Tables(indexTableau).Cell(1,1).Range.Text
        # title = self.doc.Tables(indexTableau+1).Cell(1, 1).Range.Text
        # title1 = self.doc.Tables(indexTableau+2).Cell(1, 1).Range.Text
        if isinstance(title[0], list):
            idx = 0
            self.stringToCell(self.doc.Tables(indexTableau).Cell(1, 1).Range, "N", 1)
            for tt in title[0]:
                if isinstance(tt, str):
                    self.stringToCell(self.doc.Tables(indexTableau).Cell(1, idx + 2).Range, tt, 1)
                    idx += 1
                else:
                    self.doc.Tables(indexTableau).Cell(1, idx + 2).Merge(MergeTo=self.doc.Tables(indexTableau).Cell(1, idx + tt[0] + 1))
                    self.stringToCell(self.doc.Tables(indexTableau).Cell(1, idx + 2).Range, tt[1], 1)
                    idx += 1
            idx = 0
            dif = 0
            detectMerge = False
            self.doc.Tables(indexTableau).Cell(1, 1).Merge(MergeTo=self.doc.Tables(indexTableau).Cell(2, 1))
            for tit in title[1]:
                if isinstance(tit, str):
                    if tit in title[0]:
                        if detectMerge:
                            dif -= 1
                            detectMerge = False
                        self.doc.Tables(indexTableau).Cell(1, idx - dif + 2).Merge(MergeTo=self.doc.Tables(indexTableau).Cell(2, idx + 2))
                    else:
                        self.stringToCell(self.doc.Tables(indexTableau).Cell(2, idx + 2).Range, tit, 1)
                        listIdx.append((2, idx+2))
                        detectMerge = True
                        dif += 1
                idx += 1
        else:
            self.stringToCell(self.doc.Tables(indexTableau).Cell(1, 1).Range, "N", 1)
            for i in range(0, nbrCol-1):
                self.stringToCell(self.doc.Tables(indexTableau).Cell(1, i+2).Range,title[i],1)
        for i in range(0, nbrLig - titleSize):
            self.stringToCell(self.doc.Tables(indexTableau).Cell(i+titleSize+1, 1).Range, str(i+1), 1)
            for j in range(1, nbrCol):
                self.stringToCell(self.doc.Tables(indexTableau).Cell(i+titleSize+1, j + 1).Range, data[i][title[j-1]][0], data[i][title[j-1]][1])


        # self.doc.Tables(indexTableau).AutoFitBehavior(self.constant.wdAutoFitContent)


        if isModaleTab:
            self.doc.Tables(indexTableau).Columns(1).Delete()
        try:
            self.doc.Tables(indexTableau).Rows.SetHeight(17)
            # time.sleep(0.5)
        except:
            pass

        self.MepWordTable(self.doc.Tables(indexTableau), titleSize, nbrLig, col)
        self.MepTableau(self.doc.Tables(indexTableau))
        self.doc.Tables(indexTableau).Style = self.doc.Styles("BOP")
        for i, j in listIdx:
            self.doc.Tables(indexTableau).Cell(i, j).Shading.BackgroundPatternColor = 15259856
            self.doc.Tables(indexTableau).Cell(i, j).Range.Font.Bold = True

        self.doc.Tables(indexTableau).AutoFitBehavior(1)
        self.doc.Tables(indexTableau).AutoFitBehavior(2)
        self.doc.Tables(indexTableau).PreferredWidthType = self.constant.wdPreferredWidthPercent
        time.sleep(0.5)
        self.doc.Tables(indexTableau).PreferredWidth = 100
        time.sleep(0.5)
        self.doc.Tables(indexTableau).PreferredWidthType = self.constant.wdPreferredWidthPoints
        time.sleep(0.5)
        try:
            if not isModaleTab:
                self.doc.Tables(indexTableau).Columns(1).SetWidth(19)
                time.sleep(0.5)
        except:
            pass
        self.doc.Tables(indexTableau).Rows.Alignment = self.constant.wdAlignRowCenter
        self.nbrTableau += 1
        print("Tableau "+signet+" ajouté avec succès")

    def MepWordTable(self, table, ttlen, nbrLig, nbrCol):
        for col in range(1, nbrCol+1):
            idx = ttlen + 1
            ln = ttlen + 1
            nbIden = 0
            n = 1
            while ln < nbrLig:
                if table.Cell(idx, col).Range.Text == table.Cell(idx + nbIden + 1, col).Range.Text:
                    table.Cell(idx + nbIden + 1, col).Range.Text = ""
                    if col == 2:
                        table.Cell(idx + nbIden + 1, 1).Range.Text = ""
                    nbIden += 1
                else:
                    if nbIden !=0:
                        table.Cell(idx, col).Merge(MergeTo=table.Cell(idx + nbIden, col))
                    idx += nbIden + 1
                    nbIden = 0
                ln +=1
            if nbIden != 0:
                if col == 2:
                    table.Cell(idx, 1).Range.Text = str(n)
                    table.Cell(idx, 1).Merge(MergeTo=table.Cell(idx + nbIden, 1))
                    n += 1
                table.Cell(idx, col).Merge(MergeTo=table.Cell(idx + nbIden, col))


    def MepRequisSismique(self, fonctionnel, integrite, indexTableau):
        indexTableau += self.nbrTableau
        tableau = self.doc.Tables(indexTableau)
        if not fonctionnel:
            tableau.Rows(3).Delete()
        if not integrite:
            tableau.Rows(2).Delete()
        return True


    def MePWordArray(self, data, indexTableau, passage):
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

    def MepTableau(self, tableau):
        col = tableau.Columns.Count
        try:
            for i in range(0, col):
                if "|" in tableau.Cell(1, i+1).Range.Text:
                    tp = tableau.Cell(1, i+1).Range.Text
                    rpos = tp.rfind("|")
                    lpos = tp.find("|") + 1
                    tp = tp.replace("|", "")
                    tableau.Cell(1, i + 1).Range.Text = tp[:-2]
                    time.sleep(0.5)
                    # tableau.Cell(1, i + 1).Range.Font.Bold = True
                    for j in range(lpos, rpos):
                        tableau.Cell(1, i + 1).Range.Characters(j).Font.Subscript = self.constant.wdToggle
                    time.sleep(0.5)
        except:
            pass

    def addSignet(self, signet, signetAjoute):

        rngSignet = self.doc.Bookmarks(signet).Range
        rngEnd = self.doc.Range(rngSignet.End+1,rngSignet.End+1)
        self.doc.Bookmarks.Add(signetAjoute, rngEnd)
        rngSignetAjoute = self.doc.Bookmarks(signetAjoute).Range
        rngSignetAjoute.Text = "\n"

    def copyPasteBookMarks(self, signetTab, signet):
        self.doc.Bookmarks(signetTab).Range.Copy()
        rngSignet = self.doc.Bookmarks(signet).Range
        rngSignet.Paste()
        return

    def copyPastePicture(self,signetTab, signet):
        self.doc.Shapes.Range("Annexes").Select()
        self.wordApp.Selection.Copy()
        rngSignet = self.doc.Bookmarks(signet).Range
        rngSignet.PasteAndFormat(c.wdPasteDefault)

    def stringToCell(self, range, string, style=None):
        '''
        ecris a un range renseigné, la chaine string de la couleur renseigné
        '''

        range.Font.ColorIndex = 1
        range.Text = string

        if style is not None:
            if isinstance(style, int):
                range.Font.ColorIndex = style
            else:
                range.Style = style

        range.ParagraphFormat.Alignment = self.constant.wdAlignParagraphCenter

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

    def supPartie(self,signet):
        '''
        Supprime une partie inutile dans la note de calcul
        '''
        SUPLIST = ["P_3_4_COUDE", "P_3_4_MAT_FLUID", "P_3_6_2_REDUCERS", "P_3_6_2_TEES", "P_3_7_SPECTRE"]
        if signet not in SUPLIST:
            self.stringToWord(signet, "Not applicable", "Not applicable")
        else:
            self.delSignet(signet)

    def majSommaire(self):
        '''
        Mise à jour du sommaire
        '''

        self.doc.TablesOfContents(1).Update()
        return True
    '''
    def imgFolderToWord(self, signet, pathToFolder):
        listFile = [f for f in listdir(pathToFolder) if isfile(join(pathToFolder, f))]
        for i, file in enumerate(listFile):
            #if checkImg(join(pathToFolder, file)):
                self.addSignet(signet, "annexeImg{}".format(str(i)))
                self.imgToWord("annexeImg{}".format(str(i)), join(pathToFolder, file))
    '''
    '''
    def addGraph(self, signet, data):
        rng = self.doc.Bookmarks(signet).Range
        ch = self.doc.InlineShapes.AddChart(74, rng)
        chart = ch.Chart
        excl = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excl.ActiveWorkbook
        ws = wb.Worksheets("Feuil1")
        for i, elt in enumerate(data):
            for j,elem in enumerate(elt):
                ws.Cells(2+i,1+j).Value = elem
        excl.Quit()
        a=1
    '''
    def  imgsToWord(self, signet, data):
        tpSignet = signet
        for famille in list(data.keys()):
            self.addSignet(tpSignet,"Titre{}".format(famille))
            tpSignet = "Titre{}".format(famille)
            self.addSignet(tpSignet, "phrase{}".format(famille))
            tpSignet = "phrase{}".format(famille)
            self.addSignet(tpSignet, "sousTitre{}".format(famille))
            tpSignet = "sousTitre{}".format(famille)
            self.addSignet(tpSignet, "imgvue{}".format(famille))
            tpSignet = "imgvue{}".format(famille)
            self.addSignet(tpSignet, "sautPage1{}".format(famille))
            tpSignet = "sautPage1{}".format(famille)
            self.addSignet(tpSignet, "sousTitre2{}".format(famille))
            tpSignet = "sousTitre2{}".format(famille)
            self.addSignet(tpSignet, "imgresult{}".format(famille))
            tpSignet = "imgresult{}".format(famille)
            self.addSignet(tpSignet, "sautPage2{}".format(famille))
            tpSignet = "sautPage2{}".format(famille)

        for famille in list(data.keys()):
            self.stringToWord("Titre{}".format(famille), "CALCULATION "+famille.replace("Famille", "Family "), "T2")
            self.stringToWord("phrase{}".format(famille), "This calculation family is modelled using ANSYS software. The results are detailed hereafter:\n", "Corps de Texte")
            self.stringToWord("sousTitre{}".format(famille),"3D finite element model:", "Style1")
            self.imgToWord("imgvue{}".format(famille), data[famille][1], True)
            self.stringToWord("sautPage1{}".format(famille), "\f", None)
            self.stringToWord("sousTitre2{}".format(famille), "Calculation results:", "Style1")
            self.imgToWord("imgresult{}".format(famille), data[famille][0], False)
            self.stringToWord("sautPage2{}".format(famille), "", None)
            print("CALCULATION "+famille+ " ajouté avec succès")

        for famille in list(data.keys()):
            self.doc.Bookmarks("Titre{}".format(famille)).Delete()
            self.doc.Bookmarks("phrase{}".format(famille)).Delete()
            self.doc.Bookmarks("sousTitre{}".format(famille)).Delete()
            self.doc.Bookmarks("imgvue{}".format(famille)).Delete()
            self.doc.Bookmarks("sautPage1{}".format(famille)).Delete()
            self.doc.Bookmarks("sousTitre2{}".format(famille)).Delete()
            self.doc.Bookmarks("imgresult{}".format(famille)).Delete()
            self.doc.Bookmarks("sautPage2{}".format(famille)).Delete()
        self.stringToWord(signet, "", None)

    def imgToWord(self, signet, imgPath, view):
        '''
        Insère l' image situé au path renseigné au signet précisé
        '''
        rng = self.doc.Bookmarks(signet).Range
        pic = rng.InlineShapes.AddPicture(imgPath.replace("/","\\"))
        t = pic.Height
        if not view:
            pic.Height = pic.Height - 100
        return pic


    def imgToCell(self, range, imgPath,rotation=0, width=100):
        pic = range.InlineShapes.AddPicture(imgPath.replace("/", "\\"))
        pic.Width = width
        pic.Height = width

        return pic

    def save(self, option):
        '''
        sauvegarde la note final au path indiqué
        le nom du document est rensigné pour pouvoir fermé le document si il est ouvert afin d'éviter des conflits
        '''
        print("Sauvegarde du fichier" + self.nomFinalDoc + " : " + self.pathFinalDoc)
        if self.pathFinalDoc is not None and self.nomFinalDoc is not None:
            try:
                if option == 0:
                    a = self.pathFinalDoc.replace("/", "\\")
                    self.doc.SaveAs(a)
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

    def setPathFinalDoc(self, path, name):
        self.pathFinalDoc = path.replace("Support", name) + '/' +self.nomFinalDoc.replace("Support", "_")

    def setVisible(self, bool):
        self.wordApp.Visible = bool

    def setSSText(self,displayText):
        self.splashNoteFlex.showMessage("ECRITURE DE LA NOTE DE CALCUL\n" + displayText + " (" + str(self.state) +
                                        "/" + str(MAX_STATE_NOTE_FLEX) + ")", Qt.AlignBottom + Qt.AlignCenter, QColor(0,158,224))
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

    def delSignet(self, signet):
        self.doc.Bookmarks(signet).Select()
        self.wordApp.Selection.Delete()

