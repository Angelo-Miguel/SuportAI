# app/services/openai_client.py
import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def chat(self, messages, model="gpt-4o-mini", temperature=0.7):
        return self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
