from PyQt6.QtWidgets import QPushButton, QFrame, QHBoxLayout, QLineEdit, QWidget

from PyQt6.QtCore import Qt, pyqtSignal, QPoint

from PyQt6.QtGui import QCursor, QPainter, QColor, QPen, QBrush, QPainterPath



class ModernButton(QPushButton):

    """Modern buton - animasyonlu"""

    

    def __init__(self, text: str, primary: bool = False, danger: bool = False, parent=None):

        super().__init__(text, parent)

        self.primary = primary

        self.danger = danger

        self.setup_style()

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        

    def setup_style(self):

        if self.primary:

            bg = "#2563eb"

            hover_bg = "#1d4ed8"

            text_color = "white"

        elif self.danger:

            bg = "transparent"

            hover_bg = "#dc2626"

            text_color = "#ef4444"

        else:

            bg = "#333"

            hover_bg = "#444"

            text_color = "#e5e5e5"

            

        self.setStyleSheet(f"""

            QPushButton {{

                background-color: {bg};

                color: {text_color};

                border: none;

                border-radius: 10px;

                padding: 12px 20px;

                font-size: 14px;

                font-weight: 500;

                font-family: 'Segoe UI', sans-serif;

            }}

            QPushButton:hover {{

                background-color: {hover_bg};

                color: white;

            }}

            QPushButton:pressed {{

                background-color: {hover_bg};

            }}

            QPushButton:disabled {{

                background-color: #1a1a1a;

                color: #555;

            }}

        """)



class CategoryTab(QPushButton):

    """Kategori sekmesi butonu"""

    

    def __init__(self, text: str, active: bool = False, parent=None):

        super().__init__(text, parent)

        self.active = active

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setFixedHeight(36)

        self.update_style()

        

    def update_style(self):

        if self.active:

            self.setStyleSheet("""

                QPushButton {

                    background-color: #3b3b4f;

                    color: #ffffff;

                    border: none;

                    border-radius: 18px;

                    padding: 8px 20px;

                    font-size: 13px;

                    font-weight: 600;

                    font-family: 'Segoe UI', sans-serif;

                }

            """)

        else:

            self.setStyleSheet("""

                QPushButton {

                    background-color: transparent;

                    color: #8e8ea0;

                    border: none;

                    border-radius: 18px;

                    padding: 8px 20px;

                    font-size: 13px;

                    font-weight: 500;

                    font-family: 'Segoe UI', sans-serif;

                }

                QPushButton:hover {

                    background-color: #2a2a3a;

                    color: #ffffff;

                }

            """)

            

    def set_active(self, active: bool):

        self.active = active

        self.update_style()



class IconButton(QPushButton):

    """Modern ikon buton - SVG tabanlı güzel ikonlar"""

    

    ICONS = {

        "share": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">

            <path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8"/>

            <polyline points="16 6 12 2 8 6"/>

            <line x1="12" y1="2" x2="12" y2="15"/>

        </svg>''',

        "download": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">

            <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>

            <polyline points="7 10 12 15 17 10"/>

            <line x1="12" y1="15" x2="12" y2="3"/>

        </svg>''',

        "user": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">

            <circle cx="12" cy="8" r="4"/>

            <path d="M4 20c0-4 4-6 8-6s8 2 8 6"/>

        </svg>''',

        "trash": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">

            <path d="M3 6h18M8 6V4a2 2 0 012-2h4a2 2 0 012 2v2"/>

            <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6"/>

            <path d="M10 11v6M14 11v6"/>

        </svg>''',

        "send": '''<svg viewBox="0 0 24 24" fill="currentColor">

            <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>

        </svg>''',

        "plus": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">

            <path d="M12 5v14M5 12h14"/>

        </svg>''',

        "settings": '''<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">

            <circle cx="12" cy="12" r="3"/>

            <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>

        </svg>''',

    }

    

    def __init__(self, icon_name: str, tooltip: str = "", danger: bool = False, parent=None):

        super().__init__(parent)

        self.icon_name = icon_name

        self.danger = danger

        self.setToolTip(tooltip)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setFixedSize(40, 40)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.setup_style()

        

    def setup_style(self):

        if self.danger:

            self.setStyleSheet("""

                QPushButton {

                    background-color: transparent;

                    border: none;

                    border-radius: 8px;

                    outline: none;

                }

                QPushButton:hover {

                    background-color: rgba(239, 68, 68, 0.2);

                }

            """)

            self.icon_color = "#ef4444"

        else:

            self.setStyleSheet("""

                QPushButton {

                    background-color: #2a2a2a;

                    border: none;

                    border-radius: 8px;

                    outline: none;

                }

                QPushButton:hover {

                    background-color: #3a3a3a;

                }

            """)

            self.icon_color = "#a0a0a0"

            

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        

        icon_size = 20

        x = (self.width() - icon_size) // 2

        y = (self.height() - icon_size) // 2

        

        painter.setPen(QColor(self.icon_color))

        painter.setBrush(Qt.BrushStyle.NoBrush)

        

        if self.icon_name == "user":

            painter.drawEllipse(x + 5, y + 2, 10, 10)

            path = QPainterPath()

            path.moveTo(x + 2, y + 18)

            path.quadTo(x + 10, y + 10, x + 18, y + 18)

            painter.drawPath(path)

        elif self.icon_name == "trash":

            painter.drawRect(x + 4, y + 5, 12, 14)

            painter.drawLine(x + 2, y + 5, x + 18, y + 5)

            painter.drawLine(x + 7, y + 2, x + 13, y + 2)

            painter.drawLine(x + 7, y + 2, x + 7, y + 5)

            painter.drawLine(x + 13, y + 2, x + 13, y + 5)

            painter.drawLine(x + 8, y + 8, x + 8, y + 16)

            painter.drawLine(x + 12, y + 8, x + 12, y + 16)

        elif self.icon_name == "plus":

            painter.drawLine(x + 10, y + 3, x + 10, y + 17)

            painter.drawLine(x + 3, y + 10, x + 17, y + 10)

            

        painter.end()



class SearchIconWidget(QWidget):

    """Arama ikonu widget"""

    

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setFixedSize(20, 20)

        

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        

        pen = QPen(QColor("#71717a"), 2)

        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        painter.setPen(pen)

        painter.setBrush(Qt.BrushStyle.NoBrush)

        

        painter.drawEllipse(3, 3, 11, 11)

        painter.drawLine(12, 12, 17, 17)

        

        painter.end()



class SearchBar(QFrame):

    """Modern arama çubuğu"""

    

    search_triggered = pyqtSignal(str)

    

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setup_ui()

        

    def setup_ui(self):

        self.setFixedHeight(44)

        self.setStyleSheet("""

            SearchBar {

                background-color: #2a2a3a;

                border: 1px solid #3a3a4a;

                border-radius: 22px;

            }

        """)

        

        layout = QHBoxLayout(self)

        layout.setContentsMargins(16, 0, 16, 0)

        layout.setSpacing(10)

        

        icon = SearchIconWidget()

        layout.addWidget(icon)

        

        self.input = QLineEdit()

        self.input.setPlaceholderText("Search characters...")

        self.input.setStyleSheet("""

            QLineEdit {

                background: transparent;

                border: none;

                color: #e0e0e0;

                font-size: 14px;

                font-family: 'Segoe UI', sans-serif;

            }

        """)

        self.input.returnPressed.connect(lambda: self.search_triggered.emit(self.input.text()))

        layout.addWidget(self.input)