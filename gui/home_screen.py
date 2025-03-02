from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from gui.styles import StyledWidget

class HomeScreen(StyledWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout()
        self.apply_styles()

        select_button = QPushButton("Select Assembly")
        new_button = QPushButton("Create New Assembly")

        select_button.setFixedSize(350, 120)
        new_button.setFixedSize(350, 120)

        layout.addWidget(select_button, alignment=Qt.AlignCenter)
        layout.addWidget(new_button, alignment=Qt.AlignCenter)

        select_button.clicked.connect(lambda: main_window.set_screen(1))
        new_button.clicked.connect(lambda: main_window.set_screen(2))

        self.setLayout(layout)