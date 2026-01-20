from PyQt6.QtWidgets import QPushButton

from PyQt6.QtCore import Qt

from PyQt6.QtGui import QPainter, QColor, QPainterPath, QPen, QBrush, QCursor



class SidebarIconButton(QPushButton):

    """Modern sidebar ikon butonu - Custom paint ile çizilen ikonlar"""

    

    def __init__(self, icon_type: str, tooltip: str = "", active: bool = False, parent=None):

        super().__init__(parent)

        self.icon_type = icon_type

        self.active = active

        self.setToolTip(tooltip)

        self.setFixedSize(48, 48)

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self._hovered = False

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.update_style()

        

    def update_style(self):

        bg = "#27272a" if self.active else "transparent"

        self.setStyleSheet(f"""

            QPushButton {{ 

                background-color: {bg}; 

                border: none; 

                outline: none; 

                border-radius: 12px; 

            }} 

            QPushButton:hover {{ 

                background-color: #1f1f23; 

                border: none;

                outline: none;

            }}

            QPushButton:focus {{

                border: none;

                outline: none;

            }}

        """)

    

    def set_active(self, active: bool):

        self.active = active

        self.update_style()

        self.update()

        

    def enterEvent(self, event):

        self._hovered = True

        self.update()

        super().enterEvent(event)

        

    def leaveEvent(self, event):

        self._hovered = False

        self.update()

        super().leaveEvent(event)

        

    def paintEvent(self, event):

        super().paintEvent(event)

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        

        if self.active:

            color = QColor("#a78bfa")

        elif self._hovered:

            color = QColor("#e4e4e7")

        else:

            color = QColor("#71717a")

        

        pen = QPen(color, 2)

        pen.setCapStyle(Qt.PenCapStyle.RoundCap)

        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)

        painter.setPen(pen)

        

        cx, cy = self.width() // 2, self.height() // 2

        

        if self.icon_type == "home":

            path = QPainterPath()

            path.moveTo(cx, cy - 10)

            path.lineTo(cx - 10, cy)

            path.lineTo(cx - 7, cy)

            path.lineTo(cx - 7, cy + 8)

            path.lineTo(cx + 7, cy + 8)

            path.lineTo(cx + 7, cy)

            path.lineTo(cx + 10, cy)

            path.closeSubpath()

            painter.drawPath(path)

            painter.drawRect(cx - 2, cy + 2, 4, 6)

            

        elif self.icon_type == "chat":

            path = QPainterPath()

            path.addRoundedRect(cx - 10, cy - 8, 20, 14, 4, 4)

            painter.drawPath(path)

            painter.drawLine(cx - 4, cy + 6, cx - 8, cy + 10)

            painter.setBrush(QBrush(color))

            painter.drawEllipse(cx - 5, cy - 2, 3, 3)

            painter.drawEllipse(cx - 1, cy - 2, 3, 3)

            painter.drawEllipse(cx + 3, cy - 2, 3, 3)

            

        elif self.icon_type == "create":

            painter.drawLine(cx, cy - 8, cx, cy + 8)

            painter.drawLine(cx - 8, cy, cx + 8, cy)

            painter.drawLine(cx - 5, cy - 5, cx + 5, cy + 5)

            painter.drawLine(cx + 5, cy - 5, cx - 5, cy + 5)

            

        elif self.icon_type == "settings":

            painter.drawEllipse(cx - 4, cy - 4, 8, 8)

            for i in range(6):

                import math

                angle = i * 60 * math.pi / 180

                x1 = cx + int(6 * math.cos(angle))

                y1 = cy + int(6 * math.sin(angle))

                x2 = cx + int(10 * math.cos(angle))

                y2 = cy + int(10 * math.sin(angle))

                painter.drawLine(x1, y1, x2, y2)

                

        elif self.icon_type == "user":

            painter.drawEllipse(cx - 5, cy - 10, 10, 10)

            path = QPainterPath()

            path.moveTo(cx - 10, cy + 10)

            path.quadTo(cx - 10, cy, cx, cy + 2)

            path.quadTo(cx + 10, cy, cx + 10, cy + 10)

            painter.drawPath(path)

            

        elif self.icon_type == "robot":

            painter.drawRoundedRect(cx - 8, cy - 6, 16, 14, 3, 3)

            painter.setBrush(QBrush(color))

            painter.drawEllipse(cx - 5, cy - 2, 4, 4)

            painter.drawEllipse(cx + 1, cy - 2, 4, 4)

            painter.drawLine(cx, cy - 6, cx, cy - 10)

            painter.drawEllipse(cx - 2, cy - 12, 4, 4)

            

        elif self.icon_type == "trash":

            painter.drawRect(cx - 6, cy - 4, 12, 12)

            painter.drawLine(cx - 8, cy - 4, cx + 8, cy - 4)

            painter.drawLine(cx - 4, cy - 7, cx + 4, cy - 7)

            painter.drawLine(cx - 3, cy - 1, cx - 3, cy + 5)

            painter.drawLine(cx, cy - 1, cx, cy + 5)

            painter.drawLine(cx + 3, cy - 1, cx + 3, cy + 5)

            

        elif self.icon_type == "back":

            path = QPainterPath()

            path.moveTo(cx + 6, cy - 8)

            path.lineTo(cx - 6, cy)

            path.lineTo(cx + 6, cy + 8)

            painter.drawPath(path)

            

        elif self.icon_type == "search":

            painter.drawEllipse(cx - 7, cy - 7, 12, 12)

            painter.drawLine(cx + 3, cy + 3, cx + 8, cy + 8)

            

        elif self.icon_type == "heart":

            path = QPainterPath()

            path.moveTo(cx, cy + 8)

            path.cubicTo(cx - 10, cy, cx - 10, cy - 8, cx, cy - 4)

            path.cubicTo(cx + 10, cy - 8, cx + 10, cy, cx, cy + 8)

            if hasattr(self, 'filled') and self.filled:

                painter.setBrush(QBrush(QColor("#ef4444")))

                painter.setPen(QPen(QColor("#ef4444"), 2))

            painter.drawPath(path)

            

        elif self.icon_type == "heart_filled":

            path = QPainterPath()

            path.moveTo(cx, cy + 8)

            path.cubicTo(cx - 10, cy, cx - 10, cy - 8, cx, cy - 4)

            path.cubicTo(cx + 10, cy - 8, cx + 10, cy, cx, cy + 8)

            painter.setBrush(QBrush(QColor("#ef4444")))

            painter.setPen(QPen(QColor("#ef4444"), 2))

            painter.drawPath(path)

        

        painter.end()



class NavButton(QPushButton):

    """Sol sidebar navigasyon butonu"""

    

    def __init__(self, icon: str, text: str, active: bool = False, parent=None):

        super().__init__(f"  {icon}   {text}", parent)

        self.icon = icon

        self.text_content = text

        self.active = active

        self.setCursor(Qt.CursorShape.PointingHandCursor)

        self.setFixedHeight(44)

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.update_style()

        

    def update_style(self):

        bg = "#2a2a3a" if self.active else "transparent"

        color = "#ffffff" if self.active else "#8e8ea0"

        self.setStyleSheet(f"""

            QPushButton {{

                background-color: {bg};

                color: {color};

                border: none;

                outline: none; /* Gri odaklanma çizgisini siler */

                border-radius: 10px;

                padding: 10px 16px;

                text-align: left;

                font-size: 14px;

                font-weight: 500;

                font-family: 'Segoe UI', sans-serif;

            }}

            QPushButton:hover {{

                background-color: #2a2a3a;

                color: #ffffff;

                border: none;

                outline: none;

            }}

            QPushButton:focus {{

                border: none;

                outline: none; /* Tıklandığında çıkan kalıntı çizgiyi siler */

            }}

        """)

        self.setText(f"  {self.icon}   {self.text_content}")

        

    def set_active(self, active: bool):

        self.active = active

        self.update_style()