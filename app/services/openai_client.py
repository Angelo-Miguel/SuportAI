# app/services/openai_client.py
from app.config import Config
from openai import OpenAI
import logging

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def chat(self, messages, model=None, temperature=None):
        model = model or Config.OPENAI_MODEL
        temperature = temperature if temperature is not None else Config.OPENAI_TEMPERATURE
        try:
            return self.client.chat.completions.create(
                model=model, messages=messages, temperature=temperature
            )
        except Exception as e:
            logging.error(f"Erro na chamada OpenAI: {e}")
            raise