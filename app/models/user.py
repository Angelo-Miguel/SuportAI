# app/models/usuario.py
from app.database.db_connection import MySQLConnection

class Usuario:
    def __init__(self, id=None, nome=None, email=None, senha=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.db = MySQLConnection()
    
    @classmethod
    def buscar_por_email(cls, email):
        # Busca usuário por email
        try:
            conn = cls().db.get_connection()
            cursor = conn.cursor(dictionary=True)
            
            cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
            user_data = cursor.fetchone()
            cursor.close()
            
            if user_data:
                return cls(user_data)
            return None
                
        except Exception as e:
            print(f'Erro ao buscar usuário: {str(e)}')
            return None