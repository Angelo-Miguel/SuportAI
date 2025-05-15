# app/services/auth_service.py
from app.models.user import User
from app.database.db_connection import MySQLConnection
from flask import flash
import hashlib

# CLasse para autenticar o usuário
class AuthService:
    def __init__(self):
        self.db = MySQLConnection()
    
    # Criptografa a senha usando MD5 # FIXME: considerar usar bcrypt em produção
    def _hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()
    
    # Autentica o usuário
    def authenticate(self, email, raw_password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        password = self._hash_password(raw_password)
        
        try:
            cursor.execute(
                'SELECT * FROM users WHERE email = %s AND password = %s',
                (email, password)
            )
            user_data = cursor.fetchone()
            # TODO: colocar isso no controller
            if user_data:
                return User(user_data)
            else:
                flash('Usuário ou senha incorretos!', 'danger')
                return None
                
        except Exception as e:
            print(f'Erro ao autenticar: {str(e)}')
            flash('Erro durante o login', 'danger')
            return None
        finally:
            conn.close()
            cursor.close()