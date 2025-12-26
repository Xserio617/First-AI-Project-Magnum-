from PyQt6.QtWidgets import (

    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 

    QLineEdit, QPushButton, QLabel, QFrame, QMessageBox, QCheckBox

)

from PyQt6.QtCore import Qt, pyqtSignal

from src.database import DatabaseManager

from src.ui.components import CustomTitleBar, LogoWidget

from src.auth_manager import AuthManager



class AuthWindow(QMainWindow):

    character_saved = pyqtSignal(dict)

    login_successful = pyqtSignal(dict)



    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Login")

        self.setFixedSize(400, 600)

        self.is_login_mode = True 

        self.db = DatabaseManager()

        self.setup_ui()

        self.avatar_path = None



    def setup_ui(self):

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        

        main_container = QWidget()

        main_container.setObjectName("MainContainer")

        main_container.setStyleSheet("""

            QWidget#MainContainer {

                background-color: #09090b; 

                border: 1px solid #27272a;

                border-radius: 12px;

            }

        """)

        self.setCentralWidget(main_container)

        

        main_layout = QVBoxLayout(main_container)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(0)

        

        self.title_bar = CustomTitleBar(self)

        btn_max = self.title_bar.findChild(QPushButton, "btn_max")

        if btn_max: btn_max.hide()

        

        self.title_bar.findChild(QLabel).setText("Magnum AI - Login")

        self.title_bar.setStyleSheet("""

            QFrame {

                background-color: transparent; 

                border-bottom: 1px solid #27272a;

                border-top-left-radius: 12px;

                border-top-right-radius: 12px;

            }

        """)

        main_layout.addWidget(self.title_bar)

        

        content_widget = QWidget()

        content_layout = QVBoxLayout(content_widget)

        content_layout.setContentsMargins(40, 20, 40, 40)

        content_layout.setSpacing(20)

        

        logo_container = QHBoxLayout()

        logo_container.addStretch()

        logo = LogoWidget()

        logo_container.addWidget(logo)

        logo_container.addStretch()

        content_layout.addLayout(logo_container)

        

        self.title_label = QLabel("Welcome Back")

        self.title_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold; font-family: 'Segoe UI';")

        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(self.title_label)

        

        self.subtitle_label = QLabel("Enter the AI world")

        self.subtitle_label.setStyleSheet("color: #a1a1aa; font-size: 14px; font-family: 'Segoe UI';")

        self.subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        content_layout.addWidget(self.subtitle_label)

        

        self.input_username = QLineEdit()

        self.input_username.setPlaceholderText("Username")

        self.input_username.setFixedHeight(45)

        self.input_username.setStyleSheet(self._get_input_style())

        content_layout.addWidget(self.input_username)

        

        self.input_password = QLineEdit()

        self.input_password.setPlaceholderText("Password")

        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.input_password.setFixedHeight(45)

        self.input_password.setStyleSheet(self._get_input_style())

        content_layout.addWidget(self.input_password)



        self.chk_remember = QCheckBox("Remember Me")

        self.chk_remember.setCursor(Qt.CursorShape.PointingHandCursor)

        self.chk_remember.setStyleSheet("""

            QCheckBox { color: #a1a1aa; font-size: 13px; }

            QCheckBox::indicator { width: 18px; height: 18px; border: 1px solid #3f3f46; border-radius: 4px; background: #27272a; }

            QCheckBox::indicator:checked { background-color: #6366f1; border-color: #6366f1; }

        """)

        content_layout.addWidget(self.chk_remember)

        

        self.btn_action = QPushButton("Login")

        self.btn_action.setFixedHeight(45)

        self.btn_action.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_action.setStyleSheet("""

            QPushButton {

                background-color: #6366f1;

                color: white;

                border: none;

                border-radius: 8px;

                font-weight: bold;

                font-size: 14px;

            }

            QPushButton:hover { background-color: #4f46e5; }

        """)

        self.btn_action.clicked.connect(self.handle_auth)

        content_layout.addWidget(self.btn_action)

        

        self.btn_toggle = QPushButton("Don't have an account? Register")

        self.btn_toggle.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_toggle.setStyleSheet("color: #a1a1aa; background: transparent; border: none;")

        self.btn_toggle.clicked.connect(self.toggle_mode)

        content_layout.addWidget(self.btn_toggle)

        

        content_layout.addStretch()

        main_layout.addWidget(content_widget)



    def _get_input_style(self):

        return """

            QLineEdit, QTextEdit {

                background-color: #27272a; color: white;

                border: 1px solid #3f3f46; border-radius: 8px; padding: 8px;

                selection-background-color: #6366f1;

            }

            QLineEdit:focus, QTextEdit:focus { border: 1px solid #6366f1; }

        """



    def toggle_mode(self):

        self.is_login_mode = not self.is_login_mode

        

        if self.is_login_mode:

            self.title_label.setText("Welcome")

            self.subtitle_label.setText("Login to continue")

            self.btn_action.setText("Login")

            self.btn_toggle.setText("Don't have an account? Register")

            self.chk_remember.show()

        else:

            self.title_label.setText("Create Account")

            self.subtitle_label.setText("Register to start your journey")

            self.btn_action.setText("Register")

            self.btn_toggle.setText("Already have an account? Login")

            self.chk_remember.hide()

            

    def handle_auth(self):

        username = self.input_username.text().strip()

        password = self.input_password.text().strip()

        

        if not username or not password:

            QMessageBox.warning(self, "Error", "Please fill in all fields.")

            return

            

        if self.is_login_mode:

            success, result = self.db.login_user(username, password)

            if success:

                user_data = {"id": result, "username": username}

                

                is_remember = self.chk_remember.isChecked()

                AuthManager.save_session(result, is_remember)



                self.login_successful.emit(user_data)

                self.close()

            else:

                QMessageBox.warning(self, "Error", result)

        else:

            success, msg = self.db.register_user(username, password)

            if success:

                QMessageBox.information(self, "Success", msg)

                self.toggle_mode()

            else:

                QMessageBox.warning(self, "Error", msg)