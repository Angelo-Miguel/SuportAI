# app/controllers/chat_controller.py
from flask import Blueprint, render_template, session, redirect, url_for
from app.extensions import socketio
from flask_socketio import emit
from datetime import datetime
from app.services.ticket_service import TicketService
from app.services.message_service import MessageService
from app.services.ai_service import IaService
from app.models.message import Message
import threading

chat_bp = Blueprint("chat", __name__)

ticket_service = TicketService()
message_service = MessageService()
ia_service = IaService()


# Função utilitária para formatar o horário das mensagens
def format_time(dt):
    return dt.strftime("%H:%M") if isinstance(dt, datetime) else dt


# Função que lida com a resposta da IA
def handle_ai_response(user_message):
    # Envia a mensagem do usuário para a IA e recebe a resposta e se deve transferir para humano
    ai_response, should_transfer = ia_service.chat_with_ai(
        user_message["message"], user_message["ticket_id"]
    )
    ai_message = Message(
        {
            "message": ai_response,
            "user_id": 0,  # 0 representa a IA
            "ticket_id": user_message["ticket_id"],
        }
    )
    # Salva a mensagem da IA no banco
    message_service.send_message(ai_message)

    last_message = message_service.show_messages(user_message["ticket_id"])[-1]
    last_message["sent_at"] = format_time(last_message["sent_at"])
    socketio.emit("new_message", last_message, namespace="/")
    if should_transfer:
        ticket_service.change_ticket_status("open", user_message["ticket_id"])
        socketio.emit("change_status", "open", namespace="/")


# Cria uma nova thread para executar a IA sem travar o servidor principal
def start_ai_thread(user_message):
    threading.Thread(target=handle_ai_response, args=(user_message,)).start()


# Rota para a página de chat, usando o ticket_id
@chat_bp.route("/chat/<ticket_id>")
def chat(ticket_id):
    if "user" not in session:
        return redirect(url_for("auth.login_page"))

    # Busca o ticket e as mensagens relacionadas
    ticket = ticket_service.get_ticket_by_id(ticket_id).__dict__
    messages = message_service.show_messages(ticket_id)

    # Verifica se a IA deve responder à primeira mensagem do usuário
    first_user_message = session.pop("first_user_message", None)
    if ticket["status"] == "ia" and first_user_message and not messages:
        start_ai_thread(first_user_message)
        message_service.send_message(Message(first_user_message))
        messages = message_service.show_messages(ticket_id)

    return render_template(
        "chat.html", user=session["user"], ticket=ticket, messages=messages
    )


# Rota para sair do chat e voltar ao dashboard
@chat_bp.route("/exit", methods=["POST"])
def close_chat():
    if "user" not in session:
        return redirect(url_for("auth.login_page"))
    return redirect(url_for("user.dashboard"))


# Evento SocketIO que trata o envio de novas mensagens do usuário
@socketio.on("send_message")
def send_message(data):
    user_message = Message(
        {
            "message": data["message"],
            "user_id": data["user_id"],
            "ticket_id": data["ticket_id"],
        }
    )

    # Salva a mensagem no banco
    message_service.send_message(user_message)

    last_message = message_service.show_messages(data["ticket_id"])[-1]
    last_message["sent_at"] = format_time(last_message["sent_at"])
    emit("new_message", last_message, broadcast=True)

    # Se o atendimento estiver sob responsabilidade da IA, inicia a thread da IA
    if data["status"] == "ia":
        start_ai_thread(user_message.__dict__)
