# app/services/ticket_service.py
from app.database.db_connection import MySQLConnection
from app.models.ticket import Ticket

class TicketService():
    def __init__(self):
        self.db = MySQLConnection()
        
    def show_tickets(self, user_id):
        conn = self.db.get_connection()
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
    
    def new_ticket(self, ticket: Ticket):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                'INSERT INTO tickets (title , category, description, user_id) VALUES (%s, %s, %s, %s)',
                (ticket.title, ticket.category, ticket.description, ticket.user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()

    def get_ticket_by_id(self, ticket_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(
                'SELECT * FROM tickets WHERE ticket_id = %s',
                (ticket_id,)
            )
            ticket = cursor.fetchone()
            return ticket
        except Exception as e:
            raise e
        finally:
            cursor.close()