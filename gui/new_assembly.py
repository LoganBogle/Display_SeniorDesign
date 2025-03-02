from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt

class NewAssemblyStep1(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        
        layout = QVBoxLayout()
        
        title_label = QLabel("Select the number of components (1-5):")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)
        
        button_layout = QHBoxLayout()
        for i in range(1, 6):
            btn = QPushButton(str(i))
            btn.setFixedSize(120, 120)
            btn.setStyleSheet("background-color: #5E81AC; color: white; font-size: 24px; border-radius: 10px;")
            btn.clicked.connect(lambda checked, num=i: self.next_step(num))
            button_layout.addWidget(btn, alignment=Qt.AlignCenter)
        
        layout.addLayout(button_layout)
        
        back_button = QPushButton("Back")
        back_button.setFixedSize(250, 100)
        back_button.setStyleSheet("background-color: #BF616A; color: white; font-size: 20px; border-radius: 10px;")
        back_button.clicked.connect(lambda: main_window.set_screen(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)
        
        self.setLayout(layout)
        self.apply_styles()
    
    def apply_styles(self):
        self.setStyleSheet(""
            "QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 18px; font-family: Arial, sans-serif;}"
            "QPushButton:hover {background-color: #81A1C1;}"
            "QLabel {font-size: 20px; font-weight: bold;}"
        "")
    
    def next_step(self, num_parts):
        from gui.new_assembly_parts import NewAssemblyStep2
        self.main_window.new_assembly_step2 = NewAssemblyStep2(self.main_window, num_parts)
        self.main_window.stack.addWidget(self.main_window.new_assembly_step2)
        self.main_window.set_screen(self.main_window.stack.indexOf(self.main_window.new_assembly_step2))