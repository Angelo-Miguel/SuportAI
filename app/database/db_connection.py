# app/database/db_connection.py
import mysql.connector
from dotenv import load_dotenv
from app.config import Config

# FIXME: voltar a usar singleton, # HACK: conflito com threads da ia


# Classe que cria a conexao com o banco de dados
class MySQLConnection:
    @staticmethod
    def get_connection():
        return mysql.connector.connect(
            host=Config.DATABASE_HOST,
            port=int(Config.DATABASE_PORT or 3306),
            user=Config.DATABASE_USER,
            password=Config.DATABASE_PASSWORD,
            database=Config.DATABASE_NAME,
        )
