from g4f.client import Client
from app.database.db_connection import MySQLConnection

class IaService():
    def __init__(self):
        self.db = MySQLConnection()
        self.client = Client()
        
    def chat_with_ai(self, prompt, ticket_id):
        history = self.recovery_history(ticket_id)
        messages = [{"role": "system", "content": "Você é um assistente de suporte para TI. Responda com soluções simples e diretas que um usuário final que não entenda do assunto possa seguir. Caso não consiga, transfira a conversa para o agente humano."}]
        messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages = messages, # type: ignore
            web_search=False
        )
        return response.choices[0].message.content
    
    def recovery_history(self, ticket_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                'SELECT message, role FROM messages INNER JOIN users ON messages.user_id = users.user_id WHERE ticket_id = %s ORDER BY sent_at ASC',
                (ticket_id,)
            )
            results = cursor.fetchone()
            print("resultado historico ia: ",results)
            if results:
                return [{"role": results['role'], "content": results['message']}]
            return None
        except Exception as e:
            raise e
        finally:
            cursor.close()