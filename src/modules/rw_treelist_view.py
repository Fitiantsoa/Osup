from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal


class TreeListView(QTreeWidget):
    """List all plot to let the user choose with one to display"""

    toggle = pyqtSignal(QMouseEvent)

    def __init__(self):
        QTreeWidget.__init__(self)
        self.setColumnCount(1)
        self.setHeaderLabel(str("Choisissez les courbes à afficher :"))
        self.parent = QTreeWidgetItem(self)
        self.addTopLevelItem(self.parent)
        self.resize(284, 200)
        # self.addModel()

    def add_model(self, model):
        self.clear()
        self.expandsOnDoubleClick()
        self.parent = self.invisibleRootItem()
        self.idx = 0
        self.add_view(model, self.parent)

    def add_view(self, data, parent):
        for item in data.keys():
            if isinstance(data[item][list(data[item].keys())[0]], dict):
                new = QTreeWidgetItem()
                new.setText(0, item)
                new.setData(1, 0, data[item])
                parent.addChild(new)
                self.add_view(data[item], new)
            else:
                self.idx += 1
                print(data[item])
                new = QTreeWidgetItem()
                new.setText(0, item)
                new.setData(2, 0, data[item])
                new.setWhatsThis(0, str(self.idx))
                new.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
                new.setCheckState(0, False)
                parent.addChild(new)

    def toggle_plot_visible(self, QMouseEvent):
        """Display/Hide a plot"""
        # self.blockSignals(True)
        item = self.itemAt(QMouseEvent.pos())
        if item is not None:
            if item.childCount() == 0:
                if item.checkState(0) == 2:
                    item.setCheckState(0, Qt.Unchecked)
                else:
                    item.setCheckState(0, Qt.Checked)

            index = self.indexFromItem(item)
            if item.isExpanded():
                self.collapse(index)
            else:
                self.expand(index)

            if item.parent() is not None:
                return item.data(2, 0), item.text(0), item.parent().text(0), item.whatsThis(0), item.checkState(0)
        return None

    # def mouseReleaseEvent(self, QMouseEvent):
    #     self.blockSignals(True)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        pass

    def mousePressEvent(self, QMouseEvent):
        self.toggle.emit(QMouseEvent)
