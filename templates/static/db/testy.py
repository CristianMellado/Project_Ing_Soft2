import sqlite3

conn = sqlite3.connect('downez.db')
cursor = conn.cursor()

query = "SELECT id FROM usuarios WHERE username = ? AND id != ?"
cursor.execute(query, ('alex',1))
result = cursor.fetchone()
print(-1 if result is None else result[0])


def obtenerListaNotificaciones(idU):
    query = """
            SELECT 
                n.id,
                c.id, 
                c.title, 
                n.messagge
            FROM 
                notificaciones n
            JOIN 
                contenidos c ON c.id = n.id_contenido
            WHERE 
                n.id_usuario = ?
        """
    cursor.execute(query, (idU,))
    result = cursor.fetchall()

    lista = [{"id_notificacion": row[0],
                "id_contenido": row[1],
                "title": row[2],
                "messagge": row[3]} for row in result]
    return lista

print(obtenerListaNotificaciones(3))
conn.close()