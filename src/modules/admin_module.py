import sys
import time
import ctypes
from select import select

from som.otau_module_admin import *
from som.otau_components import *
from som.otau_admin_function import *
from PyQt5.QtCore import *
import win32com.client as win32
import win32com

class AdminMenu():
    def __init__(self, parent):
        self.parent = parent
        self.user = AdminUser(parent)
        self.machine = AdminMachine(parent)

    def appendUser(self, str1, bool, bool1, bool2,bool3):
        qml = self.parent.findChild(QObject, self.user.listeUser.name).property("model")
        qml.append(str1, bool, bool1, bool2,bool3)

    def modifyUser(self):
        qml = self.parent.findChild(QObject, self.user.listeUser.name).property("model")
        qml.modify()

    def scanUser(self, text):
        qml = self.parent.findChild(QObject, self.user.listeUser.name).property("model")
        qml.scan(text)

    def appendPC(self, str, str1):
        qml = self.parent.findChild(QObject, self.machine.listeMachine.name).property("model")
        qml.append(str, str1)

    def modifyPC(self):
        qml = self.parent.findChild(QObject, self.machine.listeMachine.name).property("model")
        qml.modify()

    def scanPC(self, text):
        qml = self.parent.findChild(QObject, self.machine.listeMachine.name).property("model")
        qml.scan(text)


