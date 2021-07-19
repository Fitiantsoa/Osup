from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt



class TorsorView(QWidget):
    """Allow user to add torsor inside the graphic view"""

    def __init__(self, data, pipe_axis):
        super().__init__()
        self.data = data
        self.add_button = None
        self.remove_button = None
        self.resize(284, 200)
        window_layout = QHBoxLayout()
        window_layout.addWidget(self.create_layout(pipe_axis))
        self.setLayout(window_layout)

    def create_layout(self, pipe_axis):
        groupBox = QGroupBox("Torseur")
        layout = QVBoxLayout()
        layout.addItem(self.strength_layout(pipe_axis))
        layout.addItem(self.add_buttons())
        groupBox.setLayout(layout)
        return groupBox

    def strength_layout(self, pipe_axis):
        torsLayout = QHBoxLayout()
        FyLabel = QLabel()
        FyLabel.resize(100, 40)
        if pipe_axis == "X":
            FyLabel.setText("Fy : ")
            self.torsFy = QLineEdit()
            self.torsFy.resize(50, 40)
            self.torsFy.setPlaceholderText("Fy")
            FzLabel = QLabel()
            FzLabel.resize(100, 40)
            FzLabel.setText("Fz : ")
            self.torsFz = QLineEdit()
            self.torsFz.resize(50, 40)
            self.torsFz.setPlaceholderText("Fz")
        elif pipe_axis == "Y":
            FyLabel.setText("Fx : ")
            self.torsFy = QLineEdit()
            self.torsFy.resize(50, 40)
            self.torsFy.setPlaceholderText("Fx")
            FzLabel = QLabel()
            FzLabel.resize(100, 40)
            FzLabel.setText("Fz : ")
            self.torsFz = QLineEdit()
            self.torsFz.resize(50, 40)
            self.torsFz.setPlaceholderText("Fz")
        else:
            FyLabel.setText("Fx : ")
            self.torsFy = QLineEdit()
            self.torsFy.resize(50, 40)
            self.torsFy.setPlaceholderText("Fx")
            FzLabel = QLabel()
            FzLabel.resize(100, 40)
            FzLabel.setText("Fy : ")
            self.torsFz = QLineEdit()
            self.torsFz.resize(50, 40)
            self.torsFz.setPlaceholderText("Fy")
        torsLayout.addWidget(FyLabel, 1, Qt.AlignCenter)
        torsLayout.addWidget(self.torsFy, 2, Qt.AlignCenter)
        torsLayout.addWidget(FzLabel, 3, Qt.AlignCenter)
        torsLayout.addWidget(self.torsFz, 4, Qt.AlignCenter)
        return torsLayout

    def add_buttons(self):
        # add_button and remove_button are connected in the ResultView object
        name_layout = QHBoxLayout()
        name_label = QLabel()
        name_label.resize(100, 40)
        name_label.setText("Nom : ")
        self.name = QLineEdit()
        self.name.resize(50, 40)
        self.name.setPlaceholderText("Nom")
        self.add_button = QPushButton()
        self.add_button.setText("Ajouter")
        self.remove_button = QPushButton()
        self.remove_button.setText("Enlever")
        name_layout.addWidget(name_label, alignment=Qt.AlignCenter)
        name_layout.addWidget(self.name, alignment=Qt.AlignCenter)
        name_layout.addWidget(self.add_button, alignment=Qt.AlignCenter)
        name_layout.addWidget(self.remove_button, alignment=Qt.AlignCenter)
        return name_layout

    def get_data(self):
        exist = self.data.torsor_exist(self.name.text())
        return self.torsFy.text(), self.torsFz.text(), self.name.text(), not exist
