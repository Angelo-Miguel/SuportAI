from flask import Blueprint, request, session, redirect, url_for
from app.models.ticket import Ticket
from app.services.ticket_service import TicketService

ticket_bp = Blueprint('ticket', __name__)
ticket_service = TicketService()

@ticket_bp.route('/new-ticket', methods=['POST'])
def new_ticket():
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))

    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')
    user_id = session['user']['user_id']

    ticket = Ticket(title=title, category=category, description=description, user_id=user_id)
    ticket_service.new_ticket(ticket)
    
    session['ticket'] = ticket.__dict__
    return redirect(url_for('chat.chat'))
