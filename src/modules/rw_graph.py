import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QFileDialog
from src.modules.rw_viewbox import ViewBox
from PyQt5.QtGui import QColor


class Graph:

    def __init__(self, data, pipe_axis):
        self.data = data
        self.view_box = ViewBox(self, data)
        self.plot_widget = pg.PlotWidget(viewBox=self.view_box, enableMenu=True, title="Graphique", background='w')
        # self.plot_widget.sceneObj.sigMouseMoved.connect(self.view_box.mouseMoved)
        self.plot_item = pg.ScatterPlotItem()
        self.displayed_torsor = pg.ScatterPlotItem()
        self.curve_item = pg.ScatterPlotItem()
        self.green_torsor = pg.ScatterPlotItem()
        self.plot_item.sigClicked.connect(self.view_box.show_tool_tip)
        self.green_torsor.sigClicked.connect(self.view_box.show_tool_tip)
        self.curve_item.sigClicked.connect(self.view_box.show_tool_tip)
        self.plot_widget.addItem(self.plot_item)
        self.plot_widget.addItem(self.green_torsor)
        self.plot_widget.addItem(self.displayed_torsor)
        self.plot_widget.addItem(self.curve_item)
        self.lg = self.plot_widget.addLegend(offset=(30, -30), )
        self.point_id = 0
        if pipe_axis == "X":
            self.plot_widget.setLabel(axis='bottom', text="Fy", units='N')
            self.plot_widget.setLabel(axis='left', text="Fz", units='N')
        elif pipe_axis == "Y":
            self.plot_widget.setLabel(axis='bottom', text="Fx", units='N')
            self.plot_widget.setLabel(axis='left', text="Fz", units='N')
        else:
            self.plot_widget.setLabel(axis='bottom', text="Fx", units='N')
            self.plot_widget.setLabel(axis='left', text="Fy", units='N')

        self.plot_widget.setMenuEnabled()
        self.plot_widget.showGrid(True, True, 1)
        self.torsor_visible = True

    def add_plot(self, dataX, dataY, color, name, point_color=QColor("black")):
        color = pg.intColor(color, hues=10, values=1, maxValue=255, minValue=5, maxHue=360, minHue=0, sat=255, alpha=255)
        pen = pg.mkPen(color, width=3)
        self.point_id = 0
        # for i in range(len(dataX)):
        #     self.add_curve_item([dataX[i]], [dataY[i]], name, pen)
        self.plot_widget.plot(x=dataX, y=dataY, symbol='o', symbolSize=6, symbolPen=point_color, pen=pen, name=name)
        a=1
        # self.lg.addItem(item)

    def add_curve_item(self,fy, fz,name,pen):
        self.point_id +=1
        name = name + str(self.point_id)
        self.curve_item.addPoints(fy, fz,name=name,pen=pen)
        self.curve_item.getData()

    def add_torsor(self, fy, fz, name, nbObj):
        if nbObj > 0:
            pen = pg.mkPen("r", width=3)
            self.plot_item.addPoints(fy, fz, name=name, pen=pen)
            self.plot_item.getData()
        elif nbObj == 0:
            pen = pg.mkPen("g", width=3)
            self.green_torsor.addPoints(fy, fz, name=name, pen=pen)
            self.green_torsor.getData()

    def remove_plot(self, itemToRemove, parent):
        item = self.plot_widget.getPlotItem().items
        for elt in item:
            name = elt.name()
            try:
                if itemToRemove in name and parent in name:
                    self.plot_widget.removeItem(elt)
                    self.lg.removeItem(name)
            except:
                continue

    def new_file(self):
        self.clear()
        self.plot_item.clear()
        self.green_torsor.clear()
        self.displayed_torsor.clear()

    def display_torsor(self, fy, fz, name):
        pen = pg.mkPen("b", width=3)
        self.displayed_torsor.addPoints(fy, fz, name=name, pen=pen)

    def clear_displayed_torsor(self):
        self.displayed_torsor.clear()

    def remove_torsor(self):
        self.plot_item.clear()
        self.green_torsor.clear()

    def clear(self):
        item = self.plot_widget.getPlotItem().items
        for elt in item:
            name = elt.name()
            try:
                self.lg.removeItem(name)
            except:
                continue
        self.plot_widget.clear()
        self.plot_widget.addItem(self.plot_item)
        self.plot_widget.addItem(self.green_torsor)
        self.plot_widget.addItem(self.displayed_torsor)
        self.torsor_visible = True

    def export(self):
        options = QFileDialog()
        options.setDefaultSuffix(".jpg")
        options.setWindowFilePath("Osup")
        file = options.getSaveFileName(filter="All Files (*);;JPG (*.jpg)")
        return file

    def hide_torsor_items(self):
        self.plot_widget.removeItem(self.plot_item)
        self.plot_widget.removeItem(self.green_torsor)
        self.plot_widget.removeItem(self.displayed_torsor)
        self.view_box.hide_label()
        self.torsor_visible = False

    def display_torsor_items(self):
        self.plot_widget.addItem(self.plot_item)
        self.plot_widget.addItem(self.green_torsor)
        self.plot_widget.addItem(self.displayed_torsor)
        self.view_box.hide_label()
        self.torsor_visible = True

    def update(self):
        self.view_box.update()