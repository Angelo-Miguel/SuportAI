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
    # Pagina do chat usuário
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    
    ticket = ticket_service.get_ticket_by_id(ticket_id).__dict__
    messages = message_service.show_messages(ticket_id)
    
     # Controla se ia vai responder ou não
    if ticket['status'] == 'ia':
        start_ai_thread(messages[0])
        
    return render_template('chat.html', user=session['user'], ticket=ticket, messages=messages)

@chat_bp.route('/send-msg', methods=['POST'])
def send_message():
    # Processo para mandar uma msg
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    
    user_message = Message({
        'message': request.form.get('message'),
        'user_id': session['user']['id'],
        'ticket_id':  request.form.get('ticket_id')
    })
    message_service.send_message(user_message)
    
    # Controla se ia vai responder ou não
    if request.form.get('status') == 'ia':
        start_ai_thread(user_message.__dict__)
        
    return redirect(request.referrer)

@chat_bp.route('/exit', methods=['POST'])
def close_chat():
    # Fecha o chat e redireciona para o dashboard
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))

    return redirect(url_for('user.dashboard'))

# Função que vai controlar a IA
def ai(user_message):
    # Resposta da IA e se deve transferir ou não
    ai_response, should_transfer= ia_service.chat_with_ai(user_message['message'], user_message['ticket_id'])

    ai_message = Message({
        'message': ai_response,
        'user_id': 0, # ID da IA no banco de dados
        'ticket_id': user_message['ticket_id']
    })
    message_service.send_message(ai_message)
    
    # Quando a IA ou o usuário pede para ser transferido para um técnico
    if should_transfer:
        ticket_service.change_ticket_status('open', user_message['ticket_id'])

# Inicia a Thread da IA
def start_ai_thread(user_message):
    threading.Thread(target=ai, args=(user_message,)).start()