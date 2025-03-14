from main import app
from flask import render_template, request
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
        cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", 
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
        cursor.execute('SELECT name, id_user FROM users WHERE email = %s AND password = %s', 
                       (email, hashed_password))
        results = cursor.fetchone()

        if cursor.rowcount == 1 and results is not None:
            return user(results['name'], results['id_user']) # type: ignore # BUG: is not a dict
        else:
            return f"Login inválido"
    except Exception as e:
        return f"Erro ao executar o Login: {str(e)}" # FIXME: Fix this later 
    
def user(username, id_user):
    return render_template('user.html', username=username, id_user=id_user)