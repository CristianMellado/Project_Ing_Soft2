import sqlite3

conn = sqlite3.connect('downez.db')
cursor = conn.cursor()

query = "SELECT id FROM usuarios WHERE username = ? AND id != ?"
cursor.execute(query, ('alex',1))
result = cursor.fetchone()
print(-1 if result is None else result[0])


def obtenerComprasConDestinatario(id_usuario):
    query = """
        SELECT 
            c.nombre_contenido, 
            c.rating, 
            c.tipo_contenido, 
            c.autor, 
            c.id, 
            uc.tipo_transaccion,
            CASE 
                WHEN uc.tipo_transaccion = 'regalo' THEN u.username 
                ELSE NULL 
            END AS destinatario_username
        FROM compras uc
        JOIN contenidos c ON uc.id_contenido = c.id
        LEFT JOIN regalos r ON uc.tipo_transaccion = 'regalo' AND uc.id = r.id_regalo
        LEFT JOIN usuarios u ON r.id_destinatario = u.id
        WHERE uc.id_usuario = ?
    """
    cursor.execute(query, (id_usuario,))
    return cursor.fetchall()

print(obtenerComprasConDestinatario(1))

conn.close()