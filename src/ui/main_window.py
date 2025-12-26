"""

Modern PyQt6 Main Window - Character.ai Style

Updated: Modular Pages, Settings & Horizontal Scroll

"""



import sys

import json

import os

import shutil

from PyQt6.QtWidgets import (

    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 

    QTextEdit, QPushButton, QLabel, QFrame, 

    QMessageBox, QSizePolicy, QApplication, QStackedWidget,

    QScrollArea, QListWidget, QListWidgetItem, QFileDialog

)

from PyQt6.QtCore import Qt, pyqtSignal, QThread, QTimer, QSize

from PyQt6.QtGui import QIcon, QColor



from src.utils import image_to_base64

from src.config import CHAR_FILE, USER_FILE, DEFAULT_CHAR, DEFAULT_USER

from src.database import DatabaseManager, load_json, save_json

from src.ai_engine import AIEngine

from src.ui.popups import CharacterPopup, PersonaPopup



from src.ui.components import (

    ChatBubble, SidebarIconButton, LogoWidget, CustomTitleBar, SendButton, SmoothScrollArea

)

from src.ui.pages.home_page import HomePage

from src.ui.pages.settings_page import SettingsPage

from src.ui.pages.profile_page import ProfilePage 



class ChatRowWidget(QWidget):

    def __init__(self, name, last_message, avatar_char, on_pin_click, on_delete_click):

        super().__init__()

        self.layout = QHBoxLayout(self)

        self.layout.setContentsMargins(15, 12, 15, 12) 

        self.layout.setSpacing(15)



        self.avatar = QLabel(avatar_char)

        self.avatar.setFixedSize(50, 50)

        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.avatar.setStyleSheet("""

            QLabel {

                background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1e1e2e, stop:1 #6366f1);

                color: white; border-radius: 25px; font-size: 20px; font-weight: bold; border: 1px solid #3f3f46; padding: 0px;

            }

        """)

        self.layout.addWidget(self.avatar)



        self.text_layout = QVBoxLayout()

        self.text_layout.setSpacing(4)

        self.name_label = QLabel(name)

        self.name_label.setStyleSheet("color: white; font-size: 16px; font-weight: 700; background: transparent;")

        self.msg_label = QLabel(last_message)

        self.msg_label.setStyleSheet("color: #94a3b8; font-size: 13px; background: transparent;")

        self.msg_label.setWordWrap(False)

        self.text_layout.addWidget(self.name_label)

        self.text_layout.addWidget(self.msg_label)

        self.layout.addLayout(self.text_layout)

        self.layout.addStretch()



        self.btn_pin = QPushButton("⋮") 

        self.btn_pin.setFixedSize(32, 32)

        self.btn_pin.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_pin.setStyleSheet("QPushButton { background-color: transparent; color: #71717a; border: none; font-size: 22px; border-radius: 16px; } QPushButton:hover { background-color: #27272a; color: white; }")

        self.btn_pin.clicked.connect(on_pin_click)

        self.layout.addWidget(self.btn_pin)



        self.btn_delete = SidebarIconButton("trash", tooltip="Delete Chat")

        self.btn_delete.setFixedSize(32, 32) 

        self.btn_delete.clicked.connect(on_delete_click)

        self.layout.addWidget(self.btn_delete)



class AIWorker(QThread):

    token_received = pyqtSignal(str)

    finished = pyqtSignal()

    error = pyqtSignal(str)



    def __init__(self, engine, system_prompt, user_persona, history, message):

        super().__init__()

        self.engine, self.system_prompt, self.user_persona, self.history, self.message = engine, system_prompt, user_persona, history, message

        self.stop_flag = False



    def run(self):

        try:

            stream = self.engine.generate_response_stream(

                self.system_prompt, self.user_persona, self.history, self.message

            )

            for chunk in stream:

                if self.stop_flag: break

                if 'message' in chunk and 'content' in chunk['message']:

                    self.token_received.emit(chunk['message']['content'])

            self.finished.emit()

        except Exception as e:

            self.error.emit(str(e))



class MainApp(QMainWindow):

    logout_requested = pyqtSignal()

    def __init__(self, user_id=None, username="Guest"):

        super().__init__()

        self.setWindowTitle("AI Chat")

        self.resize(1400, 900)

        self.setMinimumSize(1100, 700)

        

        self.current_user_id = user_id 

        self.current_username = username

        

        self.db = DatabaseManager()

        self.ai = AIEngine()

        



        self.characters = load_json(CHAR_FILE, DEFAULT_CHAR)



        local_user_data = load_json(USER_FILE, DEFAULT_USER)

        



        db_personas = []

        if self.current_user_id:

            try:

                db_personas = self.db.get_user_personas(self.current_user_id)

            except Exception as e:

                print(f"Could not retrieve personas from database: {e}")





        if db_personas:

            self.user_data = {

                "username": self.current_username,  

                "personas": db_personas,

                "favorites": local_user_data.get("favorites", [])

            }

        else:

            self.user_data = local_user_data

            self.user_data["username"] = self.current_username



        if "favorites" not in self.user_data:

            self.user_data["favorites"] = []

            

        self.current_char = None

        self.is_generating = False

        self.current_ai_bubble = None

        

        self.setup_ui()



    def setup_ui(self):

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        

        main_widget = QWidget()

        main_widget.setStyleSheet("background-color: #18181b; border: 1px solid #27272a;")

        self.setCentralWidget(main_widget)

        

        main_layout = QVBoxLayout(main_widget)

        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.setSpacing(0)

        

        self.title_bar = CustomTitleBar(self)

        main_layout.addWidget(self.title_bar)

        

        content_area = QWidget()

        content_layout = QHBoxLayout(content_area)

        content_layout.setSpacing(0)

        content_layout.setContentsMargins(1, 0, 1, 1)

        

        self.sidebar = self.create_sidebar()

        content_layout.addWidget(self.sidebar)

        

        self.content_stack = QStackedWidget()

        self.content_stack.setStyleSheet("background-color: #18181b; border: none;")

        

        self.home_page = HomePage(self.characters, self.user_data["favorites"])

        self.home_page.character_selected.connect(self.select_character)

        self.home_page.profile_clicked.connect(lambda: self.switch_page("profile")) 

        self.content_stack.addWidget(self.home_page)

        

        self.chat_page = self.create_chat_page()

        self.content_stack.addWidget(self.chat_page)



        self.chats_list_page = self.setup_chats_list_page()

        self.content_stack.addWidget(self.chats_list_page)

        

        self.settings_page = SettingsPage()

        self.content_stack.addWidget(self.settings_page)



        self.profile_page = ProfilePage(self.user_data, self.characters)

        self.profile_page.character_selected.connect(self.select_character)

        self.profile_page.create_character_clicked.connect(self.open_character_popup)

        self.profile_page.edit_persona_clicked.connect(self.open_persona_popup)

        self.profile_page.logout_clicked.connect(self.handle_logout)

        

        self.content_stack.addWidget(self.profile_page)

        

        content_layout.addWidget(self.content_stack)

        main_layout.addWidget(content_area)



    def create_sidebar(self) -> QFrame:

        sidebar = QFrame()

        sidebar.setFixedWidth(80) 

        sidebar.setStyleSheet("background-color: #09090b; border-right: 1px solid #27272a;")

        

        main_layout = QVBoxLayout(sidebar)

        main_layout.setContentsMargins(10, 20, 10, 20)

        main_layout.setSpacing(15)



        self.logo = LogoWidget() 

        main_layout.addWidget(self.logo, alignment=Qt.AlignmentFlag.AlignCenter)

        main_layout.addSpacing(10)



        self.nav_container = QWidget()

        self.nav_container.setStyleSheet("background: transparent; border: none; outline: none;") 

        self.nav_container.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        nav_layout = QVBoxLayout(self.nav_container)

        nav_layout.setContentsMargins(0,0,0,0)

        

        self.btn_home = SidebarIconButton("home", tooltip="Home", active=True)

        self.btn_home.clicked.connect(lambda: self.switch_page("home"))

        nav_layout.addWidget(self.btn_home)

        

        self.btn_chat = SidebarIconButton("chat", tooltip="Chats")

        self.btn_chat.clicked.connect(lambda: self.switch_page("chats_list"))

        nav_layout.addWidget(self.btn_chat)

        

        main_layout.addWidget(self.nav_container)

        main_layout.addStretch()

        

        self.btn_settings = SidebarIconButton("settings", tooltip="Settings")

        self.btn_settings.clicked.connect(lambda: self.switch_page("settings"))

        main_layout.addWidget(self.btn_settings)

        

        self.btn_user = SidebarIconButton("user", tooltip="Profile")

        self.btn_user.clicked.connect(lambda: self.switch_page("profile"))

        main_layout.addWidget(self.btn_user)

        

        return sidebar



    def switch_page(self, page_name):

        page_map = {"home": 0, "chat": 1, "chats_list": 2, "settings": 3, "profile": 4}

        index = 0

        if isinstance(page_name, int):

            index = page_name

        else:

            key = str(page_name).strip().lower()

            if key.isdigit(): index = int(key)

            elif key in page_map: index = page_map[key]

            else: return



        self.content_stack.setCurrentIndex(index)

        

        if hasattr(self, 'btn_home'): self.btn_home.set_active(index == 0)

        if hasattr(self, 'btn_chat'): self.btn_chat.set_active(index == 1 or index == 2)

        if hasattr(self, 'btn_settings'): self.btn_settings.set_active(index == 3)

        if hasattr(self, 'btn_user'): self.btn_user.set_active(index == 4)

        

        if index == 2: 

            self.refresh_chats_list()

        elif index == 4: 

            self.profile_page.refresh_content(self.user_data, self.characters)



    def handle_logout(self):

        from src.auth_manager import AuthManager

        AuthManager.clear_session()



        self.logout_requested.emit() 

        self.close()



    def setup_chats_list_page(self):

        page_widget = QWidget()

        page_widget.setStyleSheet("background-color: #09090b;") 

        layout = QVBoxLayout(page_widget)

        layout.setContentsMargins(0, 0, 0, 0)

        header = QLabel("Chats")

        header.setStyleSheet("color: #e9edef; font-size: 24px; font-weight: bold; padding: 20px;")

        layout.addWidget(header)

        self.chat_list_widget = QListWidget()

        self.chat_list_widget.setStyleSheet("QListWidget { border: none; background-color: transparent; outline: none; } QListWidget::item { background-color: #18181b; border: 1px solid #27272a; border-radius: 15px; margin-bottom: 12px; padding: 5px; } QListWidget::item:hover { background-color: #1e1e2e; border: 1px solid #6366f1; } QListWidget::item:selected { background-color: #1e1e2e; border: 1px solid #a855f7; }")

        self.chat_list_widget.itemClicked.connect(self.on_chat_row_clicked)

        layout.addWidget(self.chat_list_widget)

        self.refresh_chats_list()

        return page_widget



    def refresh_chats_list(self):

        self.chat_list_widget.clear()

        try:

            real_chats = []

            for char_name in self.characters:

                history = self.db.get_history(char_name)

                if history and len(history) > 0:

                    last_msg_row = history[-1] 

                    last_msg = last_msg_row[2] if len(last_msg_row) > 2 else "..."

                    real_chats.append({"id": char_name, "name": char_name, "msg": last_msg, "avatar": char_name[0].upper()})

            for chat in real_chats: self.add_chat_to_list(chat)

        except Exception as e: print(f"Error: {e}")



    def add_chat_to_list(self, chat_data):

        item = QListWidgetItem(self.chat_list_widget)

        item.setSizeHint(QSize(0, 80))

        item.setData(Qt.ItemDataRole.UserRole, chat_data["id"])

        row = ChatRowWidget(chat_data["name"], chat_data["msg"], chat_data["avatar"], lambda: self.pin_chat(chat_data["id"]), lambda: self.delete_chat(item, chat_data["name"]))

        self.chat_list_widget.setItemWidget(item, row)



    def on_chat_row_clicked(self, item): self.select_character(item.data(Qt.ItemDataRole.UserRole))

    def pin_chat(self, bot_id): print(f"Pin: {bot_id}")

    def delete_chat(self, item, bot_name):

        if QMessageBox.question(self, 'Delete', f"Delete {bot_name}?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:

            self.db.delete_character_history(bot_name); self.refresh_chats_list()



    def create_chat_page(self) -> QWidget:

        page = QWidget(); page.setStyleSheet("background-color: #18181b;")

        layout = QVBoxLayout(page); layout.setContentsMargins(0, 0, 0, 0); layout.setSpacing(0)

        self.chat_header = QFrame(); self.chat_header.setFixedHeight(70); self.chat_header.setStyleSheet("background-color: #18181b; border-bottom: 1px solid #27272a;")

        header_layout = QHBoxLayout(self.chat_header); header_layout.setContentsMargins(20, 0, 20, 0)

        btn_back = SidebarIconButton("back", "Back"); btn_back.setFixedSize(40, 40); btn_back.clicked.connect(lambda: self.switch_page("chats_list")); header_layout.addWidget(btn_back)

        self.chat_avatar = QLabel(); self.chat_avatar.setFixedSize(44, 44); self.chat_avatar.setAlignment(Qt.AlignmentFlag.AlignCenter); self.chat_avatar.setStyleSheet("background-color: #6366f1; border-radius: 22px; color: white; font-size: 18px; font-weight: bold;")

        header_layout.addWidget(self.chat_avatar); self.chat_title = QLabel("Character Name"); self.chat_title.setStyleSheet("color: #ffffff; font-size: 18px; font-weight: 600; margin-left: 12px;"); header_layout.addWidget(self.chat_title); header_layout.addStretch()

        self.btn_favorite = SidebarIconButton("heart", "Add to Favorites"); self.btn_favorite.setFixedSize(40, 40); self.btn_favorite.clicked.connect(self.toggle_favorite); header_layout.addWidget(self.btn_favorite)

        btn_export = SidebarIconButton("share", "Share Character"); btn_export.setFixedSize(40, 40); btn_export.clicked.connect(self.export_current_character); header_layout.addWidget(btn_export)

        btn_clear = SidebarIconButton("trash", "Delete Chat"); btn_clear.setFixedSize(40, 40); btn_clear.clicked.connect(self.clear_history); header_layout.addWidget(btn_clear); layout.addWidget(self.chat_header)

        self.msg_scroll = SmoothScrollArea(); self.msg_container = QWidget(); self.msg_container.setStyleSheet("background: transparent;"); self.msg_layout = QVBoxLayout(self.msg_container)

        self.msg_layout.setSpacing(16); self.msg_layout.setContentsMargins(60, 30, 60, 30); self.msg_layout.addStretch(); self.msg_scroll.setWidget(self.msg_container); layout.addWidget(self.msg_scroll)

        input_frame = QFrame(); input_frame.setFixedHeight(90); input_frame.setStyleSheet("background-color: #18181b;"); input_layout = QHBoxLayout(input_frame); input_layout.setContentsMargins(60, 15, 60, 25)

        text_container = QFrame(); text_container.setMaximumWidth(800); text_container.setFixedHeight(52); text_container.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed); text_container.setStyleSheet("QFrame { background-color: #27272a; border-radius: 26px; border: 1px solid #3f3f46; }")

        text_inner = QHBoxLayout(text_container); text_inner.setContentsMargins(24, 0, 12, 0); text_inner.setSpacing(12)

        self.input_field = QTextEdit(); self.input_field.setPlaceholderText("Type a message..."); self.input_field.setFixedHeight(36); self.input_field.setStyleSheet("background: transparent; border: none; color: #e4e4e7; font-size: 15px; padding-top: 8px;"); self.input_field.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff); self.input_field.installEventFilter(self)

        self.btn_send = SendButton(); self.btn_send.setFixedSize(40, 40); self.btn_send.clicked.connect(self.send_message); text_inner.addWidget(self.input_field, 1); text_inner.addWidget(self.btn_send, 0, Qt.AlignmentFlag.AlignVCenter); input_layout.addStretch(1); input_layout.addWidget(text_container, 10); input_layout.addStretch(1); layout.addWidget(input_frame)

        return page



    def select_character(self, name: str):

        self.current_char = name

        self.chat_title.setText(name)

        char_data = self.characters.get(name, {})

        custom_avatar = char_data.get("avatar")

        if custom_avatar and os.path.exists(custom_avatar):

            self.chat_avatar.setText(""); self.chat_avatar.setStyleSheet(f"background-image: url({custom_avatar.replace('\\', '/')}); background-position: center; border-radius: 22px; border: 1px solid #3f3f46;")

        else:

            self.chat_avatar.setText(name[0].upper()); self.chat_avatar.setStyleSheet("background-color: #6366f1; border-radius: 22px; color: white; font-size: 18px; font-weight: bold;")

        self.btn_favorite.icon_type = "heart_filled" if name in self.user_data.get("favorites", []) else "heart"; self.btn_favorite.update()

        self.load_chat_history(); self.switch_page("chat")



    def load_chat_history(self):

        while self.msg_layout.count() > 1:

            child = self.msg_layout.takeAt(0); 

            if child.widget(): child.widget().deleteLater()

        history = self.db.get_history(self.current_char); user_name = self.user_data["personas"][0]["name"]

        if not history and self.current_char:

            greeting = self.characters.get(self.current_char, {}).get("greeting", "")

            if greeting: self.add_bubble(greeting, "assistant", user_name=user_name)

        for row in history: self.add_bubble(row[2], row[1], row[0], user_name)

        QTimer.singleShot(100, self.msg_scroll.scroll_to_bottom)



    def add_bubble(self, text: str, role: str, msg_id: int = None, user_name: str = "You"):

        bubble = ChatBubble(text, role, user_name, self.current_char or "AI", msg_id); bubble.rewind_requested.connect(self.rewind_chat); self.msg_layout.insertWidget(self.msg_layout.count() - 1, bubble); return bubble



    def eventFilter(self, obj, event):

        if obj == self.input_field and event.type() == event.Type.KeyPress:

            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not event.modifiers(): self.send_message(); return True

        return super().eventFilter(obj, event)



    def send_message(self):

        text = self.input_field.toPlainText().strip()

        if not text or not self.current_char or self.is_generating: return

        self.input_field.clear(); self.is_generating = True; self.btn_send.setDisabled(True); self.input_field.setReadOnly(True); self.input_field.setPlaceholderText("AI is typing...")

        self.add_bubble(text, "user", user_name="You"); self.db.save_message(self.current_char, "user", text)

        self.current_ai_bubble = self.add_bubble("...", "assistant"); self.msg_scroll.scroll_to_bottom()

        full_history = self.db.get_history(self.current_char); recent_history = full_history[-20:] if len(full_history) > 20 else full_history

        history_payload = [(row[1], row[2]) for row in recent_history]; persona_txt = f"Name: {self.user_data['personas'][0]['name']}\nDetail: {self.user_data['personas'][0]['description']}"

        system_prompt = self.characters[self.current_char]["prompt"]

        self.worker = AIWorker(self.ai, system_prompt, persona_txt, history_payload, text); self.worker.token_received.connect(self.on_ai_token); self.worker.finished.connect(self.on_ai_finished); self.worker.error.connect(lambda e: QMessageBox.critical(self, "Error", e)); self.worker.start()



    def on_ai_token(self, token: str):

        if self.current_ai_bubble:

            if self.current_ai_bubble.text_content == "...": self.current_ai_bubble.update_text("")

            self.current_ai_bubble.append_text(token); scrollbar = self.msg_scroll.verticalScrollBar()

            if scrollbar.value() >= scrollbar.maximum() - 20: self.msg_scroll.scroll_to_bottom()



    def on_ai_finished(self):

        self.is_generating = False; self.btn_send.setDisabled(False); self.input_field.setReadOnly(False); self.input_field.setPlaceholderText("Type a message..."); self.input_field.setFocus()

        if self.current_ai_bubble: self.db.save_message(self.current_char, "assistant", self.current_ai_bubble.text_content); self.current_ai_bubble = None



    def stop_generation(self):

        if hasattr(self, 'worker') and self.worker.isRunning(): self.worker.stop_flag = True; self.worker.wait()

        self.is_generating = False; self.btn_send.setDisabled(False); self.input_field.setReadOnly(False)



    def rewind_chat(self, msg_id: int):

        if QMessageBox.question(self, "Rewind", "All messages after this will be deleted. Are you sure?") == QMessageBox.StandardButton.Yes: self.db.rewind_history(self.current_char, msg_id); self.load_chat_history()



    def clear_history(self):

        if not self.current_char: return

        if QMessageBox.question(self, "Confirm", "Delete all chat history?") == QMessageBox.StandardButton.Yes: self.stop_generation(); self.db.delete_character_history(self.current_char); self.load_chat_history()



    def open_character_popup(self):

        popup = CharacterPopup(self); popup.character_saved.connect(self.save_new_character); popup.exec()



    def save_new_character(self, char_data_package: dict):

        name, prompt, greeting, source_avatar_path = char_data_package["name"], char_data_package["prompt"], char_data_package["greeting"], char_data_package.get("avatar_source_path")

        new_char_data = {"prompt": prompt, "greeting": greeting, "avatar": None}

        if source_avatar_path and os.path.exists(source_avatar_path):

            try:

                avatar_dir = os.path.join("assets", "avatars"); os.makedirs(avatar_dir, exist_ok=True)

                _, ext = os.path.splitext(source_avatar_path); safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '_', '-')]).strip()

                target_path = os.path.join(avatar_dir, f"{safe_name}{ext}"); shutil.copy2(source_avatar_path, target_path); new_char_data["avatar"] = target_path.replace("\\", "/")

            except Exception as e: print(f"Could not save avatar: {e}")

        self.characters[name] = new_char_data; save_json(CHAR_FILE, self.characters)

        

        if self.content_stack.currentIndex() == 4:

            self.profile_page.refresh_content(self.user_data, self.characters)

            

        self.select_character(name); QMessageBox.information(self, "Success", f"'{name}' created successfully!")



    def open_persona_popup(self):

        current_personas = self.user_data.get("personas", [])

        popup = PersonaPopup(self, current_personas, self.save_persona); popup.exec()



    def save_persona(self, personas: list):

        self.user_data["personas"] = personas

        

        if self.current_user_id:

            try:

                self.db.update_user_personas(self.current_user_id, personas)

            except Exception as e:

                print(f"Could not write persona to database: {e}")



        save_json(USER_FILE, self.user_data)

        

        if self.content_stack.currentIndex() == 4:

            self.profile_page.refresh_content(self.user_data, self.characters)



    def export_current_character(self):

        if not self.current_char: return

        char_data = self.characters[self.current_char]

        img_b64 = image_to_base64(char_data.get("avatar")) if char_data.get("avatar") else None

        export_data = {"name": self.current_char, "prompt": char_data.get("prompt"), "greeting": char_data.get("greeting"), "avatar_image": img_b64}

        path, _ = QFileDialog.getSaveFileName(self, "Save", f"{self.current_char}.json", "JSON (*.json)")

        if path:

            with open(path, "w") as f: json.dump(export_data, f, indent=4)

            QMessageBox.information(self, "OK", "Saved")



    def toggle_favorite(self):

        if not self.current_char: return

        favs = self.user_data.get("favorites", [])

        if self.current_char in favs: favs.remove(self.current_char); self.btn_favorite.icon_type = "heart"

        else: favs.append(self.current_char); self.btn_favorite.icon_type = "heart_filled"

        self.user_data["favorites"] = favs; self.btn_favorite.update(); save_json(USER_FILE, self.user_data)



    def save_user_data(self):

        with open(USER_FILE, "w", encoding="utf-8") as f: json.dump(self.user_data, f, ensure_ascii=False, indent=2)



    def closeEvent(self, event): self.stop_generation(); event.accept()



if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = MainApp()

    window.show()

    sys.exit(app.exec())