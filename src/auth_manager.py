import json
import os

SESSION_FILE = "session.json"

class AuthManager:
    @staticmethod
    def save_session(user_id, remember_me=False):
        """Kullanıcı giriş yaptığında çağırılır."""
        if remember_me:
            data = {
                "user_id": user_id,
                "is_remembered": True
            }
            try:
                with open(SESSION_FILE, "w", encoding="utf-8") as f:
                    json.dump(data, f)
            except Exception as e:
                print(f"Session save error: {e}")
        else:
            AuthManager.clear_session()

    @staticmethod
    def get_remembered_user():
        """Program açılırken kayıtlı kullanıcı var mı bakar."""
        if not os.path.exists(SESSION_FILE):
            return None
            
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data.get("is_remembered"):
                    return data.get("user_id")
        except:
            return None
        return None

    @staticmethod
    def clear_session():
        """Çıkış yapıldığında session dosyasını siler."""
        if os.path.exists(SESSION_FILE):
            try:
                os.remove(SESSION_FILE)
            except Exception as e:
                print(f"Session delete error: {e}")