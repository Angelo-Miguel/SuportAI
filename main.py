from flask import Flask
from dotenv import load_dotenv
import os
from app.extensions import socketio


# Carrega variáveis de ambiente e forca override 
load_dotenv(override=True)

def create_app():
    # Factory function para criar a instância do Flask
    app = Flask(__name__)
    
    # Configurações
    app.template_folder='app/templates'
    app.static_folder='app/static'
    app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
    app.debug = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    
    # Registrar blueprints
    register_blueprints(app)
    
    # Inicializar SocketIO com o app
    socketio.init_app(app, cors_allowed_origins="*")
    
    return app

def register_blueprints(app):
    from app.controllers.auth_controller import auth_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.ticket_controller import ticket_bp
    from app.controllers.chat_controller import chat_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ticket_bp)
    app.register_blueprint(chat_bp)

if __name__ == '__main__':
    app = create_app()
    socketio.init_app(app)
    socketio.run(
        app,
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )