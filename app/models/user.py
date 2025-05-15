# app/models/user.py
# Classe das usuários
class User:
    def __init__(self, data):
        self.id = data.get('user_id')
        self.name = data.get('name')
        self.email = data.get('email')
        self.role = data.get('role')