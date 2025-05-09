# app/models/ticket.py
from app.database.db_connection import MySQLConnection

class Ticket:
    def __init__(self, id=None, title=None, category=None, description=None, user_id=None):
        self.id = id
        self.title = title
        self.category = category
        self.description = description
        self.user_id = user_id
