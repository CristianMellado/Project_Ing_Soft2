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
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS puntuaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    id_contenido INTEGER,
    puntuacion INTEGER,
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id),
    FOREIGN KEY (id_contenido) REFERENCES contenidos(id)
);
''')

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS promociones (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     id_contenido INTEGER,
#     descuento DOUBLE,
#     titulo_de_descuento TEXT,
#     dias INTEGER,
#     FOREIGN KEY (id_contenido) REFERENCES contenidos(id_contenido)
# );
# ''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarioContenido (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_contenido INTEGER,
    id_usuario INTEGER,
    type TEXT DEFAULT 'compra',
    FOREIGN KEY (id_contenido) REFERENCES contenidos (id),
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS notificaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    messagge TEXT,
    id_contenido INTEGER,
    id_usuario INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES usuarios (id)    
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS contenidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    src BLOB,
    title TEXT,
    author TEXT,
    price DOUBLE,
    extension TEXT,
    category TEXT,
    rating DOUBLE DEFAULT 0.0,
    description TEXT,
    type TEXT
);
''')

archivos = [
    ("../audio/cuentame.mp3", "Cuentame", "pedro", 5.99,'mp3','rock', 0.0,'awesome','audio'),
    ("../image/monalisa.png", "Monalisa", "van", 15.50,'png','art', 0.0,'awesome','imagen'),
    ("../image/nocheestrellada.png", "Noche Estrellada", "govh", 10.75,'png','art', 0.0,'awesome','imagen'),
    ("../video/soccervideogame.mp4", "Soccer Video Game", "ryzse", 29.99,'mp4','game', 0.0,'awesome','video'),
    ("../video/spiderman.mp4", "Spiderman", "sonyc", 19.99,'mp4','accion', 0.0,'awesome','video'),
    ("../audio/techno.mp3", "Techno Music", "technofell", 3.50,'mp3','techno', 0.0,'awesome','audio'),
    ("../video/1.mp4", "lol gameplay warwick", "franciso bejar", 10.0, "mp4", "Categoría del video",  0.0, "Descripción del video", "video"),
    ("../audio/1.mp3", "Married life", "francete moriarty", 10.0, "mp3", "Categoría del video",  0.0, "Descripción del video", "audio"),
    ("../audio/2.mp3", "Lefestin", "charles de jumps", 15.0, "mp3", "Categoría del sonido",  0.0, "Descripción del audio", "audio")
]

for ruta, titulo, autor, precio, ext, cat, rat, des, typ in archivos:
    try:
        with open(ruta, "rb") as f:
            binario = f.read()
        cursor.execute('''
            INSERT INTO contenidos (src, title, author, price, extension, category, rating, description, type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (binario, titulo, autor, precio, ext, cat, rat, des, typ))
    except Exception as e:
        print(f"Error al leer o insertar {ruta}: {e}")

conn.commit()
conn.close()
