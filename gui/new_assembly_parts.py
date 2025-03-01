from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QLineEdit, QCheckBox, QMessageBox, QListWidgetItem
from database.db_manager import get_all_components, add_component, add_assembly
from PyQt5.QtCore import Qt
from gui.virtual_keyboard import VirtualKeyboard

class NewAssemblyStep2(QWidget):
    def __init__(self, main_window, num_parts):
        super().__init__()
        self.main_window = main_window
        self.num_parts = num_parts
        self.selected_components = []

        # ✅ Rename to avoid conflict with QWidget's layout() method
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(QLabel(f"Select {num_parts} components for the assembly:"))

        self.component_list = QListWidget()
        self.component_list.setSelectionMode(QListWidget.MultiSelection)
        self.load_components()

        self.main_layout.addWidget(self.component_list)

        self.next_button = QPushButton("Next")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self.go_to_confirmation)

        create_button = QPushButton("Create New Component")
        create_button.clicked.connect(self.show_create_component_form)

        back_button = QPushButton("Back")
        back_button.setFixedSize(200, 80)
        back_button.clicked.connect(lambda: main_window.set_screen(2))

        self.main_layout.addWidget(create_button)
        self.main_layout.addWidget(self.next_button)
        self.main_layout.addWidget(back_button)

        self.component_list.itemSelectionChanged.connect(self.check_selection)

    def load_components(self):
        self.component_list.clear()
        components = get_all_components()
        for comp in components:
            item_text = f"{comp[1]} - Camera Job: {'Yes' if comp[2] else 'No'}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, comp[2])  # Store camera job status
            self.component_list.addItem(item)

    def check_selection(self):
        selected_items = self.component_list.selectedItems()
        if len(selected_items) == self.num_parts:
            # Check if all selected components have a camera job
            for item in selected_items:
                if not item.data(Qt.UserRole):
                    QMessageBox.warning(self, "Invalid Selection", "One or more selected components do not have a camera job created. Please select only components with a camera job.")
                    self.next_button.setEnabled(False)
                    return
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

    def go_to_confirmation(self):
        selected_items = [item.text() for item in self.component_list.selectedItems()]
        self.main_window.new_assembly_confirm = NewAssemblyConfirmation(self.main_window, selected_items)
        self.main_window.stack.addWidget(self.main_window.new_assembly_confirm)
        self.main_window.set_screen(self.main_window.stack.indexOf(self.main_window.new_assembly_confirm))

    def show_create_component_form(self):
        self.main_layout.addWidget(CreateComponentForm(self))

class CreateComponentForm(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        form_layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Component Name")
        self.name_input.mousePressEvent = self.show_keyboard  # ✅ Open keyboard when clicked

        self.camera_job_checkbox = QCheckBox("Camera Job Setup")

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_component)

        form_layout.addWidget(self.name_input)
        form_layout.addWidget(self.camera_job_checkbox)
        form_layout.addWidget(save_button)

        self.setLayout(form_layout)

    def show_keyboard(self, event):
        if not VirtualKeyboard.instance:
            self.keyboard = VirtualKeyboard(self.parent.main_layout, self.name_input)
            self.parent.main_layout.addWidget(self.keyboard, alignment=Qt.AlignBottom)

    def save_component(self):
        name = self.name_input.text()
        camera_job = 1 if self.camera_job_checkbox.isChecked() else 0
        if name:
            add_component(name, camera_job)
            self.parent.load_components()
            self.setParent(None)

class NewAssemblyConfirmation(QWidget):
    def __init__(self, main_window, components):
        super().__init__()
        self.main_window = main_window
        self.components = components

        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel("Confirm Your Assembly"))
        self.layout.addWidget(QLabel("Components Selected:"))

        for comp in components:
            self.layout.addWidget(QLabel(comp))

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter Assembly Name")
        self.name_input.mousePressEvent = self.show_keyboard

        confirm_button = QPushButton("Confirm")
        confirm_button.clicked.connect(self.save_assembly)

        back_button = QPushButton("Back")
        back_button.clicked.connect(lambda: main_window.set_screen(2))

        self.layout.addWidget(self.name_input)
        self.layout.addWidget(confirm_button)
        self.layout.addWidget(back_button)
        self.setLayout(self.layout)

    def show_keyboard(self, event):
        if not VirtualKeyboard.instance:
            self.keyboard = VirtualKeyboard(self.layout, self.name_input)
            self.layout.addWidget(self.keyboard, alignment=Qt.AlignBottom)

    def save_assembly(self):
        name = self.name_input.text()
        if name:
            add_assembly(name, self.components)
            self.main_window.set_screen(0)
