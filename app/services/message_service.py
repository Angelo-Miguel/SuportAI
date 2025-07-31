# app/services/message_service.py
from app.database.db_connection import MySQLConnection


# Classe para os servicos de messages
class MessageService:
    def __init__(self):
        self.db = MySQLConnection()

    def show_messages(self, ticket_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Seleciona as mensages dos usuarios referente ao ticket_id
            cursor.execute(
                "SELECT messages.message_id, messages.ticket_id, messages.user_id, users.name, users.role, messages.message, messages.sent_at FROM messages INNER JOIN users ON messages.user_id = users.user_id WHERE ticket_id = %s ORDER BY sent_at ASC;",
                (ticket_id,),
            )

            return cursor.fetchall()
        except Exception as e:
            raise e
        finally:
            conn.close()
            cursor.close()

    def send_message(self, message):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Executa o INSERT para adicionar o msg no banco
            cursor.execute(
                "INSERT INTO messages (message, user_id, ticket_id) VALUES (%s, %s, %s)",
                (message.message, message.user_id, message.ticket_id),
            )
            conn.commit()

            # TODO: Se necessario inserir um logica para retornar o id
            return None
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            cursor.close()
