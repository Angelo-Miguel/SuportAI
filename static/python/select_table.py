from connection_db import cursor

cursor.execute('''SELECT * FROM users''')
data = cursor.fetchall()
print(data)