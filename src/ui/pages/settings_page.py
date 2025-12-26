from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout

from PyQt6.QtCore import Qt

from src.ui.components import ModernButton



class SettingsPage(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(40, 40, 40, 40)

        layout.setSpacing(20)

        

        title = QLabel("Settings")

        title.setStyleSheet("color: white; font-size: 28px; font-weight: bold;")

        layout.addWidget(title)

        

        group_box = QFrame()

        group_box.setStyleSheet("background-color: #1e1e2e; border-radius: 12px;")

        group_layout = QVBoxLayout(group_box)

        group_layout.setContentsMargins(20, 20, 20, 20)

        

        lbl_theme = QLabel("Appearance Mode")

        lbl_theme.setStyleSheet("color: #e0e0e0; font-size: 16px;")

        group_layout.addWidget(lbl_theme)

        

        btn_layout = QHBoxLayout()

        btn_dark = ModernButton("Dark Mode", primary=True)

        btn_light = ModernButton("Light Mode")

        btn_layout.addWidget(btn_dark)

        btn_layout.addWidget(btn_light)

        btn_layout.addStretch()

        

        group_layout.addLayout(btn_layout)

        layout.addWidget(group_box)

        

        layout.addStretch()

        

        logout_btn = ModernButton("Logout", danger=True)

        layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignLeft)