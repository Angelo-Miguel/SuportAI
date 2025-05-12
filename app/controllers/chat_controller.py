# app/controllers/user_controller.py
from flask import Blueprint, render_template, session, redirect, url_for, request
from app.services.ticket_service import TicketService
from app.services.message_service import MessageService
from app.models.message import Message

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

@chat_bp.route('/send-msg', methods=['POST'])
def send_message():
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    
    message = Message({
        'message': request.form.get('message'),
        'user_id': session['user']['id'],
        'ticket_id':  request.form.get('ticket_id')
    })
    
    print("MSG:", message.__dict__)
    
    message_service.send_message(message)
    
    
    return redirect(request.referrer)