import ollama
try:
    ollama.list()
    print("Ollama connection successful")
except Exception as e:
    print(f"Ollama connection failed: {e}")
