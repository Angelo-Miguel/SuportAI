# app/services/ticket_service.py
from app.database.db_connection import MySQLConnection

class TicketService:
    def __init__(self):
        self.db = MySQLConnection()

    def show_tickets(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                'SELECT * FROM tickets WHERE fk_users_id_user = %s',
                (user_id,)
            )
            tickets = cursor.fetchall()
            return tickets
        except Exception as e:
            raise e
        finally:
            cursor.close()