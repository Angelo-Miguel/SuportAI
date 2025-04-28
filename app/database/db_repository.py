from app.database.db_connection import MySQLConnection

class BaseRepository:
    def __init__(self):
        self.db = MySQLConnection()
    
    def execute_query(self, query, params=None, fetch_one=False):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            else:
                result = cursor.fetchall()
            
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()