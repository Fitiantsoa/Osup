import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QToolBar, QAction, QGroupBox, QGridLayout, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from src.utils import lerp
from src.modules.plots_data import Data
from src.modules.rw_graph import Graph
from src.modules.rw_treelist_view import TreeListView
from src.modules.rw_result_table import TableView
from src.modules.rw_export_result import ExportResult
from src.constantes import *
from src.modules.rw_data_view import DataView
from src.modules.rw_torsor_view import TorsorView
from src.modules.rw_error import Error
from tkinter import *
from tkinter import messagebox
from src.Version5etag.general import General

class ResultWindowSofix(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Affichage des résultats Ancrages"
        self.result_table_view_chev = TableView("cheville")

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setWindowFlags(Qt.WindowFullscreenButtonHint)
        self.create_menu_bar()
        self.create_grid_layout()
        window_layout = QVBoxLayout()
        window_layout.setMenuBar(self.status)
        window_layout.addWidget(self.horizontal_group_box)
        self.setLayout(window_layout)
        color = self.palette()
        color.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(color)
        self.setMinimumHeight(500)
        self.setMinimumWidth(900)

    def create_grid_layout(self):
        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)
        layout.addWidget(self.graph.plot_widget, 0, 0, 2, 1)
        layout.addWidget(self.tree_view, 0, 1)
        title = QLabel()
        title.setText("Résultat Sofix")
        layout.addWidget(title, 1, 0)
        layout.addWidget(self.result_table_view_chev, 2, 0)