from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = Flask(__name__)
from routes import *

if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG")) # type: ignore # DEBUG: Set False in production .env