from PyQt6.QtWidgets import QFrame, QPushButton, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt, QRectF, QByteArray
from PyQt6.QtGui import QPainter, QColor
try:
    from PyQt6.QtSvg import QSvgRenderer
except ImportError:
    QSvgRenderer = None

class WindowButton(QPushButton):
    """Windows 11 Tarzı SVG İkonlu Pencere Butonları"""
    
    ICONS = {
        "min": '''<svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1">
            <path d="M1 5h8" stroke-linecap="round"/>
        </svg>''',
        
        "max": '''<svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1">
            <rect x="1.5" y="1.5" width="7" height="7" rx="0.5"/>
        </svg>''',
        
        "restore": '''<svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1">
            <path d="M3.5 3.5v-2h5v5h-2"/>
            <rect x="1.5" y="3.5" width="5" height="5" rx="0.5"/>
        </svg>''',
        
        "close": '''<svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.2">
            <path d="M2.5 2.5l5 5M7.5 2.5l-5 5" stroke-linecap="round"/>
        </svg>'''
    }

    def __init__(self, btn_type: str, parent=None):
        super().__init__(parent)
        self.btn_type = btn_type
        self.setFixedSize(46, 32)
        self.setStyleSheet("background: transparent; border: none; outline: none;")
        self._hovered = False
        
        if btn_type == "max":
            self.setObjectName("btn_max")

    def enterEvent(self, event):
        self._hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hovered = False
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._hovered:
            if self.btn_type == "close":
                painter.fillRect(self.rect(), QColor("#c42b1c"))
            else:
                painter.fillRect(self.rect(), QColor("#2d2d2d"))
        
        if self.btn_type == "close" and self._hovered:
            icon_color = "#ffffff"
        else:
            icon_color = "#ffffff" if self._hovered else "#999999"

        current_icon_svg = self.ICONS.get(self.btn_type)
        
        if self.btn_type == "max":
            is_maximized = False
            if self.window().windowHandle(): 
                 is_maximized = (self.window().windowState() & Qt.WindowState.WindowMaximized)
            
            if is_maximized:
                current_icon_svg = self.ICONS["restore"]
            else:
                current_icon_svg = self.ICONS["max"]

        if current_icon_svg:
            colored_svg = current_icon_svg.replace("currentColor", icon_color)
            
            if QSvgRenderer:
                renderer = QSvgRenderer(QByteArray(colored_svg.encode()))
                
                icon_size = 10 
                x = int((self.width() - icon_size) / 2)
                y = int((self.height() - icon_size) / 2)
                
                renderer.render(painter, QRectF(x, y, icon_size, icon_size))
        
        painter.end()

class CustomTitleBar(QFrame):
    """Özel pencere başlık çubuğu"""
    def __init__(self, parent_window):
        super().__init__(parent_window)
        self.parent_window = parent_window
        self.setFixedHeight(32)
        self.setStyleSheet("background-color: #0f0f10; border-bottom: 1px solid #27272a;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 0, 0)
        layout.setSpacing(10)
        
        title = QLabel("AI Chat")
        title.setStyleSheet("color: #e4e4e7; font-family: 'Segoe UI'; font-size: 12px; font-weight: 600; border: none; outline: none;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        btn_min = WindowButton("min", self)
        btn_min.clicked.connect(self.parent_window.showMinimized)
        
        btn_max = WindowButton("max", self)
        btn_max.setObjectName("btn_max")
        btn_max.clicked.connect(self.toggle_maximize)
        
        btn_close = WindowButton("close", self)
        btn_close.clicked.connect(self.parent_window.close)
        
        layout.addWidget(btn_min)
        layout.addWidget(btn_max)
        layout.addWidget(btn_close)
        
        self.start_pos = None

    def toggle_maximize(self):
        if self.parent_window.isMaximized():
            self.parent_window.showNormal()
        else:
            self.parent_window.showMaximized()
        
        self.findChild(WindowButton, "btn_max").update()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.start_pos:
            delta = event.globalPosition().toPoint() - self.start_pos
            self.parent_window.move(self.parent_window.pos() + delta)
            self.start_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.start_pos = None
    
    def mouseDoubleClickEvent(self, event):
        self.toggle_maximize()