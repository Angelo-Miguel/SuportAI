# app/controllers/user_controller.py
from flask import Blueprint, render_template, session, redirect, url_for
from app.services.ticket_service import TicketService

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
def dashboard():
    tickets = TicketService().show_tickets(session['user']['id_user'])
    
    # Página do usuário
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    return render_template('dashboard.html', user=session['user'], tickets=tickets)