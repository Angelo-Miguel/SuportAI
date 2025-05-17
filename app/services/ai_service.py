# app/service/ai_service.py
# TODO: trocar para OpenAI
from g4f.client import Client
from app.database.db_connection import MySQLConnection
from app.services.prompt_service import PromptBuilder

# Classe dos serviços da IA
class IaService:
    def __init__(self):
        self.client = Client()
        self.prompt_builder = PromptBuilder()

    def chat_with_ai(self, prompt, ticket_id):
        history, attempt_count = self.recovery_history(ticket_id)
        system_prompt = self.prompt_builder.build(attempt_count)

        messages = [{"role": "system", "content": system_prompt}]

        if history:
            history.pop()  # Remove a última mensagem (geralmente a IA anterior)
            corrected_history = []
            for msg in history:
                role = "assistant" if msg["role"] == "ai" else msg["role"]
                corrected_history.append({"role": role, "content": msg["content"]})
            messages.extend(corrected_history)

        messages.append({"role": "user", "content": prompt})

        print("IA message:", messages)  # DEBUG

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages, # type: ignore #HACK
            web_search=False
        )
        response_text = response.choices[0].message.content

        print("Resposta IA:", response_text)  # DEBUG

        should_transfer = (
            PromptBuilder.TRANSFER_TRIGGER_PHRASE in response_text.lower()
        )

        print("Tentativas:", attempt_count)
        print("Transferir para humano?", should_transfer)

        return response_text, should_transfer

    @staticmethod
    def recovery_history(ticket_id):
        conn = MySQLConnection().get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(
                'SELECT message, role FROM messages INNER JOIN users ON messages.user_id = users.user_id WHERE ticket_id = %s ORDER BY sent_at ASC',
                (ticket_id,)
            )
            results = cursor.fetchall()
            if results:
                attempt_count = sum(1 for row in results if row["role"] == "ai") # type: ignore #HACK
                formatted_results = [
                    {
                        "role": "assistant" if row["role"] == "ai" else row["role"], # type: ignore #HACK
                        "content": row["message"] # type: ignore #HACK
                    }
                    for row in results
                ]
                return formatted_results, attempt_count
            return None, 0
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()
