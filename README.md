# Project Magnum (Alpha)

Project Magnum is a modern, offline-first AI Roleplay Client designed for privacy and aesthetics. It runs locally on your machine using **Ollama**, ensuring your chats remain private and uncensored.

![Screenshot](screenshot_placeholder.png) **

## 🚀 Features
- **100% Local & Private:** Data is stored in SQLite/JSON on your device.
- **Modern UI:** Built with PyQt6, featuring a clean dark mode inspired by Windows 11.
- **Character Cards:** Import/Create characters with avatars and custom personas.
- **Ollama Powered:** Default configured for **Magnum-v4** (or any LLM supported by Ollama).

## 🛠️ Installation

1. **Install Python 3.10+**
2. **Install Ollama:** [Download Ollama](https://ollama.com) and pull the model:
   ```bash
   ollama pull magnum-v4
   # Or any other model you prefer, just update src/config.py