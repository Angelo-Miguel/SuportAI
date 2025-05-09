# app/controllers/ticket_controller.py
from flask import Blueprint, request, session, redirect, render_template, url_for
from app.models.ticket import Ticket

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/new-ticket', methods=['POST'])
def new_ticket():
    print('new_ticket')
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    title = request.form.get('title')
    category = request.form.get('category')
    description = request.form.get('description')
    user_id = session['user']['user_id']
    ticket = Ticket(title=title, category=category, description=description, user_id=user_id)
    ticket.new_ticket()
    return render_template('chat.html', user=session['user'])