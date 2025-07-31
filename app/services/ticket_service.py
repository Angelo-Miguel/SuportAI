# app/services/ticket_service.py
from app.database.db_connection import MySQLConnection
from app.models.ticket import Ticket


class TicketService:
    def __init__(self):
        self.db = MySQLConnection()

    def show_tickets(self, user_id):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Mostra dos os tickets do usuário
            cursor.execute("SELECT * FROM tickets WHERE user_id = %s", (user_id,))
            return cursor.fetchall()

        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def new_ticket(self, ticket):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Executa o INSERT para adicionar o novo ticket no banco
            cursor.execute(
                "INSERT INTO tickets (title, category, description, user_id) VALUES (%s, %s, %s, %s)",
                (ticket.title, ticket.category, ticket.description, ticket.user_id),
            )
            conn.commit()

            # Recupera o ID do último ticket inserido
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            if result:
                ticket_id = result["LAST_INSERT_ID()"]  # type: ignore  #HACK: ERROR: No overloads for "__getitem__" match the provided arguments
            else:
                ticket_id = None

            # Retorna o ID gerado pelo banco
            return ticket_id
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

    def get_ticket_by_id(self, ticket_id):
        # Mostra o ticket da id selecionado
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute("SELECT * FROM tickets WHERE ticket_id = %s", (ticket_id,))

            return Ticket(cursor.fetchone())
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def change_ticket_status(self, status, ticket_id):
        # Troca o status do tikcets
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            cursor.execute(
                "UPDATE tickets SET `status` = %s WHERE ticket_id = %s;",
                (
                    status,
                    ticket_id,
                ),
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
