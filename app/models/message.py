# app/models/message.py

class Message:
    def __init__(self, data):
        self.id = data.get('message_id')
        self.ticket_id = data.get('ticket_id')
        self.user_id = data.get('user_id')
        self.user_name = data.get('user_name')
        self.role = data.get('role')
        self.message = data.get('message')
        self.send_at = data.get('send_at')
