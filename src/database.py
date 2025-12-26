import json

import os

import sqlite3

import bcrypt

from src.config import DATA_DIR, DB_FILE



class DatabaseManager:



    def get_recent_chats(self, user_id):

        """Kullanıcının mesajlaştığı karakterleri, son mesaj tarihine göre getirir."""

        query = """

            SELECT DISTINCT c.id, c.name, c.avatar_path, c.description, MAX(m.timestamp) as last_msg_time

            FROM characters c

            JOIN messages m ON c.id = m.character_id

            WHERE m.user_id = ?

            GROUP BY c.id

            ORDER BY last_msg_time DESC

        """

        try:

            cursor = self.conn.cursor()

            cursor.execute(query, (user_id,))

            columns = [col[0] for col in cursor.description]

            results = []

            for row in cursor.fetchall():

                results.append(dict(zip(columns, row)))

            return results

        except Exception as e:

            print(f"Chat history error: {e}")

            return []

        

    def __init__(self):

        self.ensure_setup()



    def ensure_setup(self):

        if not os.path.exists(DATA_DIR):

            os.makedirs(DATA_DIR)

        

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        



        cursor.execute('''

            CREATE TABLE IF NOT EXISTS messages (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                character_name TEXT,

                role TEXT,

                content TEXT,

                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

                user_id INTEGER

            )

        ''')

        





        cursor.execute('''

            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                username TEXT UNIQUE NOT NULL,

                password_hash BLOB NOT NULL,

                personas TEXT, 

                created_at DATETIME DEFAULT CURRENT_TIMESTAMP

            )

        ''')



        try:

            cursor.execute("ALTER TABLE users ADD COLUMN personas TEXT")

        except sqlite3.OperationalError:

            pass

        

        conn.commit()

        conn.close()





    def register_user(self, username, password):

        """Yeni kullanıcı kaydeder"""

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        



        password_bytes = password.encode('utf-8')

        salt = bcrypt.gensalt()

        hashed = bcrypt.hashpw(password_bytes, salt)



        default_personas = [

            {

                "name": username, 

                "gender": "", 

                "description": "A new user.",

                "avatar": None

            }

        ]

        personas_json = json.dumps(default_personas, ensure_ascii=False)

        

        try:

            cursor.execute("INSERT INTO users (username, password_hash, personas) VALUES (?, ?, ?)", 

                         (username, hashed, personas_json))

            conn.commit()

            conn.close()

            return True, "Registration successful! You can login."

        except sqlite3.IntegrityError:

            conn.close()

            return False, "This username is already taken."

        except Exception as e:

            conn.close()

            return False, f"Error: {str(e)}"



    def login_user(self, username, password):

        """Kullanıcı girişi yapar"""

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        

        cursor.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))

        user = cursor.fetchone()

        conn.close()

        

        if user:

            user_id, stored_hash = user

            password_bytes = password.encode('utf-8')

            

            if bcrypt.checkpw(password_bytes, stored_hash):

                return True, user_id

            else:

                return False, "Incorrect Password."

        else:

            return False, "User not found."

        

    def get_user_personas(self, user_id):

        """Kullanıcının profillerini çeker"""

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        cursor.execute("SELECT personas FROM users WHERE id = ?", (user_id,))

        row = cursor.fetchone()

        conn.close()

        

        if row and row[0]:

            return json.loads(row[0])

        return []



    def update_user_personas(self, user_id, personas_list):

        """Kullanıcının profillerini günceller"""

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        personas_json = json.dumps(personas_list, ensure_ascii=False)

        cursor.execute("UPDATE users SET personas = ? WHERE id = ?", (personas_json, user_id))

        conn.commit()

        conn.close()



    def get_recent_chats(self, user_id):

        return []

        

    def save_message(self, char_name, role, content):

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        cursor.execute("INSERT INTO messages (character_name, role, content) VALUES (?, ?, ?)", (char_name, role, content))

        new_id = cursor.lastrowid

        conn.commit()

        conn.close()

        return new_id



    def get_history(self, char_name, limit=None):

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        cursor.execute("SELECT id, role, content FROM messages WHERE character_name = ? ORDER BY id ASC", (char_name,))

        rows = cursor.fetchall()

        conn.close()

        if limit and len(rows) > limit: return rows[-limit:]

        return rows



    def rewind_history(self, char_name, last_msg_id):

        """

        Belirtilen mesajdan SONRAKİ tüm mesajları siler.

        """

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        cursor.execute("DELETE FROM messages WHERE character_name = ? AND id > ?", (char_name, last_msg_id))

        conn.commit()

        conn.close()



    def delete_character_history(self, char_name):

        conn = sqlite3.connect(DB_FILE)

        cursor = conn.cursor()

        cursor.execute("DELETE FROM messages WHERE character_name = ?", (char_name,))

        conn.commit(); conn.close()



def load_json(filepath, default_content):

    if not os.path.exists(filepath):

        save_json(filepath, default_content)

        return default_content

    try:

        with open(filepath, "r", encoding="utf-8") as f:

            return json.load(f)

    except Exception as e:

        print(f"JSON Yükleme Hatası ({filepath}): {e}")

        return default_content



def save_json(filepath, data):

    with open(filepath, "w", encoding="utf-8") as f:

        json.dump(data, f, ensure_ascii=False, indent=4)