# app/models/ticket.py
class Ticket:
    def __init__(self, data):
        self.id = data.get('ticket_id')
        self.title = data.get('title')
        self.category = data.get('category')
        self.description = data.get('description')
        self.status = data.get('status')
        self.created_at = data.get('created_at')
        self.user_id = data.get('user_id')