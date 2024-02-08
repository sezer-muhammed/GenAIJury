from pathlib import Path
import google.generativeai as genai
from genaijury.api_models.base import APIModel
import mimetypes

class GeminiAPIModel(APIModel):
    def __init__(self):
        self.api_key = None
        self.model = None
        self.generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 16000,
        }


    def configure(self, api_key: str, **config):
        self.api_key = api_key
        genai.configure(api_key=self.api_key)  # Initialize the library

        # Update configuration if provided
        if config:
            if 'generation_config' in config:
                self.generation_config = config['generation_config']
            if 'safety_settings' in config:
                self.safety_settings = config['safety_settings']

        # Create the Gemini model instance
        self.model = genai.GenerativeModel(
            model_name="gemini-pro-vision",  # Adapt if using a different model
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )

    def call(self, image_paths: list[str], text_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("API key not configured. Call the 'configure' method first.")
        if not self.model:
            raise RuntimeError("Gemini model not initialized. Call the 'configure' method first.")

        image_parts = []
        for image_path in image_paths:
            mime_type = mimetypes.guess_type(image_path)[0] or 'application/octet-stream'
            image_parts.append(
                {
                    "mime_type": mime_type,
                    "data": Path(image_path).read_bytes()
                }
            )

        prompt_parts = [
            *image_parts,  # Unpack image_parts in the prompt
            text_prompt,
        ]

        try:
            response = self.model.generate_content(prompt_parts)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}")