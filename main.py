from flask import Flask
from dotenv import load_dotenv
from app.extensions import socketio
from app.config import Config

# Carrega variáveis de ambiente e forca override 
load_dotenv(override=True)

def create_app():
    # Factory function para criar a instância do Flask
    app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER, static_folder=Config.STATIC_FOLDER)
    app.config.from_object(Config)
    
    # Registrar blueprints
    register_blueprints(app)
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

app = create_app()

if __name__ == '__main__':
    socketio.run(
        app,
        host=app.config['FLASK_HOST'],
        port=app.config['FLASK_PORT']
    )