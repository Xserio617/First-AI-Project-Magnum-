import sys
from PyQt6.QtWidgets import QApplication
from src.ui.auth_window import AuthWindow
from src.ui.main_window import MainApp
from src.auth_manager import AuthManager


main_window_instance = None
login_window_instance = None

def start_app():
    global main_window_instance, login_window_instance
    
    app = QApplication(sys.argv)

    def show_login():
        """Function to open login screen"""
        global login_window_instance
        login_window_instance = AuthWindow()
        login_window_instance.login_successful.connect(on_login_success)
        login_window_instance.show()

    def on_logout():
        """Function to run on logout"""
        global main_window_instance
        print("Logged out. Returning to login screen...")

        show_login()

    def on_login_success(user_data):
        """Function to run on login success"""
        global main_window_instance, login_window_instance
        
        print(f"Login successful: {user_data['username']}")
        
    
        if login_window_instance:
            login_window_instance.close()


        main_window_instance = MainApp(
            user_id=user_data['id'], 
            username=user_data['username'] 
        )
        

        main_window_instance.logout_requested.connect(on_logout) 
        main_window_instance.show()

    saved_user_id = AuthManager.get_remembered_user()
    
    if saved_user_id:
        print(f"Welcome! ID: {saved_user_id}")
        main_window_instance = MainApp(user_id=saved_user_id, username="Registered Member") 
        main_window_instance.logout_requested.connect(on_logout)
        main_window_instance.show()
    else:
        show_login()

    sys.exit(app.exec())

if __name__ == "__main__":
    start_app()