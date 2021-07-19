#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject
from src.modules.components import ListView, TreeView
from src.models.tree_model import *
from src.models.list_model import *


class DbMenu():
    def __init__(self, parent):
        self.parent = parent
        self.sections = DbSection(parent)
        self.materiaux = DbMateriaux(parent)
        self.NTBSmessageDialog = "NotSavedDataManager"

    def close(self,forceClose):
        section = self.parent.findChild(QObject, self.sections.treesection.name).property("model").dataHasChanged
        materiaux = self.parent.findChild(QObject, self.materiaux.treemateriaux.name).property("model").dataHasChanged
        if not forceClose:
            if section or materiaux:
                msg = "La(es) base(s) de donnée(s) :"
                if section:
                    msg += " Sections,"
                if materiaux:
                    msg += " Matériaux,"
                msg += " n'est (ne sont) pas enregistrée(s).\nContinuer sans enregistrer ?"
                self.parent.findChild(QObject, self.NTBSmessageDialog).setProperty("text",msg)
                self.parent.findChild(QObject,self.NTBSmessageDialog).open()
                return False
        return True

    def reset(self):
        self.sections.saved = True
        self.materiaux.saved = True


class DbSection:
    def __init__(self, parent):
        self.parent = parent
        self.treesection = TreeView("treeviewSections", ProfileTreeModel([]))


class DbMateriaux:
    def __init__(self, parent):
        self.parent = parent
        self.treemateriaux = TreeView("treeviewMateriaux", MaterialTreeModel([]))