from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt


class CurrentJob(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel("Current Job Screen")
        label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        layout.addWidget(label, alignment=Qt.AlignCenter)
        self.setLayout(layout)
