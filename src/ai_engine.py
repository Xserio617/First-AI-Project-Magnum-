import ollama

from src.config import MODEL_NAME



class AIEngine:
    def __init__(self):
        self.force_cpu = False

    def _is_cuda_runner_error(self, err: Exception) -> bool:
        msg = str(err).lower()
        return (
            "cuda error" in msg
            or "status code: 500" in msg
            or "llama runner process has terminated" in msg
        )

    def _build_options(self, kwargs):
        options = dict(kwargs) if kwargs else {}
        if self.force_cpu:
            options["num_gpu"] = 0
        return options

    def check_connection(self):
        try:
            ollama.list()
            return True
        except:
            return False

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



        def stream_with_fallback():
            options = self._build_options(kwargs)

            try:
                stream = ollama.chat(
                    model=MODEL_NAME,
                    messages=messages_payload,
                    stream=True,
                    options=options,
                )
                for chunk in stream:
                    yield chunk
                return
            except Exception as e:
                if "10061" in str(e):
                    raise ConnectionError("Could not connect to Ollama. Make sure the app is running.") from e
                if self._is_cuda_runner_error(e) and not self.force_cpu:
                    print("CUDA runner failed. Retrying with CPU mode (num_gpu=0)...")
                    self.force_cpu = True
                else:
                    raise e

            stream = ollama.chat(
                model=MODEL_NAME,
                messages=messages_payload,
                stream=True,
                options=self._build_options(kwargs),
            )
            for chunk in stream:
                yield chunk

        return stream_with_fallback()

    def generate_simple_response(self, messages, **kwargs):
        """
        Stream olmayan tek seferlik yanıt döndürür.
        """
        try:
            response = ollama.chat(
                model=MODEL_NAME, 
                messages=messages, 
                stream=False, 
                options=self._build_options(kwargs)
            )
            if 'message' in response and 'content' in response['message']:
                return response['message']['content']
            return None
        except Exception as e:
            if self._is_cuda_runner_error(e) and not self.force_cpu:
                print("CUDA runner failed. Retrying with CPU mode (num_gpu=0)...")
                self.force_cpu = True
                try:
                    response = ollama.chat(
                        model=MODEL_NAME,
                        messages=messages,
                        stream=False,
                        options=self._build_options(kwargs),
                    )
                    if 'message' in response and 'content' in response['message']:
                        return response['message']['content']
                except Exception as retry_err:
                    print(f"Simple generation retry error: {retry_err}")
            print(f"Simple generation error: {e}")
            return None
