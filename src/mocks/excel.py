import sys

from PyQt5.QtCore import *
import win32com.client as win32
from win32com.client import constants as c


class ExcelDE():

    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.caseList = []
        self.appNode = 0

    def fillExcel(self, FyMax, FyMin, FzMax, FzMin, pasY, pasZ, noeud, file):
        xl = win32.gencache.EnsureDispatch('Excel.Application')
        wb = xl.Workbooks.Open(file)
        ws = wb.Worksheets(3)
        index = 1
        noeud = list(filter(('').__ne__, noeud.split(' ')))
        for nd in noeud:
            for i in range(FyMin, FyMax + 1, pasY):
                for j in range(FzMin, FzMax + 1, pasZ):
                    index += 1
                    ws.Cells(index, 1).Value = index - 1
                    ws.Cells(index, 2).Value = index - 1
                    ws.Cells(index, 3).Value = "Nodal"
                    ws.Cells(index, 4).Value = nd
                    ws.Cells(index, 5).Value = 0
                    ws.Cells(index, 6).Value = i
                    ws.Cells(index, 7).Value = j
                    ws.Cells(index, 8).Value = 0
                    ws.Cells(index, 9).Value = 0
                    ws.Cells(index, 10).Value = 0
                    ws.Cells(index, 11).Value = "0AB"
        file = file.replace('file:///', '')
        wb.Save()
        wb.Close()
        xl.Quit()
        print("Excel is Ok")
        # liste = []
        # for i in range(FyMin, FyMax + 1, pasY):
        #     for j in range(FzMin, FzMax + 1, pasZ):
        #         liste.append([i, j])
    #     passer a calcul etrier
    #     for elt in liste:
    #         b.append(i+j)

    def readExcel(self, file):
        xl = win32.gencache.EnsureDispatch('Excel.Application')
        wb = xl.Workbooks.Open(file)
        ws = wb.Worksheets(1)
        index = 1
        caseList = []
        while True:
            index += 1
            if ws.Cells(index, 3).Value is None:
                break
            Cas = int(ws.Cells(index, 3).Value)
            try:
                if ws.Cells(index, 3).Value not in caseList[Cas - 1]:
                    caseList.append([Cas, []])
            except:
                caseList.append([Cas, []])
            Rate = float(ws.Cells(index, 18).Value)
            caseList[Cas - 1][1].append(Rate)
        tempdict = []
        for elt in caseList:
            elt[1].sort(reverse=True)
            if 0.96 <= elt[1][0] <= 1:
                tempdict.append(elt[0])
        self.caseList = tempdict
        print(self.caseList)


    def linkCase(self, dataFile):
        xl = win32.gencache.EnsureDispatch('Excel.Application')
        wb = xl.Workbooks.Open(dataFile)
        ws = wb.Worksheets(3)
        coupleList = []
        row = 2
        while ws.Cells(row, 1).Value != None:
            try:
                if ws.Cells(row, 1).Value in self.caseList:
                    coupleList.append([ws.Cells(row, 6).Value, ws.Cells(row, 7).Value])
                row += 1
                if row % 1000 == 0:
                    print(row)
            except TypeError:
                print(row)
        print(coupleList)
        self.toExcel(coupleList)


    def toExcel(self, coupleList):
        xl = win32.gencache.EnsureDispatch('Excel.Application')
        wb = xl.Workbooks.Add()
        ws = wb.Worksheets("Feuil1")
        for i,elt in enumerate(coupleList):
            ws.Cells(i+1, 1).Value = elt[0]
            ws.Cells(i + 1, 2).Value = elt[1]

