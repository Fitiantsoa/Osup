from PyQt5.QtWidgets import QWidget, QGroupBox, QGridLayout, QHBoxLayout, QRadioButton, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt


class DataView(QWidget):
    """Used to let the user choose what ratio value he wanted to display"""

    def __init__(self):
        super().__init__()
        self.resize(284, 200)
        window_layout = QHBoxLayout()
        window_layout.addWidget(self.create_layout())
        self.setLayout(window_layout)

    def create_layout(self):
        group_box = QGroupBox("Configuration")
        layout = QGridLayout()
        layout.addItem(self.rate_layout(), 0, 0)
        layout.addItem(self.double_rate_layout(), 1, 0)
        layout.addItem(self.precision_layout(), 2, 0)
        layout.addWidget(self.update_button(), 3, 0)
        group_box.setLayout(layout)
        return group_box

    def rate_layout(self):
        rate_layout = QHBoxLayout()
        self.cb1 = QRadioButton("")
        self.cb1.resize(100, 30)
        self.cb1.setChecked(True)
        rateLabel = QLabel()
        rateLabel.resize(100, 40)
        rateLabel.setText("Ratio : ")
        self.rateTF = QLineEdit()
        self.rateTF.resize(50, 40)
        self.rateTF.setPlaceholderText("Ratio")
        self.rateTF.setText("1")
        rate_layout.addWidget(self.cb1, 0, Qt.AlignCenter)
        rate_layout.addWidget(rateLabel, 1, Qt.AlignCenter)
        rate_layout.addWidget(self.rateTF, 2, Qt.AlignCenter)
        return rate_layout

    def double_rate_layout(self):
        rate_layout = QGridLayout()
        cb = QRadioButton("")
        cb.resize(100, 30)
        layout1 = QHBoxLayout()
        rateLabel = QLabel()
        rateLabel.resize(100, 40)
        rateLabel.setText("Ratio min. : ")
        self.rateMin = QLineEdit()
        self.rateMin.resize(50, 40)
        self.rateMin.setPlaceholderText("Ratio")
        layout1.addWidget(rateLabel, 1, Qt.AlignCenter)
        layout1.addWidget(self.rateMin, 2, Qt.AlignCenter)
        layout2 = QHBoxLayout()
        rateLabel2 = QLabel()
        rateLabel2.resize(100, 40)
        rateLabel2.setText("Ratio max. : ")
        self.rateMax = QLineEdit()
        self.rateMax.resize(50, 40)
        self.rateMax.setPlaceholderText("Ratio")
        layout2.addWidget(rateLabel2, 1, Qt.AlignCenter)
        layout2.addWidget(self.rateMax, 2, Qt.AlignCenter)
        rate_layout.addWidget(cb, 0, 0, 2, 1)
        rate_layout.addItem(layout1, 0, 1)
        rate_layout.addItem(layout2, 1, 1)
        return rate_layout

    def precision_layout(self):
        precision_layout = QHBoxLayout()
        self.precL = QLabel()
        self.precL.resize(50, 40)
        precision_layout.addWidget(self.precL, 1, Qt.AlignRight)
        return precision_layout

    def update_button(self):
        button = QPushButton()
        button.setText("Update")
        button.clicked.connect(lambda: self.execCalcul())
        return button
