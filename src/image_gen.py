import os
from src.config import IMG_MODEL_ID, IMG_OUTPUT_DIR, DEFAULT_NEGATIVE_PROMPT

class ImageGenerator:
    def __init__(self):
        self.pipe = None
        self.device = "cpu"
        self.torch = None
        self.pipeline_cls = None
        self.available = False
        self.init_error = None

        self._load_runtime_dependencies()
        if self.available and self.torch.cuda.is_available():
            try:
                cap = self.torch.cuda.get_device_capability()
                if cap[0] >= 10:
                    print(f"UYARI: GPU Mimarisi çok yeni ({cap}). PyTorch desteği bekleniyor. CPU kullanılacak.")
                    self.device = "cpu"
                else:
                    self.device = "cuda"
            except Exception:
                self.device = "cuda"
        else:
            self.device = "cpu"
            
        self._ensure_output_dir()

    def _load_runtime_dependencies(self):
        """Import heavy/fragile deps lazily so UI can start even when Torch DLL fails."""
        try:
            import torch
            from diffusers import StableDiffusionXLPipeline

            self.torch = torch
            self.pipeline_cls = StableDiffusionXLPipeline
            self.available = True
            self.init_error = None
        except Exception as e:
            self.available = False
            self.init_error = str(e)
            print(f"Image generation unavailable: {self.init_error}")

    def _ensure_output_dir(self):
        """Çıktı klasörünü oluşturur"""
        if not os.path.exists(IMG_OUTPUT_DIR):
            os.makedirs(IMG_OUTPUT_DIR)

    def load_model(self):
        """Modeli hafızaya yükler"""
        if self.pipe is not None:
            return

        if not self.available:
            raise RuntimeError(f"Image generation is unavailable: {self.init_error}")

        print(f"--- LOADING IMAGE MODEL: {IMG_MODEL_ID} ---")
        try:
            dtype = self.torch.float16 if self.device == "cuda" else self.torch.float32
            self.pipe = self.pipeline_cls.from_pretrained(
                IMG_MODEL_ID,
                torch_dtype=dtype,
                use_safetensors=True,
            )
            
            self.pipe.to(self.device)
            print(f"--- IMAGE MODEL LOADED SUCCESSFULLY ({self.device.upper()} MODE) ---")
        except Exception as e:
            print(f"FATAL ERROR loading image model: {e}")
            self.pipe = None
            raise e

    def generate(self, prompt, negative_prompt=None, steps=28):
        """Görsel oluşturur ve dosya yolunu döner"""
        if not self.available:
            raise RuntimeError(f"Image generation is unavailable: {self.init_error}")

        if not self.pipe:
            self.load_model()

        enhanced_prompt = f"masterpiece, best quality, {prompt}"
        
        final_neg = negative_prompt if negative_prompt else DEFAULT_NEGATIVE_PROMPT

        print(f"Generating Image: {enhanced_prompt}...")
        
        try:
            image = self.pipe(
                prompt=enhanced_prompt,
                negative_prompt=final_neg,
                num_inference_steps=steps,
                guidance_scale=7.0,
                width=1024, # SDXL standart çözünürlük
                height=1024
            ).images[0]

            from datetime import datetime
            filename = f"img_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            save_path = os.path.join(IMG_OUTPUT_DIR, filename)
            
            image.save(save_path)
            print(f"Image saved to: {save_path}")
            return save_path
            
        except Exception as e:
            print(f"Generation Error: {e}")
            return None