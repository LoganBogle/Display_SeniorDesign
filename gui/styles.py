from PyQt5.QtWidgets import QWidget

class StyledWidget(QWidget):
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 20px; font-family: Arial, sans-serif;}
            QPushButton {background-color: #5E81AC; color: white; font-size: 22px; border-radius: 15px; padding: 15px;}
            QPushButton:hover {background-color: #81A1C1;}
            QLabel {font-size: 22px; font-weight: bold; text-align: center;}
            QListWidget {background-color: #3B4252; color: white; border-radius: 10px; padding: 10px; font-size: 20px;}
            QLineEdit {background-color: #4C566A; color: white; font-size: 20px; padding: 10px; border-radius: 10px;}
            QComboBox {background-color: #4C566A; color: white; font-size: 20px; padding: 10px; border-radius: 10px;}
        """)