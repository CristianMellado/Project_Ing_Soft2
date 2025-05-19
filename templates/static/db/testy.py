import sqlite3

conn = sqlite3.connect('downez.db')
cursor = conn.cursor()

query = "SELECT price FROM contenidos WHERE id = ?"
cursor.execute(query, (1,))
result = cursor.fetchone()[0]
print(result)
conn.close()
