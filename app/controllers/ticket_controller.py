from flask import Blueprint, request, session, redirect, url_for
from app.models.ticket import Ticket
from app.services.ticket_service import TicketService

ticket_bp = Blueprint('ticket', __name__)
ticket_service = TicketService()

@ticket_bp.route('/new-ticket', methods=['POST'])
def new_ticket():
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))

    ticket = Ticket({
        'title': request.form.get('title'),
        'category': request.form.get('category'),
        'description': request.form.get('description'),
        'user_id': session['user']['id']
    })
    
    ticket_id = ticket_service.new_ticket(ticket)
    return redirect(url_for('chat.chat',ticket_id = ticket_id))

@ticket_bp.route('/open-ticket', methods=['POST'])
def open_ticket():
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))

    ticket_id = request.form.get('ticket_id')
    ticket = ticket_service.get_ticket_by_id(ticket_id)


    if ticket:
        return redirect(url_for('chat.chat', ticket_id=ticket_id))
    else:
        return "Ticket not found", 404
