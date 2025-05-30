# app/controllers/chat_controller.py
from flask import Blueprint, render_template, session, redirect, url_for
from app.extensions import socketio
from flask_socketio import emit
from datetime import datetime
import threading
from app.services.ticket_service import TicketService
from app.services.message_service import MessageService
from app.services.ai_service import IaService
from app.models.message import Message

chat_bp = Blueprint('chat', __name__)

ticket_service = TicketService()
message_service = MessageService()
ia_service = IaService()

@chat_bp.route('/chat/<ticket_id>')
def chat(ticket_id):
    # Pagina do chat usuário
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    
    ticket = ticket_service.get_ticket_by_id(ticket_id).__dict__
    messages = message_service.show_messages(ticket_id)
    first_user_message = session.pop('first_user_message', None)

    # Lógica para iniciar a primeira msg com a ia e gravar no banco de dados    
    if ticket['status'] == 'ia' and first_user_message and len(messages) == 0:        
        try:
            start_ai_thread(first_user_message)
            message_service.send_message(Message(first_user_message))
            messages = message_service.show_messages(ticket_id)
        except Exception as e:
            print(f"Erro ao enviar primeira mensagem: {e}")
            
    return render_template('chat.html', user=session['user'], ticket=ticket, messages=messages)

@socketio.on('send_message')
def send_message(data):
    # Processo para mandar uma msg
    user_message = Message({
        'message': data['message'],
        'user_id': data['user_id'],
        'ticket_id':  data['ticket_id']
    })
    message_service.send_message(user_message)
    
    last_message = message_service.show_messages(data['ticket_id'])[-1]

    # Verifica se é um datetime antes de formatar
    if isinstance(last_message['sent_at'], datetime): #type: ignore #HACK
        last_message['sent_at'] = last_message['sent_at'].strftime('%H:%M') #type: ignore #HACK

    emit('new_message', last_message, broadcast=True)
    
    # Controla se ia vai responder ou não
    if data['status'] == 'ia':
        start_ai_thread(user_message.__dict__)

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
    
    # Pega a ultima msg
    last_message = message_service.show_messages(user_message['ticket_id'])[-1]
    print("MSG IA: ", last_message)

    # Verifica se é um datetime antes de formatar
    if isinstance(last_message['sent_at'], datetime): #type: ignore #HACK
        last_message['sent_at'] = last_message['sent_at'].strftime('%H:%M') #type: ignore #HACK
    
    socketio.emit('new_message', last_message, namespace='/')
    
    # Quando a IA ou o usuário pede para ser transferido para um técnico
    if should_transfer:
        ticket_service.change_ticket_status('open', user_message['ticket_id'])
        socketio.emit("change_status", "open", namespace='/')

# Inicia a Thread da IA
def start_ai_thread(user_message):
    threading.Thread(target=ai, args=(user_message,)).start()