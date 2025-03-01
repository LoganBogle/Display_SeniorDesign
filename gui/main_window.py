from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QPushButton, QVBoxLayout, QWidget
from gui.select_assembly import SelectAssembly
from gui.new_assembly import NewAssemblyStep1
from gui.current_job import CurrentJob

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pick and Place System")
        self.resize(800, 600)

        self.stack = QStackedWidget()
        self.home_screen = HomeScreen(self)
        self.select_assembly = SelectAssembly(self)
        self.new_assembly_step1 = NewAssemblyStep1(self)
        self.current_job = CurrentJob()

        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.select_assembly)
        self.stack.addWidget(self.new_assembly_step1)
        self.stack.addWidget(self.current_job)

        self.setCentralWidget(self.stack)

    def set_screen(self, index):
        self.stack.setCurrentIndex(index)


class HomeScreen(QWidget):
    def __init__(self, main_window):
        super().__init__()
        layout = QVBoxLayout()
        select_button = QPushButton("Select Assembly")
        new_button = QPushButton("Create New Assembly")

        select_button.setFixedSize(300, 100)
        new_button.setFixedSize(300, 100)

        layout.addWidget(select_button)
        layout.addWidget(new_button)

        select_button.clicked.connect(lambda: main_window.set_screen(1))
        new_button.clicked.connect(lambda: main_window.set_screen(2))

        self.setLayout(layout)