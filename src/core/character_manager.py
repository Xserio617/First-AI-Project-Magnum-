import json

import os

from src.config import CHAR_FILE, DEFAULT_CHAR



class CharacterManager:

    def __init__(self):

        self.characters = []

        self.load_characters()



    def load_characters(self):

        """Karakterleri JSON dosyasından yükler"""

        if not os.path.exists(CHAR_FILE):

            self.save_characters(DEFAULT_CHAR)

            data = DEFAULT_CHAR

        else:

            try:

                with open(CHAR_FILE, "r", encoding="utf-8") as f:

                    data = json.load(f)

            except (json.JSONDecodeError, FileNotFoundError):

                data = DEFAULT_CHAR

                self.save_characters(data)



        self.characters = []

        for name, details in data.items():

            char_info = {"name": name}

            char_info.update(details)

            self.characters.append(char_info)



    def save_characters(self, data):

        """Karakterleri dosyaya kaydeder"""

        os.makedirs(os.path.dirname(CHAR_FILE), exist_ok=True)

        

        with open(CHAR_FILE, "w", encoding="utf-8") as f:

            json.dump(data, f, ensure_ascii=False, indent=4)



    def get_all_characters(self):

        """Tüm karakter listesini döndürür"""

        return self.characters



    def get_character(self, name):

        """İsme göre tek bir karakter verisi döndürür"""

        for char in self.characters:

            if char['name'] == name:

                return char

        return None