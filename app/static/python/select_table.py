from connection_db import sqlConn

cursor = sqlConn.cursor()
cursor.execute("SELECT name FROM users WHERE email = 'angelo@gmail.com' and password = 'f7d63bbdc0fda6d3c6ae9c061a86910d'")
result = cursor.fetchone()