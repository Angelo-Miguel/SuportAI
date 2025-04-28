# app/controllers/user_controller.py
from flask import Blueprint, render_template, session, redirect, url_for

user_bp = Blueprint('user', __name__)

@user_bp.route('/user')
def dashboard():
    # Página do usuário
    if 'user' not in session:
        return redirect(url_for('auth.login_page'))
    return render_template('user.html', user=session['user'])