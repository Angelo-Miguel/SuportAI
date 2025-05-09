# app/models/ticket.py
from app.database.db_connection import MySQLConnection

class Ticket:
    def __init__(self, id=None, title=None, category=None, description=None, user_id=None):
        self.id = id
        self.title = title
        self.category = category
        self.description = description
        self.user_id = user_id
        self.db = MySQLConnection()
    
    @classmethod
    def show_tickets(cls, user_id):
        conn = cls().db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                'SELECT * FROM tickets WHERE user_id = %s',
                (user_id,)
            )
            tickets = cursor.fetchall()
            return tickets
        except Exception as e:
            raise e
        finally:
            cursor.close()

    def new_ticket(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                'INSERT INTO tickets (title, category, description, user_id) VALUES (%s, %s, %s, %s)',
                (self.title, self.category, self.description, self.user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()