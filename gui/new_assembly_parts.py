from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QCheckBox, QHBoxLayout, QComboBox, QListWidgetItem
from database.db_manager import get_all_components, add_component, add_assembly
from PyQt5.QtCore import Qt
from PyQt5 import QtGui 
from gui.virtual_keyboard import VirtualKeyboard

class NewAssemblyStep2(QWidget):
    def __init__(self, main_window, num_parts):
        super().__init__()
        self.main_window = main_window
        self.num_parts = num_parts
        self.selected_components = []

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        title_label = QLabel(f"Select {num_parts} components for the assembly:")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        self.main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        self.component_list = QListWidget()
        self.component_list.setSelectionMode(QListWidget.MultiSelection)
        self.component_list.setStyleSheet("background-color: #3B4252; color: white; border-radius: 5px; padding: 5px; font-size: 18px;")
        self.load_components()
        self.main_layout.addWidget(self.component_list)

        button_layout = QHBoxLayout()
        create_button = QPushButton("Create New Component")
        create_button.setFixedSize(250, 100)
        create_button.setStyleSheet("background-color: #A3BE8C; color: white; font-size: 20px; border-radius: 10px;")
        create_button.clicked.connect(self.show_create_component_form)

        self.next_button = QPushButton("Next")
        self.next_button.setFixedSize(250, 100)
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet("background-color: #5E81AC; color: white; font-size: 20px; border-radius: 10px;")
        self.next_button.clicked.connect(self.go_to_confirmation)

        back_button = QPushButton("Back")
        back_button.setFixedSize(250, 100)
        back_button.setStyleSheet("background-color: #BF616A; color: white; font-size: 20px; border-radius: 10px;")
        back_button.clicked.connect(lambda: main_window.set_screen(2))

        button_layout.addWidget(create_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(back_button)
        self.main_layout.addLayout(button_layout)

        self.component_list.itemSelectionChanged.connect(self.check_selection)
        self.apply_styles()

    def load_components(self):
        self.component_list.clear()
        components = get_all_components()  # Fetch components from the database
        
        for comp in components:
            item_text = f"{comp[1]}"  # Only display the name
            item = QListWidgetItem(item_text)
            
            # Store camera job status correctly in Qt.UserRole
            item.setData(Qt.UserRole, (comp[2], comp[3], comp[4]))  # (Tray 1, Tray 2, Tray 3)
            
            self.component_list.addItem(item)
    
    def show_create_component_form(self):
        self.main_layout.addWidget(CreateComponentForm(self))

    def check_selection(self):
        if len(self.component_list.selectedItems()) == self.num_parts:
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

    def go_to_confirmation(self):
        selected_items = [item.text() for item in self.component_list.selectedItems()]
        self.main_window.new_assembly_confirm = NewAssemblyConfirmation(self.main_window, selected_items)
        self.main_window.stack.addWidget(self.main_window.new_assembly_confirm)
        self.main_window.set_screen(self.main_window.stack.indexOf(self.main_window.new_assembly_confirm))

    def apply_styles(self):
        self.setStyleSheet(""
            "QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 18px; font-family: Arial, sans-serif;}"
            "QPushButton:hover {background-color: #81A1C1;}"
            "QLabel {font-size: 20px; font-weight: bold;}"
        "")

class CreateComponentForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        form_layout = QVBoxLayout()

        title_label = QLabel("Create New Component")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        form_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Component Name")
        self.name_input.setFixedWidth(400)
        self.name_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 20px; padding: 10px; border-radius: 5px;")
        self.name_input.mousePressEvent = self.show_keyboard
        form_layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        # --- Locate Job IDs Row ---
        locate_layout = QHBoxLayout()

        self.tray1_input = QLineEdit()
        self.tray1_input.setPlaceholderText("Locate Tray 1")
        self.tray1_input.setFixedWidth(240)
        self.tray1_input.setValidator(QtGui.QIntValidator(0, 320))
        self.tray1_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 18px; padding: 8px; border-radius: 5px;")

        self.tray2_input = QLineEdit()
        self.tray2_input.setPlaceholderText("Locate Tray 2")
        self.tray2_input.setFixedWidth(240)
        self.tray2_input.setValidator(QtGui.QIntValidator(0, 320))
        self.tray2_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 18px; padding: 8px; border-radius: 5px;")

        self.tray3_input = QLineEdit()
        self.tray3_input.setPlaceholderText("Locate Tray 3")
        self.tray3_input.setFixedWidth(240)
        self.tray3_input.setValidator(QtGui.QIntValidator(0, 320))
        self.tray3_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 18px; padding: 8px; border-radius: 5px;")

        locate_layout.addWidget(self.tray1_input)
        locate_layout.addWidget(self.tray2_input)
        locate_layout.addWidget(self.tray3_input)

        form_layout.addLayout(locate_layout)

        # --- Count Job IDs Row ---
        count_layout = QHBoxLayout()

        self.count_tray1_input = QLineEdit()
        self.count_tray1_input.setPlaceholderText("Count Tray 1")
        self.count_tray1_input.setFixedWidth(240)
        self.count_tray1_input.setValidator(QtGui.QIntValidator(0, 320))
        self.count_tray1_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 18px; padding: 8px; border-radius: 5px;")

        self.count_tray2_input = QLineEdit()
        self.count_tray2_input.setPlaceholderText("Count Tray 2")
        self.count_tray2_input.setFixedWidth(240)
        self.count_tray2_input.setValidator(QtGui.QIntValidator(0, 320))
        self.count_tray2_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 18px; padding: 8px; border-radius: 5px;")

        self.count_tray3_input = QLineEdit()
        self.count_tray3_input.setPlaceholderText("Count Tray 3")
        self.count_tray3_input.setFixedWidth(240)
        self.count_tray3_input.setValidator(QtGui.QIntValidator(0, 320))
        self.count_tray3_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 18px; padding: 8px; border-radius: 5px;")

        count_layout.addWidget(self.count_tray1_input)
        count_layout.addWidget(self.count_tray2_input)
        count_layout.addWidget(self.count_tray3_input)

        form_layout.addLayout(count_layout)

        # Shark Fin checkbox
        self.shark_fin_checkbox = QCheckBox("Has Shark Fin")
        self.shark_fin_checkbox.setStyleSheet("font-size: 22px; padding: 10px;")
        form_layout.addWidget(self.shark_fin_checkbox, alignment=Qt.AlignCenter)

        # Save button
        save_button = QPushButton("Save")
        save_button.setFixedSize(300, 100)
        save_button.setStyleSheet("background-color: #5E81AC; color: white; font-size: 22px; border-radius: 10px;")
        save_button.clicked.connect(self.save_component)
        form_layout.addWidget(save_button, alignment=Qt.AlignCenter)

        self.setLayout(form_layout)
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 18px; font-family: Arial, sans-serif;}
            QPushButton:hover {background-color: #81A1C1;}
            QLabel {font-size: 20px; font-weight: bold;}
        """)

    def show_keyboard(self, event):
        if not VirtualKeyboard.instance:
            self.keyboard = VirtualKeyboard(self.parent.layout(), self.name_input)
            self.parent.layout().addWidget(self.keyboard, alignment=Qt.AlignBottom)

    def save_component(self):
        name = self.name_input.text()
        tray1 = int(self.tray1_input.text()) if self.tray1_input.text() else 0
        tray2 = int(self.tray2_input.text()) if self.tray2_input.text() else 0
        tray3 = int(self.tray3_input.text()) if self.tray3_input.text() else 0
        count1 = int(self.count_tray1_input.text()) if self.count_tray1_input.text() else 0
        count2 = int(self.count_tray2_input.text()) if self.count_tray2_input.text() else 0
        count3 = int(self.count_tray3_input.text()) if self.count_tray3_input.text() else 0
        shark_fin = 1 if self.shark_fin_checkbox.isChecked() else 0

        if name:
            add_component(name, tray1, tray2, tray3, count1, count2, count3, shark_fin)
            self.parent.load_components()
            self.setParent(None)



class NewAssemblyConfirmation(QWidget):
    def __init__(self, main_window, components):
        super().__init__()
        self.main_window = main_window
        self.components = components

        self.layout = QVBoxLayout()

        title_label = QLabel("Confirm Your Assembly")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; text-align: center;")
        self.layout.addWidget(title_label, alignment=Qt.AlignCenter)

        subtitle_label = QLabel("Select Tray Assignments")
        subtitle_label.setStyleSheet("font-size: 20px; font-weight: bold; text-align: center;")
        self.layout.addWidget(subtitle_label, alignment=Qt.AlignCenter)
        
        self.tray_selections = {}  # Store selected trays for each component

        for comp in components:
            component_label = QLabel(comp)
            component_label.setStyleSheet("font-size: 20px;")
            self.layout.addWidget(component_label)
            
            # Get stored camera job availability
            tray_options = []
            component_data = next((item for item in self.main_window.new_assembly_step2.component_list.findItems(comp, Qt.MatchExactly)), None)

            if component_data:
                camera_jobs = component_data.data(Qt.UserRole)
                if camera_jobs is None:
                    camera_jobs = (0, 0, 0)
                
                print(f"DEBUG: {comp} camera jobs -> {camera_jobs}")  # Debug statement to print tray availability

                if camera_jobs[0]:
                    tray_options.append("Tray 1")
                if camera_jobs[1]:
                    tray_options.append("Tray 2")
                if camera_jobs[2]:
                    tray_options.append("Tray 3")
            
            tray_dropdown = QComboBox()
            if tray_options:
                tray_dropdown.addItems(tray_options)
            else:
                tray_dropdown.addItem("No available trays")
                tray_dropdown.setEnabled(False)
            
            tray_dropdown.setStyleSheet("font-size: 18px; padding: 10px; border-radius: 5px;")
            self.tray_selections[comp] = tray_dropdown
            self.layout.addWidget(tray_dropdown)

        self.name_input = QLineEdit()
        self.name_input.setFixedWidth(400)  # Increase width to fully display placeholder
        self.name_input.setPlaceholderText("Enter Assembly Name")
        self.name_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 20px; padding: 10px; border-radius: 5px;")
        self.name_input.mousePressEvent = self.show_keyboard
        self.layout.addWidget(self.name_input, alignment=Qt.AlignCenter)

        button_layout = QHBoxLayout()
        
        confirm_button = QPushButton("Confirm")
        confirm_button.setFixedSize(300, 100)
        confirm_button.setStyleSheet("background-color: #5E81AC; color: white; font-size: 22px; border-radius: 10px;")
        confirm_button.clicked.connect(self.save_assembly)
        
        back_button = QPushButton("Back")
        back_button.setFixedSize(300, 100)
        back_button.setStyleSheet("background-color: #BF616A; color: white; font-size: 22px; border-radius: 10px;")
        back_button.clicked.connect(lambda: main_window.set_screen(2))
        
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(back_button)
        self.layout.addLayout(button_layout)
        
        self.setLayout(self.layout)
        self.apply_styles()
    
    def apply_styles(self):
        self.setStyleSheet(""
            "QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 18px; font-family: Arial, sans-serif;}"
            "QPushButton:hover {background-color: #81A1C1;}"
            "QLabel {font-size: 20px; font-weight: bold;}"
        "")
    
    def show_keyboard(self, event):
        if not VirtualKeyboard.instance:
            self.keyboard = VirtualKeyboard(self.layout, self.name_input)
            self.layout.addWidget(self.keyboard, alignment=Qt.AlignBottom)
    
    def save_assembly(self):
        name = self.name_input.text()
        if name:
            tray_assignments = {"Tray 1": [], "Tray 2": [], "Tray 3": []}
            for comp in self.components:
                selected_tray = self.tray_selections[comp].currentText()
                if "Tray" in selected_tray:
                    tray_assignments[selected_tray].append(comp)
            
            add_assembly(name, tray_assignments["Tray 1"], tray_assignments["Tray 2"], tray_assignments["Tray 3"])  
            self.main_window.set_screen(0)
