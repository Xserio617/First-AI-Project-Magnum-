from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QGraphicsDropShadowEffect, QWidget

from PyQt6.QtCore import Qt, pyqtSignal, QRect

from PyQt6.QtGui import QCursor, QPainter, QColor, QPainterPath, QFont, QBrush, QLinearGradient, QPixmap

from .base import load_avatar_pixmap

import random

import os



class CharacterCard(QFrame):

    """Modern karakter kartı - Character.ai tarzı"""

    

    clicked = pyqtSignal(str)

    

    def __init__(self, name: str, data: dict, is_selected: bool = False, parent=None):

        super().__init__(parent)

        self.name = name

        self.is_selected = is_selected

        self.setup_ui(data)

        

    def setup_ui(self, data: dict):

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setFixedHeight(72)

        

        self._default_style = self._get_style(self.is_selected, False)

        self._hover_style = self._get_style(self.is_selected, True)

        self.setStyleSheet(self._default_style)

        

        layout = QHBoxLayout(self)

        layout.setContentsMargins(12, 10, 12, 10)

        layout.setSpacing(12)

        

        avatar_color = "#2563eb" if self.is_selected else "#374151"

        self.avatar = QLabel()

        self.avatar.setFixedSize(48, 48)

        self.avatar.setPixmap(load_avatar_pixmap(self.name, 48, avatar_color))

        layout.addWidget(self.avatar)

        

        info_layout = QVBoxLayout()

        info_layout.setSpacing(2)

        

        self.name_label = QLabel(self.name)

        self.name_label.setStyleSheet("""

            QLabel {

                color: #f5f5f5;

                font-size: 15px;

                font-weight: 600;

                font-family: 'Segoe UI', sans-serif;

            }

        """)

        info_layout.addWidget(self.name_label)

        

        preview_text = data.get("greeting", "") or data.get("prompt", "")

        preview_text = (preview_text[:40] + "...") if len(preview_text) > 40 else preview_text

        self.preview_label = QLabel(preview_text or "No description")

        self.preview_label.setStyleSheet("""

            QLabel {

                color: #888;

                font-size: 13px;

                font-family: 'Segoe UI', sans-serif;

            }

        """)

        info_layout.addWidget(self.preview_label)

        

        layout.addLayout(info_layout)

        layout.addStretch()

        

    def _get_style(self, selected: bool, hover: bool) -> str:

        if selected:

            bg = "#1e3a5f"

            border = "#2563eb"

        elif hover:

            bg = "#252525"

            border = "transparent"

        else:

            bg = "transparent"

            border = "transparent"

            

        return f"""

            CharacterCard {{

                background-color: {bg};

                border: 2px solid {border};

                border-radius: 12px;

            }}

        """

        

    def enterEvent(self, event):

        if not self.is_selected:

            self.setStyleSheet(self._hover_style)

        super().enterEvent(event)

        

    def leaveEvent(self, event):

        self.setStyleSheet(self._default_style)

        super().leaveEvent(event)

        

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit(self.name)

        super().mousePressEvent(event)



class FeaturedCharacterCard(QFrame):

    """Öne çıkan karakter kartı - büyük, resimli, animasyonlu"""

    

    clicked = pyqtSignal(str)

    

    GRADIENTS = [

        ["#667eea", "#764ba2"],

        ["#f093fb", "#f5576c"],

        ["#4facfe", "#00f2fe"],

        ["#43e97b", "#38f9d7"],

        ["#fa709a", "#fee140"],

        ["#a8edea", "#fed6e3"],

        ["#ff9a9e", "#fecfef"],

        ["#667eea", "#764ba2"],

        ["#f6d365", "#fda085"],

        ["#89f7fe", "#66a6ff"],

    ]

    

    def __init__(self, name: str, data: dict, parent=None):

        super().__init__(parent)

        self.name = name

        self.data = data

        self.gradient = random.choice(self.GRADIENTS)

        self._hovered = False

        self._scale = 1.0

        self._hover_offset = 0

        self.avatar_pixmap = None

        self.load_avatar()

        self.setup_ui()

        

    def load_avatar(self):

        current_dir = os.path.dirname(os.path.abspath(__file__)) 

        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

        

        valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']

        safe_name = "".join([c for c in self.name if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).strip()

        

        for ext in valid_extensions:

            path = os.path.join(project_root, "assets", "avatars", safe_name + ext)

            if os.path.exists(path):

                self.avatar_pixmap = QPixmap(path)

                break

        

    def setup_ui(self):

        self.setFixedSize(160, 200)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setStyleSheet("background: transparent;")

        

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)

        

        spacer = QWidget()

        spacer.setFixedSize(160, 130)

        spacer.setStyleSheet("background: transparent;")

        layout.addWidget(spacer)

        

        info_frame = QFrame()

        info_frame.setFixedHeight(70)

        info_frame.setStyleSheet("background: transparent;")

        info_layout = QVBoxLayout(info_frame)

        info_layout.setContentsMargins(12, 8, 12, 12)

        info_layout.setSpacing(2)

        

        display_name = self.name if len(self.name) <= 18 else self.name[:15] + "..."

        name_label = QLabel(display_name)

        name_label.setStyleSheet("""

            color: #ffffff;

            font-size: 14px;

            font-weight: 600;

            font-family: 'Segoe UI', sans-serif;

            background: transparent;

        """)

        name_label.setWordWrap(False)

        name_label.setMaximumHeight(20)

        info_layout.addWidget(name_label)

        

        desc = self.data.get("greeting", self.data.get("prompt", ""))[:25]

        desc_label = QLabel(desc + "..." if len(desc) == 25 else desc)

        desc_label.setStyleSheet("""

            color: #8e8ea0;

            font-size: 11px;

            font-family: 'Segoe UI', sans-serif;

            background: transparent;

        """)

        desc_label.setWordWrap(False)

        desc_label.setMaximumHeight(16)

        info_layout.addWidget(desc_label)

        

        layout.addWidget(info_frame)

        

        self.shadow = QGraphicsDropShadowEffect()

        self.shadow.setBlurRadius(20)

        self.shadow.setColor(QColor(0, 0, 0, 80))

        self.shadow.setOffset(0, 5)

        self.setGraphicsEffect(self.shadow)

        

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        

        card_path = QPainterPath()

        card_path.addRoundedRect(0, 0, 160, 200, 16, 16)

        painter.setClipPath(card_path)

        painter.setClipPath(card_path)

        

        if self.avatar_pixmap:

            scaled = self.avatar_pixmap.scaled(160, 130, 

                Qt.AspectRatioMode.KeepAspectRatioByExpanding,

                Qt.TransformationMode.SmoothTransformation)

            x = (160 - scaled.width()) // 2

            y = (130 - scaled.height()) // 2

            painter.drawPixmap(x, y, scaled)

        else:

            gradient = QLinearGradient(0, 0, 160, 130)

            gradient.setColorAt(0, QColor(self.gradient[0]))

            gradient.setColorAt(1, QColor(self.gradient[1]))

            

            painter.setBrush(QBrush(gradient))

            painter.setPen(Qt.PenStyle.NoPen)

            painter.drawRect(0, 0, 160, 130)

            

            painter.setPen(QColor(255, 255, 255, 200))

            font = QFont("Segoe UI", 48, QFont.Weight.Bold)

            painter.setFont(font)

            painter.drawText(QRect(0, 0, 160, 130), Qt.AlignmentFlag.AlignCenter, self.name[0].upper())

        

        painter.setBrush(QColor("#1e1e2e"))

        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawRect(0, 130, 160, 70)

        

        painter.setClipping(False)

        

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit(self.name)

        super().mousePressEvent(event)

        

    def enterEvent(self, event):

        self._hovered = True

        self.shadow.setBlurRadius(30)

        self.shadow.setOffset(0, 8)

        self.shadow.setColor(QColor(99, 102, 241, 100))

        self.move(self.x(), self.y() - 5)

        super().enterEvent(event)

        

    def leaveEvent(self, event):

        self._hovered = False

        self.shadow.setBlurRadius(20)

        self.shadow.setOffset(0, 5)

        self.shadow.setColor(QColor(0, 0, 0, 80))

        self.move(self.x(), self.y() + 5)

        super().leaveEvent(event)



class SuggestionCard(QFrame):

    """Öneri kartı - "Try saying" için"""

    

    clicked = pyqtSignal(str)

    

    def __init__(self, text: str, parent=None):

        super().__init__(parent)

        self.text = text

        self.setup_ui()

        

    def setup_ui(self):

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setStyleSheet("""

            SuggestionCard {

                background-color: #2a2a3a;

                border: 1px solid #3a3a4a;

                border-radius: 12px;

            }

            SuggestionCard:hover {

                background-color: #3a3a4a;

                border: 1px solid #4a4a5a;

            }

        """)

        

        layout = QVBoxLayout(self)

        layout.setContentsMargins(16, 12, 16, 12)

        

        label = QLabel(f'"{self.text}"')

        label.setStyleSheet("""

            color: #c0c0c0;

            font-size: 13px;

            font-family: 'Segoe UI', sans-serif;

            font-style: italic;

        """)

        label.setWordWrap(True)

        layout.addWidget(label)

        

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit(self.text)

        super().mousePressEvent(event)



class QuickActionCard(QFrame):

    """Hızlı aksiyon kartı - ikonlu"""

    

    clicked = pyqtSignal(str)

    

    ICONS = {

        "language": "🌍",

        "trip": "✈️",

        "book": "📚",

        "interview": "💼",

        "story": "📝",

        "decision": "🤔",

        "brainstorm": "💡",

        "game": "🎮",

        "escape": "🤖",

    }

    

    COLORS = {

        "language": "#4facfe",

        "trip": "#f093fb",

        "book": "#43e97b",

        "interview": "#fa709a",

        "story": "#667eea",

        "decision": "#f6d365",

        "brainstorm": "#ff9a9e",

        "game": "#89f7fe",

        "escape": "#a8edea",

    }

    

    def __init__(self, action_type: str, text: str, parent=None):

        super().__init__(parent)

        self.action_type = action_type

        self.text = text

        self.setup_ui()

        

    def setup_ui(self):

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setStyleSheet("""

            QuickActionCard {

                background-color: #1e1e2e;

                border: 1px solid #2a2a3a;

                border-radius: 12px;

            }

            QuickActionCard:hover {

                background-color: #2a2a3a;

            }

        """)

        

        layout = QHBoxLayout(self)

        layout.setContentsMargins(16, 12, 16, 12)

        layout.setSpacing(12)

        

        icon_label = QLabel(self.ICONS.get(self.action_type, "✨"))

        icon_label.setStyleSheet(f"""

            background-color: {self.COLORS.get(self.action_type, '#667eea')}33;

            padding: 8px;

            border-radius: 8px;

            font-size: 18px;

        """)

        icon_label.setFixedSize(40, 40)

        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(icon_label)

        

        text_label = QLabel(self.text)

        text_label.setStyleSheet("""

            color: #e0e0e0;

            font-size: 14px;

            font-family: 'Segoe UI', sans-serif;

        """)

        layout.addWidget(text_label)

        layout.addStretch()

        

    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.clicked.emit(self.action_type)

        super().mousePressEvent(event)



class HistoryItem(QPushButton):

    """Sidebar'daki sohbet geçmişi satırı"""

    def __init__(self, char_data, parent=None):

        super().__init__(parent)

        self.setFixedHeight(64)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setStyleSheet("QPushButton { background: transparent; border: none; text-align: left; border-radius: 10px; } QPushButton:hover { background-color: #1e1e1e; }")

        

        layout = QHBoxLayout(self)

        layout.setContentsMargins(12, 8, 12, 8)

        layout.setSpacing(12)

        

        self.avatar = QLabel()

        self.avatar.setFixedSize(44, 44)

        self.avatar.setPixmap(load_avatar_pixmap(char_data['name'], 44, "#6366f1"))

        layout.addWidget(self.avatar)

        

        text_container = QVBoxLayout()

        text_container.setSpacing(2)

        name_label = QLabel(char_data['name'])

        name_label.setStyleSheet("color: #e4e4e7; font-weight: 600; font-size: 14px; border: none;")

        text_container.addWidget(name_label)

        

        preview_label = QLabel("Continue chat...")

        preview_label.setStyleSheet("color: #71717a; font-size: 12px; border: none;")

        text_container.addWidget(preview_label)

        

        layout.addLayout(text_container)

        layout.addStretch()