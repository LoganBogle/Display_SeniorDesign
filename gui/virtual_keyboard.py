from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QLineEdit
from PyQt5.QtCore import Qt

class VirtualKeyboard(QWidget):
    instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(VirtualKeyboard, cls).__new__(cls)
        return cls.instance

    def __init__(self, parent_layout, target_input):
        super().__init__()  # ✅ Ensure the QWidget constructor is called
        
        if hasattr(self, 'initialized') and self.initialized:
            return
        
        self.target_input = target_input
        self.parent_layout = parent_layout
        self.initialized = True

        layout = QVBoxLayout()
        self.keys = [
            '1','2','3','4','5','6','7','8','9','0',
            'Q','W','E','R','T','Y','U','I','O','P',
            'A','S','D','F','G','H','J','K','L',
            'Z','X','C','V','B','N','M',' ','Backspace'
        ]

        grid = QGridLayout()
        row, col = 0, 0

        for key in self.keys:
            button = QPushButton(key)
            button.clicked.connect(lambda checked, k=key: self.key_pressed(k))
            grid.addWidget(button, row, col)
            col += 1
            if col > 9:
                col = 0
                row += 1

        finish_button = QPushButton("Close Keyborad")
        finish_button.clicked.connect(self.close_keyboard)

        layout.addLayout(grid)
        layout.addWidget(finish_button)
        self.setLayout(layout)

    def key_pressed(self, key):
        if key == 'Backspace':
            current_text = self.target_input.text()
            self.target_input.setText(current_text[:-1])
        else:
            self.target_input.setText(self.target_input.text() + key)

    def close_keyboard(self):
        self.parent_layout.removeWidget(self)
        self.deleteLater()
        VirtualKeyboard.instance = None
