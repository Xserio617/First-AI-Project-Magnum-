from PyQt6.QtWidgets import (

    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 

    QPushButton, QGridLayout, QTabWidget, QScrollArea, QTextEdit

)

from PyQt6.QtCore import Qt, pyqtSignal

from PyQt6.QtGui import QCursor

from src.ui.components import (

    SmoothScrollArea, SidebarIconButton, CharacterCard, ModernButton

)



class ProfilePage(QWidget):

    character_selected = pyqtSignal(str)

    create_character_clicked = pyqtSignal()

    edit_persona_clicked = pyqtSignal()

    logout_clicked = pyqtSignal()



    def __init__(self, user_data, characters, parent=None):

        super().__init__(parent)

        self.user_data = user_data

        self.characters = characters

        self.setup_ui()



    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)



        scroll = SmoothScrollArea()

        content_widget = QWidget()

        content_layout = QVBoxLayout(content_widget)

        content_layout.setContentsMargins(40, 40, 40, 40)

        content_layout.setSpacing(30)



        profile_card = QFrame()

        profile_card.setStyleSheet("""

            QFrame {

                background-color: #18181b;

                border: 1px solid #27272a;

                border-radius: 16px;

            }

        """)

        card_layout = QHBoxLayout(profile_card)

        card_layout.setContentsMargins(30, 30, 30, 30)

        card_layout.setSpacing(30)



        self.avatar_lbl = QLabel()

        self.avatar_lbl.setFixedSize(100, 100)

        current_persona = self._get_current_persona()

        self._set_avatar(current_persona)

        card_layout.addWidget(self.avatar_lbl)



        info_layout = QVBoxLayout()

        print("Gelen User Data:", self.user_data)

        real_username = self.user_data.get("username", current_persona.get("name", "User"))

        self.name_lbl = QLabel(real_username)

        self.name_lbl.setStyleSheet("color: white; font-size: 32px; font-weight: bold; border: none;")

        info_layout.addWidget(self.name_lbl)



        self.bio_lbl = QLabel(current_persona.get("description", "No biography added yet."))

        self.bio_lbl.setStyleSheet("color: #a1a1aa; font-size: 14px; border: none;")

        self.bio_lbl.setWordWrap(True)

        info_layout.addWidget(self.bio_lbl)

        

        card_layout.addLayout(info_layout)

        card_layout.addStretch()

        

        btn_edit = SidebarIconButton("settings", "Edit Profile")

        btn_edit.clicked.connect(self.edit_persona_clicked.emit)

        card_layout.addWidget(btn_edit, alignment=Qt.AlignmentFlag.AlignTop)



        content_layout.addWidget(profile_card)



        self.tabs = QTabWidget()

        self.tabs.setStyleSheet("""

            QTabWidget::pane { border: none; }

            QTabBar::tab {

                background: transparent;

                color: #71717a;

                font-size: 16px;

                font-weight: 600;

                padding: 10px 20px;

                border-bottom: 2px solid transparent;

            }

            QTabBar::tab:selected {

                color: #6366f1;

                border-bottom: 2px solid #6366f1;

            }

            QTabBar::tab:hover { color: #e4e4e7; }

        """)



        tab_chars = QWidget()

        chars_layout = QVBoxLayout(tab_chars)

        chars_layout.setContentsMargins(0, 20, 0, 0)

        

        btn_create = ModernButton("+ Create New Character", primary=True)

        btn_create.setFixedWidth(250)

        btn_create.clicked.connect(self.create_character_clicked.emit)

        chars_layout.addWidget(btn_create, alignment=Qt.AlignmentFlag.AlignLeft)

        chars_layout.addSpacing(20)



        grid_widget = QWidget()

        self.chars_grid = QGridLayout(grid_widget)

        self.chars_grid.setContentsMargins(0, 0, 0, 0)

        self.chars_grid.setSpacing(20)

        self.chars_grid.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        

        self.refresh_characters_grid()

        

        chars_layout.addWidget(grid_widget)

        chars_layout.addStretch()

        self.tabs.addTab(tab_chars, "My Characters")



        tab_personas = QWidget()

        personas_layout = QVBoxLayout(tab_personas)

        personas_layout.setContentsMargins(0, 20, 0, 0)

        personas_layout.setSpacing(10)

        

        lbl_info = QLabel("Different identities you use in chats:")

        lbl_info.setStyleSheet("color: #a1a1aa; font-size: 14px;")

        personas_layout.addWidget(lbl_info)

        

        self.personas_container = QVBoxLayout()

        self.refresh_personas_list()

        personas_layout.addLayout(self.personas_container)

        

        personas_layout.addStretch()

        self.tabs.addTab(tab_personas, "My Personas")



        content_layout.addWidget(self.tabs)

        content_layout.addStretch()



        btn_logout = ModernButton("Logout", danger=True)

        btn_logout.setFixedWidth(200)

        btn_logout.clicked.connect(self.logout_clicked.emit)

        content_layout.addWidget(btn_logout, alignment=Qt.AlignmentFlag.AlignRight)



        scroll.setWidget(content_widget)

        layout.addWidget(scroll)



    def _get_current_persona(self):

        """Mevcut seçili personayı veya ilkini döndürür"""

        personas = self.user_data.get("personas", [])

        if personas:

            return personas[0]

        return {}



    def _set_avatar(self, persona):

        avatar_path = persona.get("avatar")

        if avatar_path:

             self.avatar_lbl.setStyleSheet(f"""

                border-radius: 50px; 

                border: 2px solid #6366f1;

                background-image: url('{avatar_path.replace('\\', '/')}');

                background-position: center;

                background-repeat: no-repeat; 

             """)

        else:

            name = persona.get("name", "U")

            display_char = name[0].upper() if name else "U"

            self.avatar_lbl.setText(display_char)

            self.avatar_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.avatar_lbl.setStyleSheet("""

                background-color: #27272a; 

                color: white; 

                font-size: 40px; 

                font-weight: bold; 

                border-radius: 50px;

                border: 2px solid #3f3f46;

            """)



    def refresh_characters_grid(self):

        """Karakterleri grid'e dizer"""

        while self.chars_grid.count():

            item = self.chars_grid.takeAt(0)

            if item.widget(): item.widget().deleteLater()



        columns = 3

        for index, (name, data) in enumerate(self.characters.items()):

            card = CharacterCard(name, data, is_selected=False)

            card.setFixedWidth(240)

            card.clicked.connect(self.character_selected.emit)

            

            row = index // columns

            col = index % columns

            self.chars_grid.addWidget(card, row, col)



    def refresh_personas_list(self):

        """Personaları liste halinde gösterir"""

        while self.personas_container.count():

            item = self.personas_container.takeAt(0)

            if item.widget(): item.widget().deleteLater()

            

        personas = self.user_data.get("personas", [])

        

        for p in personas:

            p_frame = QFrame()

            p_frame.setStyleSheet("background-color: #1e1e2e; border-radius: 10px; padding: 10px;")

            p_layout = QHBoxLayout(p_frame)

            

            p_avatar = QLabel()

            p_avatar.setFixedSize(40, 40)

            path = p.get("avatar")

            if path:

                p_avatar.setStyleSheet(f"border-radius: 20px; background-image: url('{path.replace('\\','/')}'); background-position: center;")

            else:

                name = p.get("name", "U")

                display_char = name[0].upper() if name else "U"

                p_avatar.setText(display_char)

                p_avatar.setStyleSheet("background-color: #6366f1; color: white; border-radius: 20px; qproperty-alignment: AlignCenter; font-weight: bold;")

            

            p_layout.addWidget(p_avatar)

            

            p_info = QVBoxLayout()

            p_name = QLabel(p.get("name", "Unnamed"))

            p_name.setStyleSheet("color: white; font-weight: bold; font-size: 14px; border: none;")

            p_desc = QLabel(p.get("description", "")[:50] + "...")

            p_desc.setStyleSheet("color: #a1a1aa; font-size: 12px; border: none;")

            p_info.addWidget(p_name)

            p_info.addWidget(p_desc)

            p_layout.addLayout(p_info)

            

            p_layout.addStretch()

            

            btn_edit = QPushButton("Edit")

            btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)

            btn_edit.setStyleSheet("color: #6366f1; border: none; font-weight: bold; background: transparent;")

            btn_edit.clicked.connect(self.edit_persona_clicked.emit)

            p_layout.addWidget(btn_edit)

            

            self.personas_container.addWidget(p_frame)

            

    def refresh_content(self, user_data, characters):

        """Veri değiştiğinde sayfayı yenilemek için"""

        self.user_data = user_data

        self.characters = characters

        

        current = self._get_current_persona()

        

        

        real_username = self.user_data.get("username", current.get("name", "User"))

        self.name_lbl.setText(real_username)



        self.bio_lbl.setText(current.get("description", ""))

        self._set_avatar(current)

        

        self.refresh_characters_grid()

        self.refresh_personas_list()