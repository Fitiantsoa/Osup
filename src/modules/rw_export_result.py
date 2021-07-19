from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtCore import Qt


class ExportResult(QWidget):

    def __init__(self):
        super().__init__()
        self.name = None
        self.export_button = None
        self.resize(284, 200)
        window_layout = QHBoxLayout()
        window_layout.addWidget(self.create_layout())
        self.setLayout(window_layout)

    def create_layout(self):
        groupBox = QGroupBox("Exporter les résultats")
        layout = QVBoxLayout()
        layout.addItem(self.export_buttons())
        groupBox.setLayout(layout)
        return groupBox


    def export_buttons(self):
        # add_button and remove_button are connected in the ResultView object
        name_layout = QHBoxLayout()
        name_label = QLabel()
        name_label.setText("Nom courbe: ")
        self.name = QLineEdit()
        name_label.resize(100, 40)
        self.export_button = QPushButton()
        self.export_button.setText("Exporter")
        name_layout.addWidget(name_label, alignment=Qt.AlignCenter)
        name_layout.addWidget(self.name, alignment=Qt.AlignCenter)
        name_layout.addWidget(self.export_button, alignment=Qt.AlignCenter)
        return name_layout

    def get_data(self):
        return self.name.text()

    def export(self):
        options = QFileDialog()
        options.setDefaultSuffix(".rosup")
        options.setWindowFilePath("Osup")
        file = options.getSaveFileName(filter="All Files (*);;OSUP (*.rosup)")
        return file
