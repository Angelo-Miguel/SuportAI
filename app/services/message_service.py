# app/services/message_service.py
from app.database.db_connection import MySQLConnection
from app.models.message import Message

class MessageService:
    def __init__(self):
        self.db = MySQLConnection()
    
    def show_messages(self, ticket_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                'SELECT messages.message_id, messages.ticket_id, messages.user_id, users.name, users.role, messages.message, messages.sent_at FROM messages INNER JOIN users ON messages.user_id = users.user_id WHERE ticket_id = %s ORDER BY sent_at ASC;',
                (ticket_id,)
            )
            messages = cursor.fetchall()
               
            return messages
        except Exception as e:
            raise e
        finally:
            cursor.close()
            
    #TODO: Terminar de fazer a rota e função send_message
    def send_message(self, message: Message):
        conn = MySQLConnection().get_connection()