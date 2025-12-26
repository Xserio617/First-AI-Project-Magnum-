from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QMenu, QApplication, QPushButton

from PyQt6.QtCore import Qt, pyqtSignal, QTimer

from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QCursor

import re

from .base import load_avatar_pixmap



from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QMenu, QApplication

from PyQt6.QtCore import pyqtSignal, Qt

from PyQt6.QtGui import QAction

import re





class ChatBubble(QFrame):

    """Modern mesaj balonu"""

    

    rewind_requested = pyqtSignal(int)

    

    def __init__(self, text: str, role: str, user_name: str = "You", 

                 char_name: str = "AI", msg_id: int = None, parent=None):

        super().__init__(parent)

        self.msg_id = msg_id

        self.text_content = text

        self.is_user = (role == "user")

        self._current_text = text

        self.setup_ui(user_name, char_name)

        self.update_text(text)

    

    def setup_ui(self, user_name: str, char_name: str):

        main_layout = QHBoxLayout(self)

        main_layout.setContentsMargins(10, 5, 10, 5)

        main_layout.setSpacing(10)

        

        if self.is_user:

            bg_color = "#2563eb"

            text_color = "#ffffff"

            avatar_color = "#1d4ed8"

        else:

            bg_color = "#1e1e1e"

            text_color = "#e5e5e5"

            avatar_color = "#374151"

        

        target_name = user_name if self.is_user else char_name

        self.avatar = QLabel()

        self.avatar.setFixedSize(40, 40)

        

        self.bubble_container = QFrame()

        self.bubble_container.setMaximumWidth(500)

        self.bubble_container.setStyleSheet(f"""

            QFrame {{

                background-color: {bg_color};

                border-radius: 18px;

                padding: 0px;

                border: none;

            }}

        """)

        

        bubble_layout = QVBoxLayout(self.bubble_container)

        bubble_layout.setContentsMargins(16, 12, 16, 12)

        bubble_layout.setSpacing(0)

        

        self.msg_label = QLabel()

        self.msg_label.setWordWrap(True)

        self.msg_label.setTextFormat(Qt.TextFormat.RichText)

        

        self.msg_label.setTextInteractionFlags(

            Qt.TextInteractionFlag.TextSelectableByMouse | 

            Qt.TextInteractionFlag.LinksAccessibleByMouse

        )

        

        self.msg_label.setStyleSheet(f"""

            QLabel {{

                color: {text_color};

                font-size: 14px;

                font-family: 'Segoe UI', sans-serif;

                background: transparent;

                padding: 0px;

                selection-background-color: #555; /* Seçilen metin rengi */

                border: none;

            }}

        """)

        self.msg_label.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        

        self.msg_label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.msg_label.customContextMenuRequested.connect(self.show_context_menu)



        bubble_layout.addWidget(self.msg_label)

        

        if self.is_user:

            main_layout.addStretch()

            main_layout.addWidget(self.bubble_container)

            main_layout.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignTop)

        else:

            main_layout.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignTop)

            main_layout.addWidget(self.bubble_container)

            main_layout.addStretch()

        

    

    def update_text(self, text: str):

        self._current_text = text

        self.text_content = text

        formatted_text = self._format_markdown(text)

        self.msg_label.setText(formatted_text)

    

    def append_text(self, text: str):

        try:

            self._current_text += text

            self.text_content = self._current_text

            formatted_text = self._format_markdown(self._current_text)

            self.msg_label.setText(formatted_text)

        except RuntimeError:

            pass

    

    def _format_markdown(self, text: str) -> str:

        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        text = re.sub(r'\*\*\*(.*?)\*\*\*', r'<b><i>\1</i></b>', text)

        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)

        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)

        text = text.replace("\n", "<br>")

        return text

    

    def show_context_menu(self, pos):

        """Menü artık Label üzerinden tetikleniyor"""

        if self.msg_id is None:

            return

        

        menu = QMenu(self)

        menu.setStyleSheet("""

            QMenu {

                background-color: #1e1e1e;

                border: 1px solid #333;

                border-radius: 8px;

                padding: 5px;

            }

            QMenu::item {

                color: #e5e5e5;

                padding: 8px 20px;

                border-radius: 4px;

            }

            QMenu::item:selected {

                background-color: #333;

            }

        """)

        

        if self.msg_label.hasSelectedText():

            copy_selection_action = menu.addAction("✂️ Copy Selection")

            copy_selection_action.triggered.connect(self.copy_selection)

        

        copy_all_action = menu.addAction("📋 Copy All")

        copy_all_action.triggered.connect(self.copy_text)

        

        rewind_action = menu.addAction("⏪ Rewind to Here")

        rewind_action.triggered.connect(lambda: self.rewind_requested.emit(self.msg_id))

        

        menu.exec(self.msg_label.mapToGlobal(pos))

    

    def copy_selection(self):

        """Sadece seçili kısmı kopyalar"""

        clipboard = QApplication.clipboard()

        clipboard.setText(self.msg_label.selectedText())



    def copy_text(self):

        """Tüm metni kopyalar"""

        clipboard = QApplication.clipboard()

        clipboard.setText(self.text_content)

    

    def set_message_id(self, msg_id: int):

        self.msg_id = msg_id



class TypingIndicator(QFrame):

    """AI yazıyor animasyonu görseli"""

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setFixedSize(70, 35)

        self.setStyleSheet("background-color: #1f2937; border-radius: 15px; border: none;")

        layout = QHBoxLayout(self)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lbl = QLabel("...")

        self.lbl.setStyleSheet("color: #10a37f; font-weight: bold; font-size: 18px; border: none;")

        layout.addWidget(self.lbl)

        

        self.dots = [QLabel("●") for _ in range(3)]

        self.current_dot = 0

        



class SendButton(QPushButton):

    """Modern gönder butonu - Yeşil ok"""

    

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.setFixedSize(40, 40)

        self.setStyleSheet("""

            QPushButton {

                background-color: #10a37f;

                border: none;

                border-radius: 8px;

            }

            QPushButton:hover {

                background-color: #0e906f;

            }

            QPushButton:disabled {

                background-color: #1a3a2f;

            }

        """)

        

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        

        painter.setPen(Qt.PenStyle.NoPen)

        painter.setBrush(QBrush(QColor("white")))

        

        path = QPainterPath()

        cx, cy = self.width() // 2, self.height() // 2

        path.moveTo(cx - 6, cy - 6)

        path.lineTo(cx + 6, cy)

        path.lineTo(cx - 6, cy + 6)

        path.lineTo(cx - 3, cy)

        path.closeSubpath()

        

        painter.drawPath(path)

        painter.end()