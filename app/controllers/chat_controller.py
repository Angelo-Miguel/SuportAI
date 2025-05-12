# app/controllers/user_controller.py
from flask import Blueprint, render_template, session, redirect, url_for
from app.services.ticket_service import TicketService
from app.services.message_service import MessageService

chat_bp = Blueprint('chat', __name__)
ticket_service = TicketService()
message_service = MessageService()

@chat_bp.route('/chat/<ticket_id>')
def chat(ticket_id):
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    ticket = ticket_service.get_ticket_by_id(ticket_id).__dict__
    messages = message_service.show_messages(ticket_id)
    
    return render_template('chat.html', user=session['user'], ticket=ticket, messages=messages)

#TODO: Terminar de fazer a rota e função send_message
@chat_bp.route('/send-msg', methods=['POST'])
def send_message():
    return chat(1)