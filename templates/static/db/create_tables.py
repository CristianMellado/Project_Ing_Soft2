import sqlite3
import csv
import sys
import os
# Conectar a la base de datos (o crearla si no existe)
# csv.field_size_limit(sys.maxsize)
conn = sqlite3.connect('downez.db')
cursor = conn.cursor()

encoding_t = 'latin-1'

# CREAR LAS TABLAS si no existen
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    username TEXT,
    pswd TEXT,
    saldo DOUBLE DEFAULT 0.0,
    auth INTEGER DEFAULT 0,
    estado TEXT DEFAULT "cliente"
);
''')

db = [
    {"pswd": "ok", "auth": 0, "username": "alex", "saldo": 150, "estado": "cliente", "email": "abc@gmail.com"},
    {"pswd": "123", "auth": 1, "username": "admi", "saldo": -1, "estado": "administrador", "email": "admi@gmail.com"}
]

for user in db:
    cursor.execute('''
    INSERT INTO usuarios (email, username, pswd, saldo, auth, estado)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (user["email"], user["username"], user["pswd"], user["saldo"], user["auth"], user["estado"]))


# cursor.execute('''
# CREATE TABLE IF NOT EXISTS categorias (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     nombre_categoria TEXT,
#     descripcion TEXT
# );
# ''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS recargas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER,
    monto DOUBLE,
    fecha TEXT,
    estado TEXT DEFAULT 'pendiente',    
    FOREIGN KEY (id_user) REFERENCES usuarios(id)
);
''')

e_recargas = [
    {"id_user": 1, "cantidad": 500.0, "fecha": "28-04-2025 10:37:05", "estado": "pendiente"}
]

for rec in e_recargas:
    cursor.execute('''
    INSERT INTO recargas (id_user, monto, fecha, estado)
    VALUES (?, ?, ?, ?)
    ''', (rec["id_user"], rec["cantidad"], rec["fecha"], rec["estado"]))


cursor.execute('''
CREATE TABLE IF NOT EXISTS movimientos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contenido INTEGER,
    id_usuario INTEGER,
    precio DOUBLE,
    fecha TEXT,
    FOREIGN KEY (id_contenido) REFERENCES contenidos(id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);
''')

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS puntuaciones (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_cliente INTEGER,
#     id_contenido INTEGER,
#     puntuacion INTEGER,
#     FOREIGN KEY (id_cliente) REFERENCES usuarios(id),
#     FOREIGN KEY (id_contenido) REFERENCES contenido(id)
# );
# ''')

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS promociones (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_contenido INTEGER,
#     descuento DOUBLE,
#     titulo_de_descuento TEXT,
#     dias INTEGER,
#     FOREIGN KEY (id_contenido) REFERENCES contenido(id_contenido)
# );
# ''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarioContenido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contenido INTEGER,
    id_usuario INTEGER,
    FOREIGN KEY (id_contenido) REFERENCES contenidos (id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS contenidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    src TEXT,
    title TEXT,
    author TEXT,
    price DOUBLE,
    extension TEXT,
    category TEXT,
    rating DOUBLE,
    description TEXT,
    type TEXT
);
''')

archivos = [
    ("static/audio/cuentame.mp3", "Cuentame", "pedro", 5.99,'mp3','rock','2.5','awesome','audio'),
    ("static/image/monalisa.png", "Monalisa", "van", 15.50,'png','art','2.5','awesome','imagen'),
    ("static/image/nocheestrellada.png", "Noche Estrellada", "govh", 10.75,'png','art','2.5','awesome','imagen'),
    ("static/video/soccervideogame.mp4", "Soccer Video Game", "ryzse", 29.99,'mp4','game','2.5','awesome','video'),
    ("static/video/spiderman.mp4", "Spiderman", "sonyc", 19.99,'mp4','accion','2.5','awesome','video'),
    ("static/audio/techno.mp3", "Techno Music", "technofell", 3.50,'mp3','techno','2.5','awesome','audio'),
    ("static/video/1.mp4", "lol gameplay warwick", "franciso bejar", 10.0, "mp4", "Categoría del video", 4.5, "Descripción del video", "video"),
    ("static/audio/1.mp3", "Married life", "francete moriarty", 10.0, "mp3", "Categoría del video", 4.5, "Descripción del video", "audio"),
    ("static/audio/2.mp3", "Lefestin", "charles de jumps", 15.0, "mp3", "Categoría del sonido", 4.8, "Descripción del audio", "audio"),
    ("https://github.com/DretcmU/DOWNEZ/blob/main/templates/static/image/Dedos%20dibujados.jpg?raw=true", "Dedos dibujados", "Konam bursts", 10.0, "jpg", "Categoría de la imagen", 4.5, "Descripción de  la imagen", "imagen")
]

for archivo in archivos:
    filename = archivo[0]
    titulo = archivo[1]
    autor = archivo[2]
    precio = archivo[3]
    ext=archivo[4]
    cat=archivo[5]
    rat=archivo[6]
    des=archivo[7]
    typ=archivo[8]
    #ruta para carpeta multimedia

    cursor.execute('''
    INSERT INTO contenidos (src,title, author, price, extension,category,rating,description,type)
    VALUES (?, ?, ?, ?,?,?,?,?,?)
    ''', (filename,titulo, autor, precio, ext,cat,rat,des,typ))


# relaciones = [
#     (1, 1), 
#     (2, 3),  
#     (3, 3),  
#     (4, 2),  
#     (5, 5),  
#     (6, 6)   
# ]

# # Insertar las relaciones en la tabla intermedia contenido_categoria
# for contenido_id, categoria_id in relaciones:
#     cursor.execute('''
#     INSERT INTO contenido_categoria (id_contenido, id_categoria)
#     VALUES (?, ?)
#     ''', (contenido_id, categoria_id))



# print("Importando usuarios.csv a la tabla usuarios...")
# with open('csv/usuarios.csv', 'r', newline='',  encoding=encoding_t) as file:
#     reader = csv.DictReader(file)

#     for row in reader:
#         if not row:
#             continue  # Saltar filas vacías
        
#         # Orden correcto de columnas
#         valores = [
#             row['email'],
#             row['usuario'],
#             row['contraseña'],
#             row['saldo'],
#             row['tipo'],
#             row['estado_cuenta']
#         ]
        
#         # Insertar en la tabla usuarios
#         cursor.execute('''
#             INSERT INTO usuarios (email, usuario, contraseña, saldo, tipo, estado_cuenta)
#             VALUES (?, ?, ?, ?, ?, ?)
#         ''', valores)



# print("Importando categorias.csv a la tabla categorias...")

# with open('csv/categorias.csv', 'r', newline='',  encoding=encoding_t) as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         cursor.execute('''
#             INSERT INTO categorias (nombre_categoria, descripcion)
#             VALUES (?, ?)
#         ''', (
#             row['nombre_categoria'],
#             row['descripcion']
#         ))

# print("Importando recargas.csv a la tabla recargas...")
# with open('csv/recargas.csv', 'r', newline='',  encoding=encoding_t) as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         cursor.execute('''
#             INSERT INTO recargas (id_recarga, id_cliente, monto, fecha)
#             VALUES (?, ?, ?, ?)
#         ''', (
#             int(row['id_recarga']),
#             int(row['id_cliente']),
#             float(row['monto']),
#             row['fecha']  # La fecha viene como texto, SQLite lo maneja sin problemas
#         ))

# print("Importando movimiento.csv a la tabla movimiento...")

# with open('csv/movimiento.csv', 'r', newline='',  encoding=encoding_t) as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         cursor.execute('''
#             INSERT INTO movimientos ( id_contenido, id_usuario, precio, fecha)
#             VALUES (?, ?, ?, ?)
#         ''', (
#             int(row['id_contenido']),
#             int(row['id_usuario']),
#             float(row['precio']),
#             row['fecha']  # La fecha viene como texto, SQLite lo maneja sin problemas
#         ))

# print("Importando puntuaciones.csv a la tabla puntuaciones...")

# with open('csv/puntuaciones.csv', 'r', newline='',  encoding=encoding_t) as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         cursor.execute('''
#             INSERT INTO puntuaciones ( id_cliente, id_contenido, puntuacion)
#             VALUES (?, ?, ?)
#         ''', (
#             int(row['id_cliente']),
#             int(row['id_contenido']),
#             float(row['puntuacion'])
#         ))

# print("Importando promociones.csv a la tabla promociones...")
# with open('csv/promociones.csv', 'r', newline='',  encoding=encoding_t) as file:
#     reader = csv.DictReader(file)
#     for row in reader:
#         cursor.execute('''
#             INSERT INTO promociones ( id_cliente, id_contenido, descuento, titulo_de_descuento, dias)
#             VALUES (?, ?, ?, ?,?)
#         ''', (
#             int(row['id_cliente']),
#             int(row['id_contenido']),
#             float(row['descuento']),
#             row['titulo_de_descuento'],
#             int(row['dias'])
#         ))
# # Confirmar cambios y cerrar
conn.commit()
conn.close()
