
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Mevcut motorlarını içe aktar
from src.ai_engine import AIEngine
from src.image_gen import ImageGenerator
from src.config import CHAR_FILE, DEFAULT_CHAR, USER_FILE, DEFAULT_USER
from src.database import load_json

app = FastAPI(title="Magnum AI Server")

# CORS (Telefondan erişim izni)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- GLOBAL NESNELER ---
ai_engine = AIEngine()
# Image Generator'ı RAM'de tutmak için başta yüklüyoruz
print("Sunucu başlatılıyor... Görsel motoru hazırlanıyor...")
img_gen = ImageGenerator() 

# Statik dosyalar (Resimler ve Arayüz için)
os.makedirs("assets/generated_images", exist_ok=True)
os.makedirs("web_ui", exist_ok=True) # Web arayüzü buraya gelecek
app.mount("/images", StaticFiles(directory="assets/generated_images"), name="images")
app.mount("/static", StaticFiles(directory="web_ui"), name="static")

# --- MODELLER ---
class ChatRequest(BaseModel):
    prompt: str
    character_name: str
    history: List[List[str]] # [['user', 'msg'], ['assistant', 'msg']]

class ImageRequest(BaseModel):
    prompt: str

# --- ENDPOINTLER ---

@app.get("/")
def read_root():
    return {"status": "Online", "gpu": img_gen.device}

@app.post("/api/chat")
def chat_endpoint(request: ChatRequest):
    """Magnum AI ile konuşma endpoint'i"""
    try:
        # Karakter verisini yükle
        chars = load_json(CHAR_FILE, DEFAULT_CHAR)
        char_data = chars.get(request.character_name, chars.get("Example Bot"))
        system_prompt = char_data.get("prompt", "You are a helpful assistant.")
        
        # Basit bir kullanıcı personası
        user_persona = "User: Admin" 
        
        # Geçmiş formatını ayarla
        formatted_history = []
        for msg in request.history:
            role = msg[0] # 'user' veya 'assistant'
            content = msg[1]
            formatted_history.append((role, content))

        # Stream yerine tek seferde yanıt alalım (Mobil için daha basit)
        # Not: AIEngine'de stream=False seçeneği yoksa stream'i birleştiririz.
        full_response = ""
        stream = ai_engine.generate_response_stream(
            system_prompt, user_persona, formatted_history, request.prompt
        )
        
        for chunk in stream:
            if 'message' in chunk and 'content' in chunk['message']:
                full_response += chunk['message']['content']
                
        return {"response": full_response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate_image")
def image_endpoint(request: ImageRequest):
    """Resim oluşturma endpoint'i"""
    try:
        print(f"Telefondan resim isteği geldi: {request.prompt}")
        path = img_gen.generate(request.prompt)
        
        if path:
            filename = os.path.basename(path)
            # Mobilin erişebileceği URL'yi döndür
            return {"image_url": f"/images/{filename}"}
        else:
            raise HTTPException(status_code=500, detail="Görsel oluşturulamadı.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # 0.0.0.0 yerel ağdaki tüm cihazlara açar
    uvicorn.run(app, host="0.0.0.0", port=8000)