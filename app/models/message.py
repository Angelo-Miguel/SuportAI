# app/models/message.py

class Message:
    def __init__(self, data):
        self.ticket_id = data.get('ticket_id')
        self.user_id = data.get('user_id')
        self.message = data.get('message')