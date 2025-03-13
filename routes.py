from main import app
from flask import render_template, request

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/user/<username>')
def user(username):
    return render_template('user.html', username=username)

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    # Aqui você pode validar os dados
    if email == "admin@email.com" and password == "1234":
        return "Login bem-sucedido!"
    else:
        return "E-mail ou senha incorretos!", 401
