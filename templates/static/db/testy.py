import sqlite3

conn = sqlite3.connect('downez.db')
cursor = conn.cursor()

cursor.execute('''
    UPDATE promociones
    SET descuento = 0.1,
        titulo_de_descuento = 'Año del Dragon'
    WHERE id = 5
''')

conn.commit()  # Asegura que los cambios se guarden
print("Promoción actualizada")
conn.close()