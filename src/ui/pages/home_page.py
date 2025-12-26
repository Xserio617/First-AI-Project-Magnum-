import random

from PyQt6.QtWidgets import (

    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout

)

from PyQt6.QtCore import Qt, pyqtSignal

from src.ui.components import (

    SmoothScrollArea, SearchBar, SidebarIconButton, CategoryTab, 

    FeaturedCharacterCard, CharacterCard

)



class HomePage(QWidget):

    character_selected = pyqtSignal(str) 

    profile_clicked = pyqtSignal()



    def __init__(self, characters, user_favorites, parent=None):

        super().__init__(parent)

        self.characters = characters

        self.user_favorites = user_favorites

        self.setup_ui()



    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(20)



        header = QFrame()

        header.setFixedHeight(70)

        header.setStyleSheet("background-color: #18181b; border-bottom: 1px solid #27272a;")

        header_layout = QHBoxLayout(header)

        header_layout.setContentsMargins(30, 0, 30, 0)

        

        self.search_bar = SearchBar()

        self.search_bar.setFixedWidth(400)

        header_layout.addWidget(self.search_bar)

        

        header_layout.addStretch()

        

        btn_profile = SidebarIconButton("user", "Profile")

        btn_profile.setFixedSize(40, 40)

        btn_profile.clicked.connect(self.profile_clicked.emit)

        header_layout.addWidget(btn_profile)

        

        layout.addWidget(header)



        main_scroll = SmoothScrollArea()

        scroll_content = QWidget()

        scroll_content.setStyleSheet("background: transparent;")

        

        content_layout = QVBoxLayout(scroll_content)

        content_layout.setContentsMargins(30, 30, 30, 30)

        content_layout.setSpacing(30)



        welcome = QLabel("Chat with Characters")

        welcome.setStyleSheet("color: #ffffff; font-size: 32px; font-weight: bold;")

        content_layout.addWidget(welcome)



        featured_label = QLabel("Featured (Random Selection)")

        featured_label.setStyleSheet("color: #a1a1aa; font-size: 14px; font-weight: 600;")

        content_layout.addWidget(featured_label)



        featured_scroll = SmoothScrollArea(orientation="horizontal")

        featured_scroll.setFixedHeight(230)

        featured_content = QWidget()

        featured_layout = QHBoxLayout(featured_content)

        featured_layout.setContentsMargins(0, 10, 0, 10)

        featured_layout.setSpacing(15)

        

        all_char_names = list(self.characters.keys())

        limit = 25

        sample_size = min(len(all_char_names), limit)

        

        if sample_size > 0:

            random_chars = random.sample(all_char_names, sample_size)

            for name in random_chars:

                data = self.characters[name]

                card = FeaturedCharacterCard(name, data)

                card.clicked.connect(self.character_selected.emit)

                featured_layout.addWidget(card)

        

        featured_layout.addStretch()

        featured_content.setLayout(featured_layout)

        featured_scroll.setWidget(featured_content)

        content_layout.addWidget(featured_scroll)



        all_title = QLabel("All Characters")

        all_title.setStyleSheet("color: #a1a1aa; font-size: 14px; font-weight: 600; margin-top: 20px;")

        content_layout.addWidget(all_title)

        

        grid_container = QWidget()

        grid_layout = QGridLayout(grid_container)

        grid_layout.setContentsMargins(0, 0, 0, 0)

        grid_layout.setSpacing(20)

        

        columns = 3

        

        for index, (name, data) in enumerate(self.characters.items()):

            card = CharacterCard(name, data, is_selected=False)

            card.clicked.connect(self.character_selected.emit)

            

            row = index // columns

            col = index % columns

            grid_layout.addWidget(card, row, col)

            

        content_layout.addWidget(grid_container)

        content_layout.addStretch()

        

        main_scroll.setWidget(scroll_content)

        layout.addWidget(main_scroll)

        

    def refresh_content(self, characters, favorites):

        self.characters = characters

        self.user_favorites = favorites