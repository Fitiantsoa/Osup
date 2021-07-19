import pyqtgraph as pg
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ViewBox(pg.ViewBox):
    """ Use to display torsor data inside the view

    There are one ViewBox object for each torsor contained in the 'displayed_torsor' attribute of the Graph Object
    """

    def __init__(self, parent, data, *args, **kwds):
        pg.ViewBox.__init__(self, *args, **kwds)
        self.parent = parent
        self.data = data
        self.text_item = None
        self.setMouseMode(self.RectMode)
        self.enableAutoRange()
        self.setMouseEnabled()
        self.create_text_item()
        self.sigRangeChanged.connect(lambda: self.update_text_item())

    def mouseClickEvent(self, ev):
        if ev.button() == Qt.RightButton:
            self.enableAutoRange()
        if ev.button() == Qt.LeftButton:
            self.hide_label()

    def show_tool_tip(self, a, b):
        s = [b[0].pos().x(), b[0].pos().y()]
        name = ""
        tors = [0, 0, 0]
        for elt in self.data.torsors:
            if s[0] == elt[1] and s[1] == elt[2]:
                name = elt[0] + ' : ( ' + str(elt[1]) + " N, " + str(elt[2]) + " N)"
                tors = [elt[0], elt[1], elt[2]]
        self.set_torsor_name(name, tors)

    def create_text_item(self):
        self.text_item = pg.TextItem("", color=(355, 355, 355), anchor=(1, 1))
        self.text_item.setFont(QFont("Times", 14))
        self.text_item.setPos(0, 0)
        self.text_item.setParentItem(self)
        self.update_text_item()

    def update_text_item(self):
        # a, b = self.text_item.parentItem().width(), self.text_item.parentItem().height()
        self.text_item.setPos(self.text_item.parentItem().width(), self.text_item.parentItem().height())

    def set_torsor_name(self, message, torsor):
        self.text_item.setText(message)
        self.parent.clear_displayed_torsor()
        self.parent.display_torsor([torsor[1]], [torsor[2]], torsor[0])
        self.update_text_item()

    def hide_label(self):
        self.text_item.setText("")
        self.parent.clear_displayed_torsor()
        self.update_text_item()
        self.update()
