from g4f.client import Client
from app.database.db_connection import MySQLConnection

class IaService():
    def __init__(self):
        self.db = MySQLConnection()
        self.client = Client()
        
    def chat_with_ai(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Você é um assistente de suporte para TI. Responda com soluções simples e diretas que um usuário final que não entenda do assunto possa seguir. Caso não consiga transfira a conversa para o agente humano."},
                {"role": "user", "content": prompt}
            ],
            web_search=False
        )
        return response.choices[0].message.content