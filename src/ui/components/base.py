import os

from functools import lru_cache

from PyQt6.QtGui import QPixmap, QPainter, QPainterPath, QBrush, QColor, QFont, QLinearGradient

from PyQt6.QtCore import Qt, QRect

from PyQt6.QtWidgets import QScrollArea, QFrame



@lru_cache(maxsize=32)

def load_avatar_pixmap(name: str, size: int, fallback_color: str) -> QPixmap:

    """Avatar resmi yükler veya oluşturur (önbellekli)"""

    current_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))

    

    valid_extensions = ['.png', '.jpg', '.jpeg', '.webp']

    image_path = None

    

    safe_name = "".join([c for c in name if c.isalpha() or c.isdigit() or c in (' ', '_', '-')]).strip()

    

    for ext in valid_extensions:

        path = os.path.join(project_root, "assets", "avatars", safe_name + ext)

        if os.path.exists(path):

            image_path = path

            break

    

    pixmap = QPixmap(size, size)

    pixmap.fill(Qt.GlobalColor.transparent)

    

    painter = QPainter(pixmap)

    painter.setRenderHint(QPainter.RenderHint.Antialiasing)

    

    path = QPainterPath()

    path.addEllipse(0, 0, size, size)

    painter.setClipPath(path)

    

    if image_path:

        img = QPixmap(image_path)

        scaled_img = img.scaled(size, size, Qt.AspectRatioMode.KeepAspectRatioByExpanding, 

                               Qt.TransformationMode.SmoothTransformation)

        painter.drawPixmap(0, 0, scaled_img)

    else:

        painter.setBrush(QBrush(QColor(fallback_color)))

        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(0, 0, size, size)

        

        painter.setPen(QColor("white"))

        font = QFont("Segoe UI", int(size/2.5), QFont.Weight.Bold)

        painter.setFont(font)

        painter.drawText(QRect(0, 0, size, size), Qt.AlignmentFlag.AlignCenter, name[0].upper())

    

    painter.end()

    return pixmap



class SmoothScrollArea(QScrollArea):

    """Smooth scroll ile ScrollArea - Hem Yatay Hem Dikey Destekli"""

    

    def __init__(self, orientation="vertical", parent=None):

        super().__init__(parent)

        self.setWidgetResizable(True)

        self.setFrameShape(QFrame.Shape.NoFrame)

        

        if orientation == "horizontal":

            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        else:

            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

            

        self.setStyleSheet("""

            QScrollArea {

                border: none;

                background-color: transparent;

            }

            QScrollBar:vertical {

                background-color: #0a0a0a;

                width: 8px;

                border-radius: 4px;

                margin: 0px;

            }

            QScrollBar::handle:vertical {

                background-color: #333;

                border-radius: 4px;

                min-height: 30px;

            }

            QScrollBar::handle:vertical:hover {

                background-color: #444;

            }

            QScrollBar:horizontal {

                background-color: #0a0a0a;

                height: 8px;

                border-radius: 4px;

                margin: 0px;

            }

            QScrollBar::handle:horizontal {

                background-color: #333;

                border-radius: 4px;

                min-width: 30px;

            }

            QScrollBar::handle:horizontal:hover {

                background-color: #444;

            }

            QScrollBar::add-line, QScrollBar::sub-line {

                height: 0px;

                width: 0px;

            }

            QScrollBar::add-page, QScrollBar::sub-page {

                background: none;

            }

        """)

        

    def scroll_to_bottom(self):

        """En alta kaydır"""

        scrollbar = self.verticalScrollBar()

        scrollbar.setValue(scrollbar.maximum())



class GradientFrame(QFrame):

    def __init__(self, colors=None, parent=None):

        super().__init__(parent)

        self.colors = colors or ["#1a1a2e", "#16213e", "#0f3460"]

        

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, self.width(), self.height())

        for i, color in enumerate(self.colors):

            gradient.setColorAt(i / max(len(self.colors) - 1, 1), QColor(color))

        

        painter.setBrush(QBrush(gradient))

        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawRect(self.rect())