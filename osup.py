# -*- coding: utf-8 -*-
import os, sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType

from src.osup import OSup
from src.modules.console import *
from src.models.list_model import RecentFileListModel, NodeListModel, BeamListModel, PlatineListModel, StirrupListModel, FamilyListModel
from src.models.tree_model import MaterialTreeModel, ProfileTreeModel


def unhandled_exception(self, ex_cls, ex, tb):
    import traceback
    with open("log.txt", "w") as f:
        f.write(''.join(traceback.format_tb(tb)), file=sys.stderr)
        f.write('{0}: {1}'.format(ex_cls, ex), file=sys.stderr)

sys.excepthook = unhandled_exception

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('./qml/images/Otau-Icon-16x16.png'))
    #Splash Screen
    # splashPix = QPixmap("./qml/images/SplashScreen.png")
    # splash = QSplashScreen(splashPix)
    # splash.setMask(splashPix.mask())
    # splash.show()
    # splash.showMessage("OTAU version "+versionOtau+" - Verification des licences...", Qt.AlignCenter | Qt.AlignBottom, QColor(255, 255, 255))

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    qmlRegisterType(RecentFileListModel, "RecentFileListModel", 1, 0, "RecentFileListModel")
    qmlRegisterType(NodeListModel, "NodeListModel", 1, 0, "NodeListModel")
    qmlRegisterType(BeamListModel, "BeamListModel", 1, 0, "BeamListModel")
    qmlRegisterType(PlatineListModel, "PlatineListModel", 1, 0, "PlatineListModel")
    qmlRegisterType(StirrupListModel, "StirrupListModel", 1, 0, "StirrupListModel")
    qmlRegisterType(FamilyListModel, "FamilyListModel", 1, 0, "FamilyListModel")

    qmlRegisterType(MaterialTreeModel, "MaterialTreeModel", 1, 0, "MaterialTreeModel")
    qmlRegisterType(ProfileTreeModel, "ProfileTreeModel", 1, 0, "ProfileTreeModel")
    # engine.load('./qml/views/DbMenu.qml')
    engine.load('./qml/main.qml')
    win = engine.rootObjects()[0]
    # csl = MyDialog(win)
    csl = None
    osup = OSup(win, csl, app)
    ctx.setContextProperty("osup", osup)
    os._exit(app.exec())


