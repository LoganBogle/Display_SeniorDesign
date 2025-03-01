from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QIcon
from database.db_manager import get_all_assemblies, get_assembly_details

class SelectAssembly(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        layout = QVBoxLayout()
        title_label = QLabel("Select an Assembly")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        self.assembly_list = QListWidget()
        self.assembly_list.setStyleSheet("background-color: #3B4252; color: white; border-radius: 5px; padding: 5px;")
        self.load_assemblies()
        layout.addWidget(self.assembly_list)

        button_layout = QHBoxLayout()
        select_button = QPushButton(" Confirm Selection")
        select_button.setIcon(QIcon("icons/check.png"))
        select_button.setFixedSize(300, 100)
        select_button.setStyleSheet("background-color: #5E81AC; color: white; border-radius: 10px; font-size: 16px;")
        select_button.clicked.connect(self.confirm_selection)
        
        back_button = QPushButton(" Back")
        back_button.setIcon(QIcon("icons/back.png"))
        back_button.setFixedSize(200, 80)
        back_button.setStyleSheet("background-color: #BF616A; color: white; border-radius: 10px; font-size: 16px;")
        back_button.clicked.connect(lambda: main_window.set_screen(0))

        button_layout.addWidget(select_button)
        button_layout.addWidget(back_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.apply_styles()
    
    def load_assemblies(self):
        self.assembly_list.clear()
        assemblies = get_all_assemblies()
        for assembly in assemblies:
            self.assembly_list.addItem(assembly[1])
    
    def confirm_selection(self):
        selected_item = self.assembly_list.currentItem()
        if selected_item:
            selected_assembly = selected_item.text()
            print(f"Assembly Selected: {selected_assembly}")
            self.main_window.tray_assignment_screen = TrayAssignmentScreen(self.main_window, selected_assembly)
            self.main_window.stack.addWidget(self.main_window.tray_assignment_screen)
            self.main_window.set_screen(self.main_window.stack.indexOf(self.main_window.tray_assignment_screen))

    def apply_styles(self):
        self.setStyleSheet(""
            "QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 18px; font-family: Arial, sans-serif;}"
            "QPushButton:hover {background-color: #81A1C1;}"
            "QLabel {font-size: 20px; font-weight: bold;}"
        "")


class TrayAssignmentScreen(QWidget):
    def __init__(self, main_window, assembly_name):
        super().__init__()
        self.main_window = main_window
        self.assembly_name = assembly_name

        layout = QVBoxLayout()

        title_label = QLabel(f"Tray Assignments for: {assembly_name}")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Retrieve tray assignments from the database
        assembly_details = get_assembly_details(assembly_name)
        
        if assembly_details:
            tray_1_components = assembly_details[1].split(',') if assembly_details[1] else []
            tray_2_components = assembly_details[2].split(',') if assembly_details[2] else []
            tray_3_components = assembly_details[3].split(',') if assembly_details[3] else []
            
            layout.addWidget(self.create_styled_label("Tray 1 Components:"))
            for component in tray_1_components:
                layout.addWidget(self.create_styled_label(component))
            
            layout.addWidget(self.create_styled_label("Tray 2 Components:"))
            for component in tray_2_components:
                layout.addWidget(self.create_styled_label(component))
            
            layout.addWidget(self.create_styled_label("Tray 3 Components:"))
            for component in tray_3_components:
                layout.addWidget(self.create_styled_label(component))
        else:
            layout.addWidget(self.create_styled_label("No tray assignments found for this assembly."))

        confirm_button = QPushButton("Confirm and Start Main Run")
        confirm_button.setStyleSheet("background-color: #5E81AC; color: white; font-size: 16px; border-radius: 10px;")
        confirm_button.clicked.connect(self.start_main_run)
        layout.addWidget(confirm_button)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #BF616A; color: white; font-size: 16px; border-radius: 10px;")
        back_button.clicked.connect(lambda: main_window.set_screen(1))
        layout.addWidget(back_button)

        self.setLayout(layout)
        self.apply_styles()
    
    def create_styled_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("font-size: 18px; font-weight: normal; text-align: center; padding: 5px;")
        return label

    def apply_styles(self):
        self.setStyleSheet(""
            "QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 18px; font-family: Arial, sans-serif;}"
            "QPushButton:hover {background-color: #81A1C1;}"
            "QLabel {font-size: 20px; font-weight: bold;}"
        "")

    def start_main_run(self):
        print("Starting main run...")  # Placeholder for actual main run logic
        self.main_window.run_screen = RunScreen(self.main_window, self.assembly_name, 100)  # Example: Replace 100 with actual total jobs
        self.main_window.stack.addWidget(self.main_window.run_screen)
        self.main_window.set_screen(self.main_window.stack.indexOf(self.main_window.run_screen))



class RunScreen(QWidget):
    def __init__(self, main_window, assembly_name, total_jobs):
        super().__init__()
        self.main_window = main_window
        self.assembly_name = assembly_name
        self.total_jobs = total_jobs
        self.completed_jobs = 0
        self.start_time = QTime.currentTime()

        layout = QVBoxLayout()
        
        title_label = QLabel(f"Current Assembly: {assembly_name}")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Display the ratio of completed jobs
        self.job_status_label = QLabel(f"Completed: {self.completed_jobs}/{self.total_jobs}")
        self.job_status_label.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")
        layout.addWidget(self.job_status_label, alignment=Qt.AlignCenter)

        # Timer label
        self.timer_label = QLabel("Time Elapsed: 00:00:00")
        self.timer_label.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")
        layout.addWidget(self.timer_label, alignment=Qt.AlignCenter)

        # Timer to update elapsed time
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second

        # Home button for the robot
        home_button = QPushButton("Home Robot")
        home_button.setStyleSheet("background-color: #5E81AC; color: white; font-size: 16px; border-radius: 10px;")
        home_button.clicked.connect(self.home_robot)
        layout.addWidget(home_button, alignment=Qt.AlignCenter)

        # Back button
        back_button = QPushButton("Back to Home")
        back_button.setStyleSheet("background-color: #BF616A; color: white; font-size: 16px; border-radius: 10px;")
        back_button.clicked.connect(lambda: main_window.set_screen(0))
        layout.addWidget(back_button, alignment=Qt.AlignCenter)

        self.setLayout(layout)
        self.apply_styles()
    
    def update_timer(self):
        elapsed = self.start_time.elapsed() // 1000  # Get elapsed time in seconds
        hours = elapsed // 3600
        minutes = (elapsed % 3600) // 60
        seconds = elapsed % 60
        self.timer_label.setText(f"Time Elapsed: {hours:02}:{minutes:02}:{seconds:02}")
    
    def home_robot(self):
        print("Sending robot to home position...")  # Placeholder action
    
    def apply_styles(self):
        self.setStyleSheet(""
            "QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 18px; font-family: Arial, sans-serif;}"
            "QPushButton:hover {background-color: #81A1C1;}"
            "QLabel {font-size: 20px; font-weight: bold;}"
        "")