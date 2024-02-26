from pathlib import Path
import google.generativeai as genai
from genaijury.api_models.base import APIModel
import mimetypes

class GeminiAPIModel(APIModel):
    def __init__(self):
        self.api_key = None
        self.model = None
        self.generation_config = {
            "temperature": 0.35,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 20000,
        }
        self.safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]


    def configure(self, api_key: str, **config):
            """
            Configures the Gemini API client with the provided API key and optional additional configuration.

            Args:
                api_key (str): The API key to authenticate the client.
                **config: Additional configuration options. Can include 'generation_config' and 'safety_settings'.

            Returns:
                self: The configured Gemini API client instance.
            """
            self.api_key = api_key
            genai.configure(api_key=self.api_key)  # Initialize the library

            # Update configuration if provided
            if config:
                if 'generation_config' in config:
                    self.generation_config = config['generation_config']
                if 'safety_settings' in config:
                    self.safety_settings = config['safety_settings']

            return self

    def call(self, text_prompt: str, image_paths: list[str] = []) -> str:
        if not self.api_key:
            raise ValueError("API key not configured. Call the 'configure' method first.")
        # Create the Gemini model instance


        if image_paths:
            model_type = "gemini-1.0-pro-vision-latest"
        else:
            model_type = "gemini-1.0-pro"

        model = genai.GenerativeModel(
            model_name=model_type,  # Adapt if using a different model
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )

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
            response = model.generate_content(prompt_parts)
            return response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API call failed: {e}")