from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class CurrentJob(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Current Job Screen"))
        self.setLayout(layout)