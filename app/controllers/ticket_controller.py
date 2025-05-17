# app/controllers/ticket_controller.py
from flask import Blueprint, request, session, redirect, url_for
from app.models.ticket import Ticket
from app.models.message import Message
from app.services.ticket_service import TicketService
from app.services.message_service import MessageService

ticket_bp = Blueprint('ticket', __name__)

ticket_service = TicketService()
message_service = MessageService()

@ticket_bp.route('/new-ticket', methods=['POST'])
def new_ticket():
    # Cria um novo Ticket
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))

    ticket = Ticket({
        'title': request.form.get('title'),
        'category': request.form.get('category'),
        'description': request.form.get('description'),
        'user_id': session['user']['id']
    })
    ticket_id = ticket_service.new_ticket(ticket)
    
    # FIXME: # HACK dar um jeito de colocar isso no chat controller
    # Primeira msg do usuario
    session['first_user_message'] ={
        'message': request.form.get('description'),
        'user_id': session['user']['id'],
        'ticket_id': ticket_id
    }
      
    return redirect(url_for('chat.chat',ticket_id = ticket_id))

@ticket_bp.route('/open-ticket', methods=['POST'])
def open_ticket():
    # Abre um tikcet que já foi criado
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))

    ticket_id = request.form.get('ticket_id')
    ticket = ticket_service.get_ticket_by_id(ticket_id)

    if ticket:
        return redirect(url_for('chat.chat', ticket_id=ticket_id))
    else:
        return "Ticket not found", 404