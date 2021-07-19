# import logging
# import sys
#
# from PyQt5.QtCore import QObject, pyqtSignal, Qt
# from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextBrowser
# from PyQt5.QtGui import QPalette, QTextCursor
#
# logger = logging.getLogger(__name__)
#
#
# class XStream(QObject):
#     _stdout = None
#     _stderr = None
#     messageWritten = pyqtSignal(str, str)
#
#     def flush(self):
#         pass
#
#     def fileno(self):
#         return -1
#
#     def write(self, msg):
#         if not self.signalsBlocked():
#             if msg != '\n' and msg != ' ':
#                 if self == self._stderr:
#                     self.messageWritten.emit(msg, "error")
#                 else:
#                     self.messageWritten.emit(msg, "out")
#
#     @staticmethod
#     def stdout():
#         if not XStream._stdout:
#             XStream._stdout = XStream()
#             sys.stdout = XStream._stdout
#         return XStream._stdout
#
#     @staticmethod
#     def stderr():
#         if not XStream._stderr:
#             XStream._stderr = XStream()
#             sys.stderr = XStream._stderr
#         return XStream._stderr
#
#
# class MyDialog(QDialog):
#     def __init__(self, win):
#         super(MyDialog, self).__init__()
#         self.win = win
#         # setup the ui
#         self._console = QTextBrowser(self)
#         pal = QPalette()
#         pal.setColor(QPalette.Base, Qt.black)
#         self._console.setPalette(pal)
#
#         # create the layout
#         layout = QVBoxLayout()
#         layout.addWidget(self._console)
#         self.setFixedHeight(400)
#         self.setFixedWidth(800)
#         self.setWindowTitle("Log OSup")
#         self.setLayout(layout)
#
#         # create connections
#         XStream.stdout().messageWritten.connect(self.print_log)
#         XStream.stderr().messageWritten.connect(self.print_log)
#
#         open("file.log", "w")
#
#     def print_log(self, message, stream):
#         self._console.moveCursor(QTextCursor.End)
#         if stream == "error":
#             if not self.isVisible():
#                 self.win.findChild(QObject, "displayConsole").setProperty("errorEdited", True)
#             self._console.insertHtml('<p style="color:#FF0000">' + message + "<br /></p>")
#         else:
#             self._console.insertHtml('<p style="color:#FFFFFF">' + message + "<br /></p>")
#
#         with open("file.log", "a") as f:
#             try:
#                 if stream == "error":
#                     f.write("ERROR : " + message + "\n")
#                 else:
#                     f.write("INFO : " + message + "\n")
#             except UnicodeEncodeError:
#                 pass
