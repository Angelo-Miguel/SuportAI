# app/controllers/user_controller.py
from flask import Blueprint, render_template, session, redirect, url_for


chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat/<ticket>')
def chat(ticket):
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    
    #TODO: fazer a função get_messages_by_ticket_id
    #TODO: trocar as sessões por classes
    """ messages = ticket.get_messages_by_ticket_id(ticket['ticket_id']) """
    return render_template('chat.html', user=session['user'], ticket=ticket, messages={"1":"Oi, tudo bem?","2":"Sim, e você?","1":"Estou bem, obrigado!"})

""" @chat_bp.route('/send-message', methods=['POST'])
def send_message():
    pass """