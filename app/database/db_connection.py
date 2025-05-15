# app/database/db_connection.py
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(override=True)
# FIXME: voltar a usar singleton, # HACK: conflito com threads da ia

# Classe que cria a conexao com o banco de dados
class MySQLConnection:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=os.getenv("HOST_DB"),
            user=os.getenv("USER_DB"),
            password=os.getenv("PASSWORD_DB"),
            port=os.getenv("PORT_DB"),
            database=os.getenv("DATABASE_DB")
        )
