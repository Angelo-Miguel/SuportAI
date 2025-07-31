import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_secret_key')
    DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
    TEMPLATE_FOLDER = 'app/templates'
    STATIC_FOLDER = 'app/static'
    FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = 'gpt-4o-mini'
    OPENAI_TEMPERATURE = '0.7'