import sqlite3

conn = sqlite3.connect('downez.db')
cursor = conn.cursor()

def imprimir_tabla(nombre_tabla, columnas=None):
    print(f"Tabla: {nombre_tabla}")
    
    if columnas:
        cursor.execute(f"SELECT {', '.join(columnas)} FROM {nombre_tabla}")
    else:
        cursor.execute(f"SELECT * FROM {nombre_tabla}")
    
    filas = cursor.fetchall()
    for fila in filas:
        print(fila)
    print("-" * 50)

# Imprimir todas las tablas
imprimir_tabla('usuarios')
imprimir_tabla('contenidos')  # sin data_contenido
# imprimir_tabla('categorias')
imprimir_tabla('recargas')
imprimir_tabla('movimientos')
imprimir_tabla('puntuaciones')
# imprimir_tabla('promociones')
imprimir_tabla('usuarioContenido')


# Cerrar conexiÃ³n
conn.close()
