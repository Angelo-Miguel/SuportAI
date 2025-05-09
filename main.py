from flask import Flask
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente
load_dotenv(override=True)

def create_app():
    # Factory function para criar a instância do Flask
    app = Flask(__name__)
    
    # Definindo onde estão os templates e arquivos estáticos.
    app.template_folder='app/templates'
    app.static_folder='app/static'
    
    # Configurações secritas e de debug
    app.secret_key = os.getenv('SECRET_KEY', 'fallback_secret_key')
    app.debug = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't') # DEBUG: Set False in production .env
    
    # Importar e registrar blueprints
    register_blueprints(app)
    
    return app

def register_blueprints(app):
    # Registra todos os blueprints da aplicação
    from app.controllers.auth_controller import auth_bp
    from app.controllers.user_controller import user_bp
    from app.controllers.ticket_controller import ticket_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(ticket_bp)

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=os.getenv('FLASK_HOST', '0.0.0.0'),
        port=int(os.getenv('FLASK_PORT', 5000))
    )