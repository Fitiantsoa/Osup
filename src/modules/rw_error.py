from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QDialog
from PyQt5.QtCore import Qt


class Error(QDialog):

    def __init__(self):
        super().__init__()
        self.resize(200, 75)
        self.label = QLabel()
        self.create_layout()

    def show_error(self, message):
        self.label.setText(message)
        self.exec_()

    def create_layout(self):
        layout = QVBoxLayout()
        button = QPushButton()
        button.setText("Ok")
        button.clicked.connect(lambda: self.hide())
        layout.addWidget(self.label, alignment=Qt.AlignCenter)
        layout.addWidget(button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
