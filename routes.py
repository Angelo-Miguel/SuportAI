from main import app
from flask import render_template, request, redirect, flash, session
from static.python.connection_db import sqlConn
import hashlib #md5 cript for password

cursor = sqlConn.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = None
    
    if password:
        hashed_password = hashlib.md5(password.encode()).hexdigest()
    try:
        cursor.execute('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', 
                       (nome, email, hashed_password))
        sqlConn.commit()
        return home()
    except Exception as e:
        return f"Erro ao cadastrar: {str(e)}"

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    hashed_password = None
    
    if password:
        hashed_password = hashlib.md5(password.encode()).hexdigest()
    try:
        cursor.execute('SELECT * FROM users WHERE email = %s and password = %s', 
                       (email, hashed_password))
        
        results = cursor.fetchone()
        if cursor.rowcount == 1 and results is not None:
            session['user'] = results
            return user() # type: ignore # FIXME: dict bug
        else:
            flash('Usuário ou senha incorretos!', 'danger')  # Salva a mensagem temporariamente
            return redirect('/')  # Redireciona para a tela de login
    except Exception as e:
        return f'Erro ao executar o Login: {str(e)}' # FIXME: return later 
    
def user():
    return render_template('user.html')

@app .route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')
