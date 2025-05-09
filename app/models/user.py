# app/models/user.py
from app.database.db_connection import MySQLConnection

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha