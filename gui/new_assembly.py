from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout

class NewAssemblyStep1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select the number of components (1-5):"))

        button_layout = QHBoxLayout()
        for i in range(1, 6):
            btn = QPushButton(str(i))
            btn.setFixedSize(100, 100)
            btn.clicked.connect(lambda checked, num=i: self.next_step(num))
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)

        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 80)
        back_button.clicked.connect(lambda: main_window.set_screen(0))
        layout.addWidget(back_button)

        self.setLayout(layout)

    def next_step(self, num_parts):
        from gui.new_assembly_parts import NewAssemblyStep2
        self.main_window.new_assembly_step2 = NewAssemblyStep2(self.main_window, num_parts)
        self.main_window.stack.addWidget(self.main_window.new_assembly_step2)
        self.main_window.set_screen(self.main_window.stack.indexOf(self.main_window.new_assembly_step2))