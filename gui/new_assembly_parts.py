from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QCheckBox, QHBoxLayout, QComboBox
from database.db_manager import get_all_components, add_component, add_assembly
from PyQt5.QtCore import Qt
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
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; text-align: center;")
        self.main_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        self.component_list = QListWidget()
        self.component_list.setSelectionMode(QListWidget.MultiSelection)
        self.component_list.setStyleSheet("background-color: #3B4252; color: white; border-radius: 5px; padding: 5px;")
        self.load_components()
        self.main_layout.addWidget(self.component_list)

        button_layout = QHBoxLayout()
        create_button = QPushButton("Create New Component")
        create_button.setStyleSheet("background-color: #A3BE8C; color: white; font-size: 16px; border-radius: 10px;")
        create_button.clicked.connect(self.show_create_component_form)

        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.setStyleSheet("background-color: #5E81AC; color: white; font-size: 16px; border-radius: 10px;")
        self.next_button.clicked.connect(self.go_to_confirmation)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("background-color: #BF616A; color: white; font-size: 16px; border-radius: 10px;")
        back_button.clicked.connect(lambda: main_window.set_screen(2))

        button_layout.addWidget(create_button)
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(back_button)
        self.main_layout.addLayout(button_layout)

        self.component_list.itemSelectionChanged.connect(self.check_selection)
        self.apply_styles()

    def load_components(self):
        self.component_list.clear()
        components = get_all_components()
        for comp in components:
            item_text = f"{comp[1]}"  
            self.component_list.addItem(item_text)

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
        self.setStyleSheet("""
            QWidget {background-color: #2E3440; color: #D8DEE9; font-size: 18px; font-family: Arial, sans-serif;}
            QPushButton:hover {background-color: #81A1C1;}
            QLabel {font-size: 20px; font-weight: bold;}
        """)

class CreateComponentForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        form_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Component Name")
        self.name_input.setStyleSheet("background-color: #4C566A; color: white; font-size: 16px; padding: 5px; border-radius: 5px;")

        self.tray1_checkbox = QCheckBox("Tray 1")
        self.tray2_checkbox = QCheckBox("Tray 2")
        self.tray3_checkbox = QCheckBox("Tray 3")

        checkboxes_layout = QHBoxLayout()
        checkboxes_layout.addWidget(self.tray1_checkbox)
        checkboxes_layout.addWidget(self.tray2_checkbox)
        checkboxes_layout.addWidget(self.tray3_checkbox)

        save_button = QPushButton("Save")
        save_button.setStyleSheet("background-color: #5E81AC; color: white; font-size: 16px; border-radius: 10px;")
        save_button.clicked.connect(self.save_component)

        form_layout.addWidget(self.name_input)
        form_layout.addLayout(checkboxes_layout)
        form_layout.addWidget(save_button)

        self.setLayout(form_layout)

    def save_component(self):
        name = self.name_input.text()
        tray1 = 1 if self.tray1_checkbox.isChecked() else 0
        tray2 = 1 if self.tray2_checkbox.isChecked() else 0
        tray3 = 1 if self.tray3_checkbox.isChecked() else 0
        
        if name:
            add_component(name, tray1, tray2, tray3)
            self.parent.load_components()
            self.setParent(None)


class NewAssemblyConfirmation(QWidget):
    def __init__(self, main_window, components):
        super().__init__()
        self.main_window = main_window
        self.components = components

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Confirm Your Assembly"))
        self.layout.addWidget(QLabel("Select Tray Assignments"))
        
        self.tray_selections = {}  # Store selected trays for each component

        for comp in components:
            component_label = QLabel(comp)
            self.layout.addWidget(component_label)
            
            # Get stored camera job availability
            tray_options = ["None"]
            component_data = next((item for item in self.main_window.new_assembly_step2.component_list.findItems(comp, Qt.MatchExactly)), None)
            if component_data:
                camera_jobs = component_data.data(Qt.UserRole)
                if camera_jobs[0]:
                    tray_options.append("Tray 1")
                if camera_jobs[1]:
                    tray_options.append("Tray 2")
                if camera_jobs[2]:
                    tray_options.append("Tray 3")
            
            tray_dropdown = QComboBox()
            tray_dropdown.addItems(tray_options)
            self.tray_selections[comp] = tray_dropdown
            self.layout.addWidget(tray_dropdown)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Assembly Name")
        self.layout.addWidget(self.name_input)

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.save_assembly)
        
        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: main_window.set_screen(2))
        
        self.layout.addWidget(confirm_button)
        self.layout.addWidget(back_button)
        self.setLayout(self.layout)

    def save_assembly(self):
        name = self.name_input.text()
        if name:
            tray_assignments = {"Tray 1": [], "Tray 2": [], "Tray 3": []}
            for comp in self.components:
                selected_tray = self.tray_selections[comp].currentText()
                if selected_tray != "None":
                    tray_assignments[selected_tray].append(comp)
            
            add_assembly(name, tray_assignments["Tray 1"], tray_assignments["Tray 2"], tray_assignments["Tray 3"])  # Save tray-specific assignments
            self.main_window.set_screen(0)
