from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor, QPainterPath, QBrush, QLinearGradient, QPen

class LogoWidget(QWidget):
    """Modern logo widget - gradient ve animasyon"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(48, 48)
        self._angle = 0
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        cx, cy = self.width() // 2, self.height() // 2
        
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#6366f1"))
        gradient.setColorAt(1, QColor("#a855f7"))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(4, 4, 40, 40)
        
        pen = QPen(QColor("white"), 2)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        
        painter.setBrush(QBrush(QColor("white")))
        painter.drawEllipse(cx - 8, cy - 4, 6, 6)
        painter.drawEllipse(cx + 2, cy - 4, 6, 6)
        
        path = QPainterPath()
        path.moveTo(cx - 6, cy + 4)
        path.quadTo(cx, cy + 10, cx + 6, cy + 4)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawPath(path)
        
        painter.end()