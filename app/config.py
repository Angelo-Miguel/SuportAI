import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    # FLASK
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "fallback_secret_key")
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
    TEMPLATE_FOLDER = "app/templates"
    STATIC_FOLDER = "app/static"
    FLASK_HOST = os.getenv("FLASK_HOST", "0.0.0.0")
    FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

    # OPENAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4o-mini"
    OPENAI_TEMPERATURE = 0.7

    # DATABASE
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT = os.getenv("DATABASE_PORT", "5000")
    DATABASE_USER = os.getenv("DATABASE_USER", "root")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "test")
