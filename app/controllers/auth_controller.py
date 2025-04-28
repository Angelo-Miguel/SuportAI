# app/controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, flash, session, url_for
from app.services.auth_service import AuthService
from app.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def home():
    # Rota principal que redireciona para login
    return redirect(url_for('auth.login'))

@auth_bp.route('/login')
def login_page():
    # Exibe a página de login
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login():
    # Processa o formulário de login
    email = request.form.get('email')
    password = request.form.get('password')
    
    auth_service = AuthService()
    user = auth_service.authenticate(email, password)
    
    if user:
        return redirect(url_for('user.dashboard'))
    else:
        return redirect(url_for('auth.login_page'))

# TODO: Implementar o ADM para gerenciar usuários e permissões
@auth_bp.route('/cadastro')
def register_page():
    # Exibe a página de cadastro
    return render_template('cadastro.html')

@auth_bp.route('/cadastrar', methods=['POST'])
def register():
    # Processa o formulário de cadastro
    nome = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    
    user_service = UserService()
    try:
        user_service.create_user(nome, email, password)
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('auth.login_page'))
    except Exception as e:
        flash(f'Erro ao cadastrar: {str(e)}', 'danger')
        return redirect(url_for('auth.register_page'))

@auth_bp.route('/logout')
def logout():
    # Realiza logout do usuário
    session.pop('user', None)
    return redirect(url_for('auth.login_page'))