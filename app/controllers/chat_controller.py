# app/controllers/user_controller.py
from flask import Blueprint, render_template, session, redirect, url_for


chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
def chat():
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    return render_template('chat.html', user=session['user'], ticket=session['ticket'])