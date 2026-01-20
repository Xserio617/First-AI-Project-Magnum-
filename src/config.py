import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_NAME = "magnum-v4"

IMG_MODEL_ID = "cagliostrolab/animagine-xl-3.1"
IMG_OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "generated_images")

DEFAULT_NEGATIVE_PROMPT = (
    "nsfw, lowres, (bad), text, error, fewer, extra, missing, worst quality, "
    "jpeg artifacts, low quality, watermark, unfinished, displeasing, "
    "chromatic aberration, signature, extra digits, artistic error, "
    "username, scan, [abstract]"
)

DATA_DIR = os.path.join(BASE_DIR, "data")

CHAR_FILE = os.path.join(DATA_DIR, "characters.json")
USER_FILE = os.path.join(DATA_DIR, "user_persona.json")
DB_FILE = os.path.join(DATA_DIR, "chat_history.db")
SETTINGS_FILE = os.path.join(DATA_DIR, "settings.json")

DEFAULT_CHAR = {
    "Example Bot": {
        "prompt": "You are a helpful assistant..", 
        "greeting": "Hello! How can I help you?"
    }
}

DEFAULT_USER = {
  "current_persona": "Default",
  "personas": [
    {
      "name": "Default",
      "gender": "Not Specified",
      "description": "No specific information about the user."
    }
  ]
}

DEFAULT_SETTINGS = {"temperature": 0.7}