from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class SelectAssembly(QWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select an Assembly Screen"))

        select_button = QPushButton("Confirm Selection")
        select_button.setFixedSize(300, 100)
        select_button.clicked.connect(lambda: main_window.set_screen(3))

        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 80)
        back_button.clicked.connect(lambda: main_window.set_screen(0))

        layout.addWidget(select_button)
        layout.addWidget(back_button)
        self.setLayout(layout)