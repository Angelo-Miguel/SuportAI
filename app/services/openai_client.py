# app/services/openai_client.py
from app.config import Config
from openai import OpenAI


class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def chat(
        self, messages, model=Config.OPENAI_MODEL, temperature=Config.OPENAI_TEMPERATURE
    ):
        return self.client.chat.completions.create(
            model=model, messages=messages, temperature=temperature
        )
