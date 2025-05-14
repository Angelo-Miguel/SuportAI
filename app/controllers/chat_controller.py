# app/controllers/chat_controller.py
from flask import Blueprint, render_template, session, redirect, url_for, request
import threading
from app.services.ticket_service import TicketService
from app.services.message_service import MessageService
from app.services.ai_service import IaService
from app.models.message import Message


chat_bp = Blueprint('chat', __name__)

ticket_service = TicketService()
message_service = MessageService()
ia_service = IaService()

#TODO implementar socketio
@chat_bp.route('/chat/<ticket_id>')
def chat(ticket_id):
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    ticket = ticket_service.get_ticket_by_id(ticket_id).__dict__
    messages = message_service.show_messages(ticket_id)
    
    if ticket['status'] == 'ia' and len(messages) == 1:
        start_ai_thread(messages[0])
        
    return render_template('chat.html', user=session['user'], ticket=ticket, messages=messages)

@chat_bp.route('/send-msg', methods=['POST'])
def send_message():
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    
    user_message = Message({
        'message': request.form.get('message'),
        'user_id': session['user']['id'],
        'ticket_id':  request.form.get('ticket_id')
    })
    message_service.send_message(user_message)
    #TODO: terminar o loop da ia
    if request.form.get('status') == 'ia':
        print("message: ",user_message.__dict__)
        start_ai_thread(user_message.__dict__)
    return redirect(request.referrer)

@chat_bp.route('/exit', methods=['POST'])
def close_chat():
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))

    return redirect(url_for('user.dashboard'))

def ai(user_message):
    #resposta da IA
    ai_response = ia_service.chat_with_ai(user_message['message'], user_message['ticket_id'])
    print("msg: ",user_message['message'])

    ai_message = Message({
        'message': ai_response,
        'user_id': 0,  # ou "ia_bot", se seu sistema suporta string
        'ticket_id': user_message['ticket_id']
    })
    message_service.send_message(ai_message)
    
def start_ai_thread(user_message):
    threading.Thread(target=ai, args=(user_message,)).start()