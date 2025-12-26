import ollama
from src.config import MODEL_NAME

class AIEngine:
    def generate_response_stream(self, system_prompt, user_persona, chat_history, user_message, **kwargs):
        """
        Ollama'ya gönderilecek prompt'u hazırlar ve stream (akış) başlatır.
        Saf İngilizce Modu: Modelin en yüksek performansını vermesi için.
        """
        
        print(f"--- ACTIVE MODEL: {MODEL_NAME} (Native English Mode) ---")

        formatting_rules = """
FORMATTING RULES:
- Use *single asterisks* for physical actions and expressions. (e.g., *smiles softly*)
- Use **double asterisks** for internal thoughts that are NOT spoken aloud. (e.g., **I wonder if he knows the truth**)
- Use ***triple asterisks*** for setting the scene or describing the environment. (e.g., ***The wind howls outside the castle walls***)
"""
        final_prompt = (
            f"You are roleplaying as: {system_prompt}\n\n"
            f"--- INSTRUCTIONS ---\n"
            f"1. Stay in character at all times. Never break the fourth wall.\n"
            f"2. Write primarily in English. Use descriptive, literary language.\n"
            f"3. Only speak for your character. Do NOT describe the user's actions.\n"
            f"{formatting_rules}\n"
            f"--- USER INFO ---\n"
            f"Information about the user you are talking to:\n{user_persona}\n"
        )

        messages_payload = [{'role': 'system', 'content': final_prompt}]
        
        for role, content in chat_history:
            api_role = "assistant" if role == "assistant" else "user"
            messages_payload.append({'role': api_role, 'content': content})
        
        messages_payload.append({'role': 'user', 'content': user_message})

        try:
            return ollama.chat(
                model=MODEL_NAME, 
                messages=messages_payload, 
                stream=True, 
                options=kwargs
            )
        except Exception as e:
            if "10061" in str(e):
                raise ConnectionError("Could not connect to Ollama. Make sure the app is running.") from e
            raise e