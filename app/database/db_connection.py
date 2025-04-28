import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(override=True)

class MySQLConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance
    
    def _initialize_connection(self):
        self.connection = mysql.connector.connect(
            host=os.getenv("HOST_DB"),
            user=os.getenv("USER_DB"),
            password=os.getenv("PASSWORD_DB"),
            port=os.getenv("PORT_DB"),
            database=os.getenv("DATABASE_DB")
        )
    
    def get_connection(self):
        if not self.connection.is_connected():
            self._initialize_connection()
        return self.connection
    
    def close_connection(self):
        if self.connection.is_connected():
            self.connection.close()