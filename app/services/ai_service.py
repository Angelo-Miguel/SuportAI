# app/services/ai_service.py

from app.services.openai_client import OpenAIClient
from app.services.embedding_service import EmbeddingService
from app.database.db_connection import MySQLConnection
from app.services.prompt_service import PromptBuilder


class IaService:
    def __init__(self):
        self.ai_client = OpenAIClient()
        self.prompt_builder = PromptBuilder()
        self.embedding_service = EmbeddingService()

    def chat_with_ai(self, prompt, ticket_id):
        history, attempt_count = self.recovery_history(ticket_id)
        system_prompt = self.prompt_builder.build(attempt_count)

        messages = [{"role": "system", "content": system_prompt}]

        if history:
            history.pop()
            for msg in history:
                role = "assistant" if msg["role"] == "ai" else msg["role"]
                messages.append({"role": role, "content": msg["content"]}) #type: ignore #HACK

        relevant_docs = self.embedding_service.get_relevant_chunks(prompt)
        if relevant_docs:
            context_text = "\n".join(relevant_docs)
            messages.append({
                "role": "system",
                "content": f"Contexto adicional baseado em documentos anteriores:\n{context_text}"
            })

        messages.append({"role": "user", "content": prompt})

        print("Mensagens para IA:", messages)  # DEBUG

        response = self.ai_client.chat(messages)
        response_text = response.choices[0].message.content

        print("Resposta da IA:", response_text)  # DEBUG

        should_transfer = (
            PromptBuilder.TRANSFER_TRIGGER_PHRASE in response_text.lower() #type: ignore #HACK
        )

        print("Tentativas:", attempt_count)
        print("Transferir para humano?", should_transfer)

        return response_text, should_transfer

    @staticmethod
    def recovery_history(ticket_id):
        conn = MySQLConnection().get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            query = "SELECT message, role FROM messages INNER JOIN users ON messages.user_id = users.user_id WHERE ticket_id = %s ORDER BY sent_at ASC"
            cursor.execute(query, (ticket_id,))
            results = cursor.fetchall()

            if not results:
                return None, 0

            attempt_count = sum(1 for row in results if row["role"] == "ai") #type: ignore #HACK
            formatted_results = [
                {
                    "role": "assistant" if row["role"] == "ai" else row["role"], #type: ignore #HACK
                    "content": row["message"] #type: ignore #HACK
                }
                for row in results
            ]

            return formatted_results, attempt_count

        except Exception as e:
            print("Erro ao recuperar histórico:", e)
            raise

        finally:
            cursor.close()
            conn.close()
