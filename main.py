from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'BEGUB') # type: ignore # SECRET_KEY: Set in .env  # BEGUB: Default value
from routes import *

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG")) # type: ignore # DEBUG: Set False in production .env  