"""

Modern PyQt6 Popups - Character.ai Style

Tam ve Düzenlenmiş Sürüm (Avatar Destekli Persona - FIX)

"""



from PyQt6.QtWidgets import (

    QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, 

    QPushButton, QHBoxLayout, QComboBox, QMessageBox, QFileDialog, QFrame, QWidget

)

from PyQt6.QtCore import Qt, pyqtSignal

from PyQt6.QtGui import QCursor

from src.ui.components import CustomTitleBar



class CharacterPopup(QDialog):

    character_saved = pyqtSignal(dict)



    def __init__(self, parent=None):

        super().__init__(parent)

        self.avatar_path = None

        self.setup_ui()



    def setup_ui(self):

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(450, 650)

        

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        

        self.bg_frame = QFrame()

        self.bg_frame.setStyleSheet("background-color: #18181b; border: 1px solid #3f3f46; border-radius: 12px;")

        layout.addWidget(self.bg_frame)

        

        inner_layout = QVBoxLayout(self.bg_frame)

        inner_layout.setContentsMargins(0, 0, 0, 0)

        

        self.title_bar = CustomTitleBar(self)

        self.title_bar.findChild(QLabel).setText("Create New Character")

        btn_max = self.title_bar.findChild(QPushButton, "btn_max")

        if btn_max: btn_max.hide()

        inner_layout.addWidget(self.title_bar)

        

        content_widget = QWidget()

        

        self.form_layout = QVBoxLayout(content_widget)

        self.form_layout.setContentsMargins(24, 20, 24, 24)

        self.form_layout.setSpacing(12)

        

        avatar_layout = QHBoxLayout()

        avatar_layout.addStretch()

        self.btn_avatar = QPushButton("Select Avatar")

        self.btn_avatar.setFixedSize(80, 80)

        self.btn_avatar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.btn_avatar.setStyleSheet("QPushButton { background-color: #27272a; color: #a1a1aa; border-radius: 40px; border: 2px dashed #3f3f46; font-size: 11px; } QPushButton:hover { border-color: #6366f1; color: #6366f1; }")

        self.btn_avatar.clicked.connect(self.select_avatar)

        avatar_layout.addWidget(self.btn_avatar)

        avatar_layout.addStretch()

        self.form_layout.addLayout(avatar_layout)

        

        self.inp_name = self.create_input("Character Name", "Ex: Benjamin")

        self.form_layout.addWidget(self.inp_name)

        

        self.inp_prompt = self.create_text_input("System Prompt (Personality)", "How should the character behave?", 100)

        self.form_layout.addWidget(self.inp_prompt)



        self.inp_greeting = self.create_text_input("First Message (Greeting)", "What will it say to the user first?", 60)

        self.form_layout.addWidget(self.inp_greeting)

        

        self.form_layout.addStretch()

        

        btn_layout = QHBoxLayout()

        self.btn_cancel = QPushButton("Cancel")

        self.btn_cancel.setFixedHeight(40)

        self.btn_cancel.setStyleSheet("QPushButton { background-color: transparent; color: #a1a1aa; border: 1px solid #3f3f46; border-radius: 8px; font-weight: 600; } QPushButton:hover { background-color: #27272a; color: white; }")

        self.btn_cancel.clicked.connect(self.close)

        

        self.btn_save = QPushButton("Create")

        self.btn_save.setFixedHeight(40)

        self.btn_save.setStyleSheet("QPushButton { background-color: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; } QPushButton:hover { background-color: #4f46e5; }")

        self.btn_save.clicked.connect(self.save_character)

        

        btn_layout.addWidget(self.btn_cancel)

        btn_layout.addWidget(self.btn_save)

        self.form_layout.addLayout(btn_layout)

        

        inner_layout.addWidget(content_widget)



    def create_input(self, label_text, placeholder):

        label = QLabel(label_text)

        label.setStyleSheet("color: #e4e4e7; font-weight: 600; font-size: 13px;")

        line_edit = QLineEdit()

        line_edit.setPlaceholderText(placeholder)

        line_edit.setFixedHeight(40)

        line_edit.setStyleSheet("QLineEdit { background-color: #27272a; color: white; border: 1px solid #3f3f46; border-radius: 8px; padding: 8px; } QLineEdit:focus { border: 1px solid #6366f1; }")

        

        self.form_layout.addWidget(label)

        return line_edit



    def create_text_input(self, label_text, placeholder, height):

        label = QLabel(label_text)

        label.setStyleSheet("color: #e4e4e7; font-weight: 600; font-size: 13px;")

        text_edit = QTextEdit()

        text_edit.setPlaceholderText(placeholder)

        text_edit.setFixedHeight(height)

        text_edit.setStyleSheet("QTextEdit { background-color: #27272a; color: white; border: 1px solid #3f3f46; border-radius: 8px; padding: 8px; } QTextEdit:focus { border: 1px solid #6366f1; }")

        

        self.form_layout.addWidget(label)

        return text_edit



    def select_avatar(self):

        file_name, _ = QFileDialog.getOpenFileName(self, "Select Avatar", "", "Image Files (*.png *.jpg *.jpeg)")

        if file_name:

            self.avatar_path = file_name

            self.btn_avatar.setText("")

            self.btn_avatar.setStyleSheet(f"QPushButton {{ background-color: #27272a; border: 2px solid #6366f1; border-radius: 40px; border-image: url({file_name.replace('\\', '/')}) 0 0 0 0 stretch stretch; }}")



    def save_character(self):

        name = self.inp_name.text().strip()

        prompt = self.inp_prompt.toPlainText().strip()

        greeting = self.inp_greeting.toPlainText().strip()

        

        if not name or not prompt:

            QMessageBox.warning(self, "Missing Information", "Please fill in at least the Name and Prompt fields.")

            return

            

        char_data_package = {

            "name": name, "prompt": prompt, "greeting": greeting, "avatar_source_path": self.avatar_path 

        }

        self.character_saved.emit(char_data_package)

        self.accept()



class PersonaPopup(QDialog):

    def __init__(self, parent, user_personas_list, on_save_callback):

        super().__init__(parent)

        self.personas = user_personas_list

        self.on_save = on_save_callback

        self.avatar_path = None

        

        if not self.personas:

            self.personas = [{"name": "Default", "gender": "Prefer not to say", "description": "", "avatar": None}]

        

        self.setup_ui()

        self.load_persona(0)



    def setup_ui(self):

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(500, 650)

        

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        

        self.bg_frame = QFrame()

        self.bg_frame.setStyleSheet("background-color: #18181b; border: 1px solid #3f3f46; border-radius: 12px;")

        layout.addWidget(self.bg_frame)

        

        inner_layout = QVBoxLayout(self.bg_frame)

        inner_layout.setContentsMargins(0, 0, 0, 0)

        

        self.title_bar = CustomTitleBar(self)

        self.title_bar.findChild(QLabel).setText("Profile Management")

        btn_max = self.title_bar.findChild(QPushButton, "btn_max")

        if btn_max: btn_max.hide()

        inner_layout.addWidget(self.title_bar)

        

        content_widget = QWidget()

        

        self.form_layout = QVBoxLayout(content_widget)

        self.form_layout.setContentsMargins(24, 20, 24, 24)

        self.form_layout.setSpacing(15)



        self.combo_personas = QComboBox()

        self.combo_personas.setFixedHeight(40)

        self.combo_personas.setStyleSheet("QComboBox { background-color: #27272a; color: white; border: 1px solid #3f3f46; border-radius: 8px; padding: 5px; } QComboBox::drop-down { border: none; }")

        self.combo_personas.currentIndexChanged.connect(self.load_persona)

        self.form_layout.addWidget(self.combo_personas)



        avatar_layout = QHBoxLayout()

        avatar_layout.addStretch()

        self.btn_avatar = QPushButton("Profile Picture")

        self.btn_avatar.setFixedSize(80, 80)

        self.btn_avatar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.btn_avatar.setStyleSheet("QPushButton { background-color: #27272a; color: #a1a1aa; border-radius: 40px; border: 2px dashed #3f3f46; font-size: 11px; } QPushButton:hover { border-color: #6366f1; color: #6366f1; }")

        self.btn_avatar.clicked.connect(self.select_avatar)

        avatar_layout.addWidget(self.btn_avatar)

        avatar_layout.addStretch()

        self.form_layout.addLayout(avatar_layout)



        self.entry_name = self.create_input("Profile Name", "")

        self.form_layout.addWidget(self.entry_name)

        

        lbl_gender = QLabel("Gender")

        lbl_gender.setStyleSheet("color: #e4e4e7; font-weight: 600; font-size: 13px;")

        self.form_layout.addWidget(lbl_gender)



        self.combo_gender = QComboBox()

        self.combo_gender.addItems(["Prefer not to say", "Male", "Female"])

        self.combo_gender.setFixedHeight(40)

        self.combo_gender.setStyleSheet("""

            QComboBox { 

                background-color: #27272a; color: white; 

                border: 1px solid #3f3f46; border-radius: 8px; padding: 5px; padding-left: 10px;

            }

            QComboBox::drop-down { border: none; }

            QComboBox:on { border: 1px solid #6366f1; }

        """)

        self.form_layout.addWidget(self.combo_gender)



        self.entry_desc = self.create_text_input("About (AI will know this)", "What should it know about you?", 100)

        self.form_layout.addWidget(self.entry_desc)



        btn_layout = QHBoxLayout()

        self.btn_delete = QPushButton("Delete")

        self.btn_delete.setFixedHeight(40)

        self.btn_delete.setStyleSheet("QPushButton { background-color: transparent; color: #ef4444; border: 1px solid #ef4444; border-radius: 8px; font-weight: 600; } QPushButton:hover { background-color: rgba(239, 68, 68, 0.1); }")

        self.btn_delete.clicked.connect(self.delete_persona)

        

        self.btn_save = QPushButton("Save")

        self.btn_save.setFixedHeight(40)

        self.btn_save.setStyleSheet("QPushButton { background-color: #6366f1; color: white; border: none; border-radius: 8px; font-weight: 600; } QPushButton:hover { background-color: #4f46e5; }")

        self.btn_save.clicked.connect(self.save)

        

        btn_layout.addWidget(self.btn_delete)

        btn_layout.addWidget(self.btn_save)

        self.form_layout.addLayout(btn_layout)

        

        inner_layout.addWidget(content_widget)

        self.refresh_combo()



    def create_input(self, label_text, placeholder):

        label = QLabel(label_text)

        label.setStyleSheet("color: #e4e4e7; font-weight: 600; font-size: 13px;")

        line_edit = QLineEdit()

        line_edit.setPlaceholderText(placeholder)

        line_edit.setFixedHeight(40)

        line_edit.setStyleSheet("QLineEdit { background-color: #27272a; color: white; border: 1px solid #3f3f46; border-radius: 8px; padding: 8px; } QLineEdit:focus { border: 1px solid #6366f1; }")

        self.form_layout.addWidget(label)

        return line_edit



    def create_text_input(self, label_text, placeholder, height):

        label = QLabel(label_text)

        label.setStyleSheet("color: #e4e4e7; font-weight: 600; font-size: 13px;")

        text_edit = QTextEdit()

        text_edit.setPlaceholderText(placeholder)

        text_edit.setFixedHeight(height)

        text_edit.setStyleSheet("QTextEdit { background-color: #27272a; color: white; border: 1px solid #3f3f46; border-radius: 8px; padding: 8px; } QTextEdit:focus { border: 1px solid #6366f1; }")

        self.form_layout.addWidget(label)

        return text_edit



    def refresh_combo(self):

        self.combo_personas.blockSignals(True)

        self.combo_personas.clear()

        self.combo_personas.addItems([p["name"] for p in self.personas])

        self.combo_personas.addItem("+ Create New Profile")

        self.combo_personas.blockSignals(False)



    def select_avatar(self):

        file_name, _ = QFileDialog.getOpenFileName(self, "Select Profile Picture", "", "Image Files (*.png *.jpg *.jpeg)")

        if file_name:

            self.avatar_path = file_name

            self.update_avatar_preview(file_name)



    def update_avatar_preview(self, path):

        if path:

            self.btn_avatar.setText("") 

            self.btn_avatar.setStyleSheet(f"QPushButton {{ background-color: #27272a; border: 2px solid #6366f1; border-radius: 40px; border-image: url('{path.replace('\\', '/')}') 0 0 0 0 stretch stretch; }}")

        else:

            self.btn_avatar.setText("Profile Picture")

            self.btn_avatar.setStyleSheet("QPushButton { background-color: #27272a; color: #a1a1aa; border-radius: 40px; border: 2px dashed #3f3f46; font-size: 11px; } QPushButton:hover { border-color: #6366f1; color: #6366f1; }")



    def load_persona(self, index):

        if index < len(self.personas):

            p = self.personas[index]

            self.entry_name.setText(p["name"])

            

            gender_val = p.get("gender", "Prefer not to say")

            index_cb = self.combo_gender.findText(gender_val)

            if index_cb >= 0:

                self.combo_gender.setCurrentIndex(index_cb)

            else:

                self.combo_gender.setCurrentIndex(0)



            self.entry_desc.setText(p.get("description", ""))

            

            self.avatar_path = p.get("avatar")

            self.update_avatar_preview(self.avatar_path)

            

            is_default = (index == 0)

            self.entry_name.setEnabled(not is_default)

            self.btn_delete.setEnabled(not is_default)

        else:

            self.entry_name.clear()

            self.combo_gender.setCurrentIndex(0)

            self.entry_desc.clear()

            self.avatar_path = None

            self.update_avatar_preview(None)

            self.entry_name.setEnabled(True)

            self.btn_delete.setEnabled(False)



    def save(self):

        name = self.entry_name.text().strip()

        if not name:

            QMessageBox.warning(self, "Error", "Profile name cannot be empty!")

            return



        new_persona = {

            "name": name,

            "gender": self.combo_gender.currentText(),

            "description": self.entry_desc.toPlainText().strip(),

            "avatar": self.avatar_path

        }



        current_idx = self.combo_personas.currentIndex()

        if current_idx < len(self.personas):

            self.personas[current_idx] = new_persona

        else:

            self.personas.append(new_persona)



        self.on_save(self.personas)

        self.accept()



    def delete_persona(self):

        current_idx = self.combo_personas.currentIndex()

        if current_idx >= len(self.personas): return 

        

        confirm = QMessageBox.question(self, "Confirm", "Are you sure you want to delete this profile?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        

        if confirm == QMessageBox.StandardButton.Yes:

            del self.personas[current_idx]

            self.on_save(self.personas)

            self.accept()