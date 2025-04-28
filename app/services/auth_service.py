# app/services/auth_service.py
from app.models.user import Usuario
from app.database.db_connection import MySQLConnection
from flask import session, flash, redirect
import hashlib

class AuthService:
    def __init__(self):
        self.db = MySQLConnection()
    
    #Criptografa a senha usando MD5 # FIXME: considerar usar bcrypt em produção
    def _hash_password(self, password):
        return hashlib.md5(password.encode()).hexdigest()
    
    # Autentica o usuário
    def authenticate(self, email, raw_password):
        password = self._hash_password(raw_password)
        
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute(
                'SELECT * FROM users WHERE email = %s AND password = %s',
                (email, password)
            )
            
            user = cursor.fetchone()
            cursor.close()
            
            if user:
                session['user'] = user
                return user
            else:
                flash('Usuário ou senha incorretos!', 'danger')
                return None
                
        except Exception as e:
            print(f'Erro ao autenticar: {str(e)}')
            flash('Erro durante o login', 'danger')
            return None