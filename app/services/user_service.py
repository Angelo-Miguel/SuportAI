# app/services/user_service.py
from app.database.db_connection import MySQLConnection
import hashlib


class UserService:
    def __init__(self):
        self.db = MySQLConnection()

    # Criptografa a senha usando MD5 # FIXME: considerar usar bcrypt em produção
    def _hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    # Cria um novo usuário no banco de dados
    def create_user(self, name, email, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        hashed_password = self._hash_password(password)

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password),
            )
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            cursor.close()
