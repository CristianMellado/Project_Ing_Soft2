from datetime import datetime, timedelta
import sqlite3
import base64

DB_PATH = 'templates/static/db/downez.db'

# [RF-0148] Función para retornar el conector de sql para cada clase entidad.
def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

class E_Usuarios:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # [RF-0037] Registrar a un cliente a ex-cliente en la tabla usuarios.
    def registrar_Excliente(self, idU):
        query = "UPDATE usuarios SET estado_cuenta = 'ex-cliente' WHERE id = ?"
        self.cursor.execute(query, (idU,))
        self.conn.commit()

    # [RF-0038] Verifica en la tabla usuarios si el username y password son correctos, siempre y cuando sean clientes o un administrador.
    def verificarLogin(self, username, password):
        query = """
        SELECT 
                role, id 
            FROM 
                usuarios 
            WHERE 
                username = ? AND pswd = ? AND (estado_cuenta = 'cliente' OR estado_cuenta = 'administrador')
        """
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            return result[0], result[1]  # tipo (Administrador/Cliente), id_usuario
        return None, None
    
    # [RF-0039] Obtiene los datos de un usuario por id de la tabla usuarios.
    def obtenerUser(self, id_usuario):
        query="SELECT username, email, saldo, estado_cuenta FROM usuarios WHERE id = ?"
        self.cursor.execute(query, (id_usuario,))
        resultado = self.cursor.fetchone()

        if resultado:
            return {
                "username": resultado[0],
                "email": resultado[1],  
                "saldo": resultado[2],
                "estado":resultado[3]
            }
        return None

    # [RF-0040] Obtiene el saldo de un usuario por id de la tabla usuarios.
    def obtenerSaldo(self, id):
        query = "SELECT saldo FROM usuarios WHERE id = ?"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        print(result)
        if result:
            return result[0]
        return None

    # [RF-0041] Actualiza el saldo de un usuario por id de la tabla usuarios.
    def actualizarSaldo(self,id, cantidad):
        query = "UPDATE usuarios SET saldo = saldo + ? WHERE id = ?"
        self.cursor.execute(query, (cantidad, id))
        self.conn.commit()

    # [RF-0042] Valida los datos un usuario por id de la tabla usuarios, para verificar si existe y sea una cuenta activa.
    def validarDatos(self, username):
        query = "SELECT id FROM usuarios WHERE username = ? AND (estado_cuenta = 'cliente' OR estado_cuenta = 'administrador')"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result is None # si es none, es porque no se encontro, por ende no existe ese usuario a registrar :D
    
    # [RF-0043] Verifica en la tabla usuarios si un cliente existe por id y estado de cuenta.
    def UsuarioExiste(self, username, idU):
        query = "SELECT id FROM usuarios WHERE username = ? AND id != ? AND estado_cuenta = 'cliente'"
        self.cursor.execute(query, (username,idU))
        result = self.cursor.fetchone()
        return -1 if result is None else result[0]
    
    # [RF-0044] Registra un usuario a la tabla usuarios.
    def registrarUsuario(self, username, password, email):
        query = "INSERT INTO usuarios (username, pswd, email) VALUES (?, ?, ?)"
        print("A")
        self.cursor.execute(query, (username, password, email))
        self.conn.commit()
    
    # [RF-0045] Retorna información de varios usuarios por coincidencia de id's o usernames, solo para administradores.
    def buscar_info_usuarios(self, query):
        q_like = f"%{query.lower()}%"
        sql = "SELECT id, username, email, estado_cuenta FROM usuarios WHERE CAST(id AS TEXT) LIKE ? OR LOWER(username) LIKE ?"
        self.cursor.execute(sql, (q_like,q_like))
        result = self.cursor.fetchall()

        lista = []
        for row in result:
            lista.append({
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "type": row[3],
            })
        return lista

class E_Compras:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # [RF-0046] Verifica su un usuario compro cierto contenido, se valida por id's en la tabla compras.
    def verificarContenido(self, idu, idc):
        query = "SELECT id_contenido, id_usuario FROM compras WHERE id_contenido = ? AND id_usuario = ?"
        self.cursor.execute(query, (idc,idu,))
        result = self.cursor.fetchone()
        #print(result)
        if(result is None): return False
        return True
    
    # [RF-0047] Registra una compra de un cliente y retorna el id de la compra.
    def registrarCompra(self, idU, idC,precio, type_trans="compra"):
        query = "INSERT INTO compras (id_usuario,id_contenido, precio, fecha, tipo_compra) VALUES (?, ?, ?, ?,?)"
        fecha = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.cursor.execute(query, (idU, idC, precio, fecha,type_trans))
        transaccion_id = self.cursor.lastrowid  # obtiene el ID insertado
        self.conn.commit()
        return transaccion_id

    # # [RF-0048] Retorna las compras de un cliente de la tabla compras.
    # def obtenerDescargasCliente(self, id_usuario):
    #     query = """
    #         SELECT 
    #             c.nombre_contenido, 
    #             c.rating, 
    #             c.tipo_contenido, 
    #             c.autor, 
    #             c.id, 
    #             uc.tipo_compra,
    #             CASE 
    #                 WHEN uc.tipo_compra = 'regalo' THEN u.username 
    #                 ELSE NULL 
    #             END AS destinatario_username
    #         FROM compras uc
    #         JOIN contenidos c ON uc.id_contenido = c.id
    #         LEFT JOIN regalos r ON uc.tipo_compra = 'regalo' AND uc.id = r.id_regalo
    #         LEFT JOIN usuarios u ON r.id_destinatario = u.id
    #         WHERE uc.id_usuario = ?
    #     """
    #     self.cursor.execute(query, (id_usuario,))
    #     results = self.cursor.fetchall()
    #     lista = []
    #     for row in results:
    #         lista.append({
    #             "title": row[0],
    #             "rating": row[1],
    #             "type": row[2],
    #             "author": row[3],
    #             "id": row[4],
    #             "tipo_compra": row[5] + " al usuario " + row[6] if row[6] else row[5]
    #         })
    #     return lista

    # [RF-0048] Retorna las compras de un cliente de la tabla compras, incluyendo el número de descargas.
    def obtenerDescargasCliente(self, id_usuario):
        query = """
            SELECT 
                c.nombre_contenido, 
                c.rating, 
                c.tipo_contenido, 
                c.autor, 
                c.id, 
                uc.tipo_compra,
                CASE 
                    WHEN uc.tipo_compra = 'regalo' THEN u.username 
                    ELSE NULL 
                END AS destinatario_username,
                IFNULL(d.downloaded, 0) AS num_descargas
            FROM compras uc
            JOIN contenidos c ON uc.id_contenido = c.id
            LEFT JOIN regalos r ON uc.tipo_compra = 'regalo' AND uc.id = r.id_regalo
            LEFT JOIN usuarios u ON r.id_destinatario = u.id
            LEFT JOIN descarga d ON d.id_usuario = uc.id_usuario AND d.id_contenido = c.id
            WHERE uc.id_usuario = ?
        """
        self.cursor.execute(query, (id_usuario,))
        results = self.cursor.fetchall()
        lista = []
        for row in results:
            lista.append({
                "title": row[0],
                "rating": row[1],
                "type": row[2],
                "author": row[3],
                "id": row[4],
                "tipo_compra": row[5] + " al usuario " + row[6] if row[6] else row[5],
                "descargas": row[7]
            })
        return lista

class E_Regalos(E_Compras):
    def __init__(self):
        super().__init__()

    # [RF-0049] Registra un regalo en tabla compras y el destinatario en la tabla regalos.
    def registrarRegalo(self, idU, idC, precio, type_trans, id_des):
        id_trans = self.registrarCompra(idU,idC,precio,type_trans)
        query = "INSERT INTO regalos (id_regalo, id_destinatario) VALUES (?, ?)"
        self.cursor.execute(query, (id_trans,id_des))
        self.conn.commit()

    # [RF-0050] Verifica si el destinarario ya tiene el contenido.
    def verificarContenidoDestinatario(self, id_des, idc):
        query = """
            SELECT 
                c.id
            FROM 
                compras c
            JOIN 
                regalos r ON c.id = r.id_regalo
            WHERE 
                c.id_contenido = ? AND r.id_destinatario = ?
        """
        self.cursor.execute(query, (idc, id_des))
        result = self.cursor.fetchone()
        return result is not None
    
class E_Puntuaciones:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # [RF-0051] Registra una puntuación en la tabla puntuaciones.
    def Registrar_Puntuacion(self, user_id, id_contenido, puntuacion):
        if not self.Existe_Puntuacion(user_id,id_contenido):
            # Paso 1: Insertar nueva puntuación
            insert_query = "INSERT INTO puntuaciones (id_contenido, id_cliente, puntuacion) VALUES (?, ?, ?)"
            self.cursor.execute(insert_query, (id_contenido, user_id, puntuacion,))
        else:
            update_query = "UPDATE puntuaciones SET puntuacion = ? WHERE id_contenido = ? AND id_cliente = ?"
            self.cursor.execute(update_query, (puntuacion, id_contenido, user_id,))
        self.conn.commit()

        # Paso 2: Calcular el nuevo promedio de puntuaciones
        promedio_query = "SELECT AVG(puntuacion) FROM puntuaciones WHERE id_contenido = ?"
        self.cursor.execute(promedio_query, (id_contenido,))
        promedio = self.cursor.fetchone()[0]

        # Paso 3: Actualizar el campo 'rating' en la tabla contenidos
        update_query = "UPDATE contenidos SET rating = ? WHERE id = ?"
        self.cursor.execute(update_query, (promedio, id_contenido))
        self.conn.commit()
    
    # [RF-0052] Verifica si ya existe una puntuación en la tabla puntuaciones.
    def Existe_Puntuacion(self, idU,idC):
        query = "SELECT * FROM puntuaciones WHERE id_cliente = ? AND id_contenido = ?"
        self.cursor.execute(query, (idU,idC,))
        result = self.cursor.fetchone()
        if(result is None): return False
        return True

class E_Notificaciones:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # [RF-0053] Registra una notificación en la tabla notificiones, y retorna un html de un resultado de un contenido como notifiación.
    def registrarNotificacionRegalo(self, idU, idC, msg):
        query="SELECT nombre_contenido, id FROM contenidos WHERE id = ?"
        self.cursor.execute(query, (idC,))
        result = self.cursor.fetchone()
        full_msg = f"<strong>Titulo:<a href=item_view.html?id={result[1]}></strong> {result[0]}</a></p><p>{msg}"
        query = "INSERT INTO notificaciones (id_usuario, messagge) VALUES (?, ?)"
        self.cursor.execute(query, (idU, full_msg))
        self.conn.commit()
    
    # [RF-0054] Registra una notificación en la tabla notificiones de tipo recarga.
    def registrarNotificacionRecarga(self, idU, msg):
        query = "INSERT INTO notificaciones (id_usuario, messagge) VALUES (?, ?)"
        self.cursor.execute(query, (idU, msg))
        self.conn.commit()

    # [RF-0055] Obtiene una lista de todas las notifiaciones para cierto cliente.
    def obtenerListaNotificaciones(self, idU):
        query = """
                SELECT 
                    n.id,
                    n.messagge
                FROM 
                    notificaciones n
                WHERE 
                    n.id_usuario = ?
            """
        self.cursor.execute(query, (idU,))
        result = self.cursor.fetchall()

        lista = [{"id_notificacion": row[0],
                    "messagge": row[1]} for row in result]
        return lista
    
    # [RF-0056] Acepta una notifiación y la marca como leída, esta es eliminada de la tabla notificaciones.
    def aceptarNotificacion(self, id_noti):
        query_delete = "DELETE FROM notificaciones WHERE id = ?"
        self.cursor.execute(query_delete, (id_noti,))
        self.conn.commit()
            
class E_Recargas:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # [RF-0057] Regista una solicitud de recarga de un cliente.
    def registrarSolicitud(self, monto, user_id):
        fecha = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        query = "INSERT INTO recargas (id_user, monto, fecha) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user_id, monto, fecha))
        self.conn.commit()

    # [RF-0058] Obtiene una lista de todas las peticiones de recargas de saldo, para el administrador.
    def obtenerListaPeticiones(self):
        query = """
            SELECT 
                recargas.id, 
                usuarios.username, 
                recargas.monto, 
                recargas.fecha, 
                recargas.estado
            FROM 
                recargas
            JOIN 
                usuarios ON recargas.id_user = usuarios.id
            WHERE 
                recargas.estado = 'pendiente' AND usuarios.estado_cuenta = 'cliente'
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        lista = [{"id_recarga": row[0],
                "usuario": row[1],
                "monto": row[2],
                "fecha": row[3],
                "estado": row[4]} for row in result]

        return lista
    
    # [RF-0059] Retorna información del historial de recargas de un cliente según su id.
    def obtenerRecargasCliente(self, idU):
        query = """
            SELECT 
                id,
                monto,
                fecha,
                estado
            FROM 
                recargas
            WHERE 
                id_user = ?
        """
        self.cursor.execute(query,(idU))
        result = self.cursor.fetchall()

        lista = [{"id_recarga": row[0],
                "monto": row[1],
                "fecha": row[2],
                "estado": row[3]} for row in result]

        return lista
    
    # [RF-0060] El administrador prueba una recarga de un cliente.
    def aprobarRecarga(self, id_recarga):
        query = "SELECT id_user, monto FROM recargas WHERE id = ? AND estado = 'pendiente'"
        self.cursor.execute(query, (id_recarga,))
        result = self.cursor.fetchone()
        if result:
            id_user, monto = result
            query_set = "UPDATE recargas SET estado = 'aprobada' WHERE id = ?"
            self.cursor.execute(query_set, (id_recarga,))
            self.conn.commit()
            return id_user, monto
        return None, None
    
class E_Promociones:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # [RF-0162] Se retornan todas las promociones disponibles de la tabla promociones.
    def obtenerPromociones(self):
        self.cursor.execute('''
            SELECT id, descuento, titulo_de_descuento,fecha_fin FROM promociones
        ''')
        
        promociones = self.cursor.fetchall()
        results = []
        for promo in promociones:
            results.append({
                "id": promo[0],
                "descuento": promo[1],
                "titulo_de_descuento": promo[2],
                "fecha_fin": promo[3]
            })

        return results
    
    # [RF-0165] Retorna el descuento de la tabla promociones de cierto id de promoción.
    def ObtenerPromocion(self, idprom):
        self.cursor.execute("SELECT descuento FROM promociones WHERE id = ?", (idprom,))
        resultado_promo = self.cursor.fetchone()
        return resultado_promo

    # [RF-0177] Se registra una nueva promocion a la tabla promociones.
    def agregarPromocion(self, data):
        try:
            fecha_futura = datetime.now() + timedelta(days=data.get("dias"))
            fecha_str = fecha_futura.strftime("%Y-%m-%d")
            descuento = float(data.get("descuento"))/100.0
            query = "INSERT INTO promociones (titulo_de_descuento,descuento, fecha_fin) VALUES (?, ?, ?)"
            self.cursor.execute(query, (data.get("titulo"), descuento, fecha_str))
            self.conn.commit()
            return True
        except:
            return False


class E_Contenidos:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    # [RF-0061] Registra un contenido en la tabla contenidos.
    def registrarContenido(self, data):
        query = """
            INSERT INTO contenidos (
                Archivo_bytes,
                nombre_contenido,
                autor,
                precio,
                extension,
                categoria,
                rating,
                descripcion,
                tipo_contenido
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            data["src"],
            data["title"],
            data["author"],
            float(data["price"]),
            data["extension"],
            data["category"],
            float(data["rating"]),
            data["description"],
            data["type"]
        ))
        self.conn.commit()

    # [RF-0062] Actualiza un contenido existente en la tabla contenidos.
    def actualizarContenido(self, data):
        campos_validos = {
            "Archivo_bytes": data.get("src"),
            "nombre_contenido": data.get("title"),
            "autor": data.get("author"),
            "precio": float(data["price"]) if data.get("price") is not None else None,
            "extension": data.get("extension"),
            "categoria": data.get("category"),
            "rating": float(data["rating"]) if data.get("rating") is not None else None,
            "descripcion": data.get("description"),
            "tipo_contenido": data.get("type")
        }

        # Filtrar solo campos que no son None
        columnas = []
        valores = []

        for campo, valor in campos_validos.items():
            if valor is not None:
                columnas.append(f"{campo} = ?")
                valores.append(valor)

        if not columnas:
            return  # Nada que actualizar

        query = f"""
            UPDATE contenidos SET
                {', '.join(columnas)}
            WHERE id = ?
        """

        valores.append(data["id"])
        self.cursor.execute(query, tuple(valores))
        self.conn.commit()

    # [RF-0063] Obtiene contenidos con toda su información y con la opcion de retornar en orden del mas descargado al menos decargador.
    def obtenerContenidos(self, top=False):
        query = """
            SELECT id, Archivo_bytes, nombre_contenido, autor, precio, descripcion, rating,
                tipo_contenido, categoria, extension, downloaded, id_promocion
            FROM contenidos WHERE estado='activo'
        """
        if top:
            query += " ORDER BY downloaded DESC"

        self.cursor.execute(query)
        result = self.cursor.fetchall()
        lista = []

        for row in result:
            (id_, src_bin, title, author, price, desc, rating,
            tipo, category, ext, down, id_prom) = row

            # Generar data URL para el contenido
            data_url = C_Contenidos._generar_data_url(src_bin, tipo, ext)

            # Verificar si tiene promoción y modificar el precio si es necesario
            if id_prom is not None:
                self.cursor.execute("SELECT titulo_de_descuento, descuento FROM promociones WHERE id = ?", (id_prom,))
                promo_row = self.cursor.fetchone()
                if promo_row:
                    titulo_prom,descuento = promo_row
                    precio_final = round(float(price) * (1 - descuento), 2)
                    price = f"<span style='color:green;'>{precio_final}</span> <s>{price}</s> ({titulo_prom})"

            lista.append({
                "id": id_,
                "src": data_url,
                "title": title,
                "author": author,
                "price": price,
                "description": desc,
                "rating": rating,
                "type": tipo,
                "category": category,
                "downloaded": down
            })

        return lista

    # [RF-0064] Retorna contenidos para cierta coincidencia con un query y con filtros de la tabla contenidos.
    def Buscar_info(self, query="", filters=None, admi=False):
        if filters is None:
            filters = []

        sql = "SELECT id, nombre_contenido, autor, tipo_contenido, estado FROM contenidos WHERE 1=1"
        if not admi:
            sql +=" AND estado='activo'"

        params = []

        tipos = [f.lower() for f in filters if f.lower() in ["imagen", "video", "audio"]]
        if tipos:
            placeholders = ", ".join(["?"] * len(tipos))
            sql += f" AND LOWER(tipo_contenido) IN ({placeholders})"
            params.extend(tipos)

        filters_lower = [f.lower() for f in filters]

        if query:
            if "id" in filters_lower:
                sql += " AND CAST(id AS TEXT) LIKE ?"
                params.append(f"%{query}%")
            else:
                if "author" in filters_lower:
                    sql += " AND LOWER(autor) LIKE ?"
                    params.append(f"%{query.lower()}%")
                else:
                    sql += " AND (LOWER(nombre_contenido) LIKE ? OR CAST(id AS TEXT) LIKE ? OR LOWER(autor) LIKE ?)"
                    params.extend([f"%{query.lower()}%", f"%{query.lower()}%", f"%{query.lower()}%"])

        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()

        lista = []
        for row in result:
            lista.append({
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "type": row[3]+"/"+row[4] if admi else row[3],
            })
        return lista

    # [RF-0065] Retorna cierto contenido por su Id de la tabla contenidos.
    def getContent(self, content_id):
        query = "SELECT * FROM contenidos WHERE id = ?"
        self.cursor.execute(query, (content_id,))
        row = self.cursor.fetchone()
        
        if row:
            keys = ['id', 'src', 'title', 'author', 'price', 'extension', 'category',
                    'rating', 'description', 'type', 'downloaded', 'estado', 'id_promocion']
            content_dict = dict(zip(keys, row))

            # convertir binario a data URL
            content_dict["src"] = C_Contenidos._generar_data_url(
                content_dict["src"], content_dict["type"], content_dict["extension"]
            )

            # Verificar si tiene promoción
            id_prom = content_dict.get("id_promocion")
            if id_prom is not None:
                self.cursor.execute("SELECT titulo_de_descuento, descuento FROM promociones WHERE id = ?", (id_prom,))
                promo_row = self.cursor.fetchone()
                if promo_row:
                    titulo_prom,descuento = promo_row
                    precio_final = round(float(content_dict["price"]) * (1 - descuento), 2)
                    content_dict["price"] = f"<span style='color:green;'>{precio_final}</span> <s>{content_dict["price"]}</s> ({titulo_prom})"

            return content_dict
        else:
            return None

    # [RF-0066] Retorna el precio de cierto contenido por id.
    def obtenerPrecio(self, content_id):
        query = "SELECT precio FROM contenidos WHERE id = ?"
        self.cursor.execute(query, (content_id,))
        return self.cursor.fetchone()[0]

    # [RF-0067] Veritica si un contenido contiene una promoción en la tabla promociones.
    def verificarPromocion(self, idC):
        self.cursor.execute("SELECT id_promocion FROM contenidos WHERE id = ?", (idC,))
        resultado = self.cursor.fetchone()
        
        # Retorna True si hay una promoción asociada, False si no
        return resultado is not None and resultado[0] is not None
    
    # [RF-0068] Retorna el archivo binario de un contenido id para descargarlo.
    def obtenerBinarioPorID(self, idC):
        self.cursor.execute("SELECT Archivo_bytes, nombre_contenido, extension FROM contenidos WHERE id = ?", (idC,))
        row = self.cursor.fetchone()
        if row:
            return {
                "src": row[0],  # binario
                "title": "_".join(row[1].split(" ")),
                "extension": row[2]  # etc.
            }
        return None
    
    # [RF-0149] Verificar si ya existe registro en la tabla descarga.
    def downloadedContentVerificate(self, id_contenido, id_usuario):
        query_check_descarga = """
            SELECT downloaded FROM descarga
            WHERE id_usuario = ? AND id_contenido = ?
        """
        self.cursor.execute(query_check_descarga, (id_usuario, id_contenido))
        result = self.cursor.fetchone()
        return result

    # [RF-0069] Actualiza el número de descargas hechas de cierto contenido.
    def downloadCount(self, id_contenido, id_usuario):
        # Aumentar contador global del contenido
        query_update_contenido = """
            UPDATE contenidos SET
                downloaded = downloaded + 1
            WHERE id = ?
        """
        self.cursor.execute(query_update_contenido, (id_contenido,))
        self.conn.commit()
        

        if self.downloadedContentVerificate(id_contenido,id_usuario):
            # Ya existe, actualizar descargado
            query_update_descarga = """
                UPDATE descarga SET
                    downloaded = downloaded + 1
                WHERE id_usuario = ? AND id_contenido = ?
            """
            self.cursor.execute(query_update_descarga, (id_usuario, id_contenido))
        else:
            # No existe, insertar nuevo registro
            query_insert_descarga = """
                INSERT INTO descarga (id_usuario, id_contenido, downloaded)
                VALUES (?, ?, 1)
            """
            self.cursor.execute(query_insert_descarga, (id_usuario, id_contenido))

        self.conn.commit()
    
    # [RF-0155] Se actualiza el estado de un contenido en la tabla contenidos.
    def actualizarEstadoContenido(self, idC):
        self.cursor.execute("SELECT estado FROM contenidos WHERE id = ?", (idC,))
        row = self.cursor.fetchone()
        
        if not row:
            print("Contenido no encontrado")
            return None

        estado_actual = row[0]
        
        if estado_actual.lower() == "activo":
            nuevo_estado = "desactivado"
            resultado = True
        else:
            nuevo_estado = "activo"
            resultado = False

        self.cursor.execute("UPDATE contenidos SET estado = ? WHERE id = ?", (nuevo_estado, idC))
        self.conn.commit()
        return resultado
    
    # [RF-0163] Retorna de la tabla conteidos, el precio de un contenido y su id de promoción.
    def get_Prom(self, idC):
        self.cursor.execute("SELECT precio, id_promocion FROM contenidos WHERE id = ?", (idC,))
        resultado = self.cursor.fetchone()
        if resultado is None:
            return None
        return resultado
    
    # [RF-0171] La clase E_Contenidos le asignacion de una promocion a un contenido en su tabla contenidos.
    def asignarPromocion(self, idC, idP):
        try:
            self.cursor.execute("UPDATE contenidos SET id_promocion = ? WHERE id = ?", (idP, idC))
            self.conn.commit()
            return True
        except:
            return False

class C_Puntuacion:
    def __init__(self):
        pass
    
    # [RF-0070] Pide a la tabla puntuaciones la puntuación de cierto contenido.
    def Obtener_Puntuacion(self, idU, idC):
        e_pun = E_Puntuaciones()
        return e_pun.Existe_Puntuacion(idU, idC)
    
    # [RF-0071] Envia una puntuacion para cierto contenido a la tabla puntuaciones.
    def Enviar_Puntuacion(self, idU, idC, score):
       e_pun = E_Puntuaciones()
       e_pun.Registrar_Puntuacion(idU,idC,score)


class C_Promociones:
    def __init__(self):
        pass

    # [RF-161] El Controlador contenidos solicita al controlador Promociones todas las promociones actuales.
    def obtenerPromociones(self):
        prom_manager = E_Promociones()
        return prom_manager.obtenerPromociones()
    
    # [RF-0166] El controlador promociones solicita la promocion de cierto id promocion a la clase E_Promociones.
    def ObtenerPromocion(self, idprom):
        prom_manager = E_Promociones()
        return prom_manager.ObtenerPromocion(idprom)        
    
    # [RF-0176] El Controlador promociones enviar a la clase  E_Promociones la agregación de una promocion.
    def agregarPromocion(self, data):
        man_prom = E_Promociones()
        return man_prom.agregarPromocion(data)   

class C_Transacciones:
    def __init__(self):
        pass

    # [RF-0072] Verifica si el tipo de tarjeta es valido.
    def verificarMetPago(self, Ncard, cardType):
        generate_Bancos_disponibles = lambda a: a in ["mastercard","bcp","visa","paypal"]
        return generate_Bancos_disponibles(cardType)
    
    # [RF-0073] Realizar en envio a la tabla recargas de una solicitud de recargas y verificar si la tarjeta tiene el saldo suficiente.
    def realizarPago(self, user_id, amount, Ncard):
        pagoTarjeta = lambda a,b : 1
        if pagoTarjeta(amount, Ncard):
            controller = E_Recargas()
            controller.registrarSolicitud(amount, user_id)
            return 0
        return 1
    
    # [RF-0074] Pide a la tabla recargas la lista de peticiones de recargas.
    def obtenerListaPeticiones(self):
        controller = E_Recargas()
        return controller.obtenerListaPeticiones()
    
    # [RF-0075] Pide a la clase de recargas el historial de descargas de cierto usuario.
    def obtenerRecargasCliente(self, idU):
        controller = E_Recargas()
        return controller.obtenerRecargasCliente(idU)
    
    # [RF-0076] Envia a la clase recargas la aprobación de cierta recarga.
    def aprobarRecarga(self, id_recarga):
        controller = E_Recargas()
        id_user, cantidad = controller.aprobarRecarga(id_recarga)
        return id_user, cantidad
    
    # [RF-0077] Verifica en las respectivas clases de promociones y contenido para retornar el precio final de cierto contenido que tenga un descuento.
    def ProcesarPrecioFinal(self, idC):
        man_cont = C_Contenidos()
        precio_original, id_promocion = man_cont.get_Prom(idC)

        if id_promocion is None:
            return precio_original

        man_prom = C_Promociones()
        resultado_promo = man_prom.ObtenerPromocion(id_promocion)

        descuento = resultado_promo[0]  # Esperado entre 0.0 y 1.0
        precio_final = precio_original * (1 - descuento)
        return round(precio_final, 2)

    # [RF-0078] Solicita a la clase usuarios la actualizacion del saldo de cierto cliente.
    def actualizarSaldo(self, idU, precio):
        controller = E_Usuarios()
        controller.actualizarSaldo(idU, precio)

    # [RF-0079] Envia a las clases compras o regalos cierto contenido para ser registrado.
    def registrarCompra(self, idU, idC, precio, id_des=None):
        if id_des==None:
            uscont = E_Compras()
            uscont.registrarCompra(idU,idC,precio,'compra')
        else:
            uscont = E_Regalos()
            uscont.registrarRegalo(idU,idC,precio,'regalo',id_des)

    # [RF-0080] Verifica en las clases compras y regalos si cierto contenido le pertenece a cierto cliente.
    def verificarContenido(self, idu, idc):
        us_trans = E_Compras()
        us_rega = E_Regalos()     
        if us_trans.verificarContenido(idu,idc) or us_rega.verificarContenidoDestinatario(idu,idc):
            return True
        return False
    
class C_Contenidos:
    def __init__(self):
        pass

    # [RF-0081] Envia a la clase de entidad contenidos el registro de un contenido.
    def registrarContenido(self, data):
        contenidos = E_Contenidos()
        contenidos.registrarContenido(data)
    
    # [RF-0082] Envia a la clase de entidad contenidos actulizar un cierto contenido.
    def actualizarContenido(self, data):
        contenidos = E_Contenidos()
        contenidos.actualizarContenido(data)

    # [RF-0083] Envia a la clase de entidad contenidos la consulta de cierto contenido por un query y filtros.
    def consultarDatos(self, query, filters):
        query = query.lower().strip()
        resultados = []

        contenidos = E_Contenidos()
        A =  contenidos.obtenerContenidos()


        aut = 0 
        if 'author' in filters:
            filters.remove('author')
            aut = 1

        for item in A:
            if len(filters)==0 or item["type"] in filters:
                titulo = item.get('title', '').lower()
                author = item.get('author', '').lower()
                if query in titulo or (aut and query in author):
                    resultados.append({
                        'title': titulo,
                        'author': author,
                        'type': item["type"],
                        'id': item["id"]
                    })

        return resultados
    
    # [RF-0084] Envia a la clase de entidad contenidos la busqueda de cierto contenido por query y filtros pero tambien por id, para la busqueda de informacion de un administrador.
    def solicitar_info_contenido(self, query, filters, admi=False):
        contenidos = E_Contenidos()
        return contenidos.Buscar_info(query,filters, admi)
    
    # [RF-0085] Funcion que conbierte el contenido binario a Base64, leible para el frontend.
    @staticmethod
    def _generar_data_url(bin_data, tipo, extension):
        # Parte	Explicación:
        # data:	Esquema que indica que se trata de un Data URL.
        # image/png	Tipo MIME del contenido (imagen en formato PNG en este caso).
        # ;base64	Indica que los datos están codificados en Base64.
        # iVBORw0KGgoAAA...	Los datos binarios del archivo codificados en Base64.
        # data_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA..."
        # <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA..." />        
        mime_types = {
            "imagen": f"image/{extension}",
            "audio": f"audio/{extension}",
            "video": f"video/{extension}"
        }
        mime_type = mime_types.get(tipo, "application/octet-stream")
        encoded = base64.b64encode(bin_data).decode("utf-8")
        return f"data:{mime_type};base64,{encoded}"
    
    # [RF-0086] Envia a la clase de entidad contenidos obtener una lista de los top 10 más descargados de cada tipo de contenido.
    @staticmethod
    def getTopContent():
        contenidos = E_Contenidos()
        todos = contenidos.obtenerContenidos(top=True)

        top_imagenes = []
        top_audios = []
        top_videos = []

        for item in todos:
            tipo = item['type']
            if tipo == 'imagen' and len(top_imagenes) < 10:
                top_imagenes.append(item)
            elif tipo == 'audio' and len(top_audios) < 10:
                top_audios.append(item)
            elif tipo == 'video' and len(top_videos) < 10:
                top_videos.append(item)

            # Si ya tienes 10 de cada tipo, puedes salir del bucle
            if len(top_imagenes) == 10 and len(top_audios) == 10 and len(top_videos) == 10:
                break

        return top_imagenes + top_audios + top_videos
    
    # [RF-0087] Envia a la clase de entidad contenidos obtener cierto contenido por su id.
    def getContent(self, content_id):
        contenidos = E_Contenidos()
        return contenidos.getContent(content_id)
    
    # [RF-0088] Envia a la clase de entidad contenidos, obtener el precio de cierto contenido por su id.
    def obtenerPrecio(self, content_id):
        contenidos = E_Contenidos()
        return contenidos.obtenerPrecio(content_id)
    
    # [RF-0089] Envia a la clase de entidad contenidos, la verificación de promocion de cierto contenido.
    def verificarPromocion(self, idC):
        contenidos = E_Contenidos()
        return contenidos.verificarPromocion(idC)
    
    # [RF-0090] Solicita a la clase controlador promociones  la puntuación a registrar pra cierto contenido.
    def Obtener_Puntuacion(self, idU, idC):
        c_pun = C_Puntuacion()
        return c_pun.Obtener_Puntuacion(idU, idC)
    
    # [RF-0091] Envia a la clase controlador promociones  la puntuación a registrar pra cierto contenido.
    def Enviar_Puntuacion(self, idU, idC, score):
       ctr = C_Puntuacion()
       ctr.Enviar_Puntuacion(idU,idC,score)
    
    # [RF-0092] Envia a la clase de entidad contenidos, la solicitud de obtener toda la información de cierto contenido para ser descargado
    def obtenerContenidoBinarios(self, idC, idU):
        conte = E_Contenidos()
        contenido  = conte.obtenerBinarioPorID(idC)
        conte.downloadCount(idC, idU)

        if contenido:
            bin_data = contenido['src']
            extension = contenido['extension']
            filename = contenido['title'].replace(" ", "_") + "." + extension

            mime_map = {
                        # Imágenes
                        "png": "image/png",
                        "jpg": "image/jpeg",
                        "jpeg": "image/jpeg",
                        "gif": "image/gif",
                        "bmp": "image/bmp",
                        "webp": "image/webp",
                        "svg": "image/svg+xml",
                        "tiff": "image/tiff",
                        "ico": "image/x-icon",

                        # Audio
                        "mp3": "audio/mpeg",
                        "wav": "audio/wav",
                        "ogg": "audio/ogg",
                        "aac": "audio/aac",
                        "flac": "audio/flac",
                        "m4a": "audio/mp4",
                        "mid": "audio/midi",
                        "oga": "audio/ogg",

                        # Video
                        "mp4": "video/mp4",
                        "webm": "video/webm",
                        "mov": "video/quicktime",
                        "avi": "video/x-msvideo",
                        "mkv": "video/x-matroska",
                        "flv": "video/x-flv",
                        "wmv": "video/x-ms-wmv",
                        "3gp": "video/3gpp",
            }
            mime_type = mime_map.get(extension.lower(), "application/octet-stream") 
            return mime_type, bin_data, filename
        return None,None,None
    
    # [RF-153] El controlador contenidos solicita a la tabla E_Contenidos, si cierto contenido fue descargado.
    def downloadedContentVerificate(self, idc, idu):
        e_con = E_Contenidos()
        return e_con.downloadedContentVerificate(idc,idu) is not None
    
    # [RF-154] El controlador contenidos solicita actualizar el estado de un contenido en su tabla de E_Contenidos.
    def actualizarEstadoContenido(self, idC):
        e_con = E_Contenidos()
        return e_con.actualizarEstadoContenido(idC)
    
    # [RF-160] El Controlador contenidos solicita al controlador Promociones todas las promociones actuales.
    def obtenerPromociones(self):
        prom_manager = C_Promociones()
        return prom_manager.obtenerPromociones()   

    # [RF-0164] el controlador conteidos solicita a la clase E_Contenidos cierto promocion por su id.
    def get_Prom(self, idC):
        e_con = E_Contenidos()
        return e_con.get_Prom(idC)
    
    # [RF-0170] El controlador contenidos envia la clase E_Contenidos la asignacion de una promocion.
    def asignarPromocion(self, idC, idP):
        e_con = E_Contenidos()
        return e_con.asignarPromocion(idC,idP)
    
    # [RF-0175] El Controlador contenidos enviar a su controlador promociones la agregación de una promocion.
    def agregarPromocion(self, data):
        man_prom = C_Promociones()
        return man_prom.agregarPromocion(data)   

class C_Usuario:
    def __init__(self):
        self.id = None
    
    # [RF-0093] Solicita a la clase de entidad usuarios, obtener los datos de cierto usuario por su id.
    def getDataUser(self, id_user):
        usuarios = E_Usuarios()
        return usuarios.obtenerUser(id_user)
    
    # [RF-0094] Solicita a la clase controlador contenidos, buscar contenidos con cierto query y filtro.
    def Buscar(self, query,filters):
        # content_manager = C_Contenidos()
        # return content_manager.consultarDatos(query,filters)
        content_manager = C_Contenidos()
        resultados = content_manager.solicitar_info_contenido(query, filters)
        return resultados
    
    # [RF-0095] Solicita a la controlador contenidos, obtener cierto contenido por su id.
    def seleccionarContent(self, content_id):
        content_manager = C_Contenidos()
        return content_manager.getContent(content_id)
    
    # [RF-0096] Solicita a la clase de entidad usuarios, verificar los datos de cierto usuario por su id.
    def loginVerificar(self, username, password):
        usuarios = E_Usuarios()
        return usuarios.verificarLogin(username,password)
    
    # [RF-0097] Solicita a la clase controlador Contenidos, los top contenidos a mostrar.
    def getContentView(self):
        content_manager = C_Contenidos()
        return content_manager.getTopContent()

    # [RF-0098] Solicita a la clase de entidad usuarios, verificar si cierto username esta en uso.
    def validarRegistro(self, user):
        us = E_Usuarios()
        return us.validarDatos(user)

    # [RF-0099] Envia a la clase de entidad usuarios, el registro de un nuevo usuario.
    def registrarUsuario(self, user,ps,em):
        us = E_Usuarios()
        us.registrarUsuario(user,ps,em)

    # [RF-0100] Solicita a la clases controlador transacciones y contenidos, verificar si fue comprado por cierto usuario y si fue puntuado.
    def verificarContenido(self, idU, idC):
        c_usContenido = C_Transacciones()
        content_manager = C_Contenidos()
        res = {'success':c_usContenido.verificarContenido(idU, idC), 
               'hasRated':content_manager.downloadedContentVerificate(idC, idU)}
        return res
    
    # [RF-00101] Solicita a la clase de entidad compras, la lista de compras realizadas por cierto cliente.
    def obtenerDescargasCliente(self, idU):
        uscont = E_Compras()
        return uscont.obtenerDescargasCliente(idU)
    
    # [RF-00102] Solicita a la clase controlador transacciones, la lista de recargas de cierto cliente.
    def obtenerRecargasCliente(self, idU):
        controller_trans = C_Transacciones()
        return controller_trans.obtenerRecargasCliente(idU)
    
    # [RF-00103] Solicita a la clase controlador contenidos, cierto contenido, para ser descargado.
    def obtenerContenidoDescarga(self,content_id,idU):
        controller = C_Contenidos()
        return controller.obtenerContenidoBinarios(content_id, idU) 

class C_Cliente(C_Usuario):
    def __init__(self):
        super().__init__()

    # [RF-00104] Solicita a la clase controlador transacciones, el metodo de pago de tarjeta  y si tiene saldo suficiente en la tarjeta.
    def enviarSolicitud(self, Ncard, amount, cardType, id_user):
        controller = C_Transacciones()
        if not controller.verificarMetPago(Ncard,cardType):
            return {"success": False, "message":"Metodo de pago invalido"}
        if controller.realizarPago(id_user, amount, Ncard):
            return {"success": False, "message":"Saldo insuficiente"}
        return {"success": True}
    
    # [RF-00105] Solicita a la clase entidad usuarios, el saldo actual del cliente.
    def obtenerSaldo(self, id_user):
        usuarios = E_Usuarios()
        return usuarios.obtenerSaldo(id_user)
    
    # [RF-00106] Solicita a la clase controlador transacciones y contenidos, el pago de cierto contenido.
    def pagarContenido(self, idU, idC, id_des=None):
        controller_trans = C_Transacciones()
        controller_cont = C_Contenidos()
        saldo = self.obtenerSaldo(idU) 

        if controller_cont.verificarPromocion(idC):
            precioFinal = controller_trans.ProcesarPrecioFinal(idC)
        else:
            precioFinal = controller_cont.obtenerPrecio(idC)
            print(precioFinal)

        if saldo > precioFinal:
            controller_trans.actualizarSaldo(idU, -precioFinal)
        else:
            return False
        if id_des == None:
            controller_trans.registrarCompra(idU, idC, precioFinal)
        else:
            controller_trans.registrarCompra(idU, idC, precioFinal, id_des=id_des)
        return True
    
    # [RF-00107] Solicita a la clase controlador contenidos, obtener la puntuación de cierto conteido.
    def Obtener_Puntuacion(self, idU):
        ctr = C_Contenidos()
        return ctr.Obtener_Puntuacion(idU)
    
    # [RF-00108] Envia a la clase controlador contenidos, la puntuación de cierto conteido.
    def Enviar_Puntuacion(self, idU, idC, score):
       ctr = C_Contenidos()
       ctr.Enviar_Puntuacion(idU,idC,score)

    # [RF-0109] Envia a la clase entiedad usuarios, controlador transacciones, y a entidad notificaciones, la compra de un regalo de cierto cliente a otro.
    def Enviar_destinatario(self, idU, idC, destinatario):
        res = {'success':False}
        e_us = E_Usuarios()
        id_des = e_us.UsuarioExiste(destinatario, idU)
        if id_des==-1:
            res['msg']="El destinatario no existe."
        else:
            c_rega = C_Transacciones()
            if c_rega.verificarContenido(id_des, idC):
                res['msg'] = 'El destinatario ya tiene el contenido.'
            else:
                if not self.pagarContenido(idU, idC,id_des=id_des):
                    res['msg'] = 'Saldo insuficiente.'
                else:
                    res['success'] = True
                    e_notifi = E_Notificaciones()
                    from_user = e_us.obtenerUser(idU)['username']
                    e_notifi.registrarNotificacionRegalo(id_des, idC, f"Regalo de parte de {from_user}.")
        return res
    
    # [RF-0110] Solicita a la clase entidad usuarios, validar el saldo de cierto cliente para ver si es posible registrarlo como ex-cliente.
    def SolicitarValidarSaldo(self, idU):
        if (self.obtenerSaldo(idU) == 0):
            usuarios = E_Usuarios()
            usuarios.registrar_Excliente(idU)
            return True
        return False
    
    # [RF-0111] Solicita a la clase entidad notificaciones, obtener la lista de notifaciones para cierto usuario.
    def obtenerNotificaciones(self, idU):
        e_notifi = E_Notificaciones()
        res = e_notifi.obtenerListaNotificaciones(idU)
        #res.extend(e_notifi.obtenerListaNotificacionesRecargas(idU))
        return res
    
    # [RF-0112] Envia a la clase entidad notificaciones, aceptar cierta notifacion para marcar como leida.
    def aceptarNotificacion(self, idN):
        e_notifi = E_Notificaciones()
        e_notifi.aceptarNotificacion(idN)
    
    # [RF-0113] Solicita a la clase entidad usuarios y controlador transacciones, retirar el saldo de cierto usuario.
    def Retirar_Saldo(self, card, cardType, idU):
        usuarios = E_Usuarios()
        monto = usuarios.obtenerSaldo(idU)
        controller_trans = C_Transacciones()
        #controller_trans.RegistrarRetiro(card, cardType, idU, monto)
        usuarios.actualizarSaldo(idU, -monto)
        return True
    
class C_Administrador(C_Usuario):
    def __init__(self):
        super().__init__()
    
    # [RF-0114] Solicita a la clase controlador transacciones, obtener la lista de recargas.
    def getRecargas(self):
        controller = C_Transacciones()
        return controller.obtenerListaPeticiones()
    
    # [RF-0115] Envia a la clase controlador transacciones y entidad notifaciones, la aprobación de cierta recarga.
    def aprobarRecarga(self, id_recarga):
        controller = C_Transacciones()
        id_user,cantidad = controller.aprobarRecarga(id_recarga)
        controller.actualizarSaldo(id_user,cantidad)
        print(id_user,cantidad)
        # usuarios = E_Usuarios()
        # usuarios.actualizarSaldo(id_user, cantidad)
        e_noti = E_Notificaciones()
        e_noti.registrarNotificacionRecarga(id_user,f"Recarga de ${cantidad} aprobada.")

    # [RF-0116] Envia a la clase controlador contenidos, un contenido nuevo a registrar.
    def ingresarAgregarContenido(self, datos):
        content_manager = C_Contenidos()
        content_manager.registrarContenido(datos)

    # [RF-0117] Envia a la clase controlador contenidos, actualizar un contenido existente.
    def actualizarContenido(self, datos):
        content_manager = C_Contenidos()
        content_manager.actualizarContenido(datos)

    # [RF-0118] Solicita a la clase controlador contenidos y entidad usuarios, buscar información sobre estos.
    def buscar_info(self, data):
        resultados = []
        filters = data['filters']
        if 'cliente' not in filters:
            content_manager = C_Contenidos()
            resultados = content_manager.solicitar_info_contenido(data['query'], filters, True)
        if not ('audio' in filters or 'video' in filters or 'imagen' in filters or 'author' in filters):
            usuarios = E_Usuarios()
            resultados += usuarios.buscar_info_usuarios(data['query'])

        return resultados
    
    # [RF-0119] Solicita a la clase entidad usuarios, obtener datos de cierto usuario según su id.
    def seleccionarUser(self, id):
        usuarios = E_Usuarios()
        return usuarios.obtenerUser(id)

    # [RF-0152] Envia al controlador Contenidos la actualización de estado de un contenido.
    def actualizarEstadoContenido(self, idC):
        content_manager = C_Contenidos()
        return {"success": True, "estado": content_manager.actualizarEstadoContenido(idC)}
    
    # [RF-159] El Controlador Administrador solicita al controlador Contenidos todas las promociones actuales.
    def obtenerPromociones(self):
        content_manager = C_Contenidos()
        return content_manager.obtenerPromociones()

    # [RF-0169] El controlador administrador envia al controlador contenidos la asignacion de una promocion.
    def asignarPromocion(self, idC, idP):
        man_content = C_Contenidos()
        return man_content.asignarPromocion(idC,idP)    
    
    # [RF-0174] El Controlador administrador enviar a su controlador contenidos la agregación de una promocion.
    def agregarPromocion(self, data):
        man_content = C_Contenidos()
        return man_content.agregarPromocion(data)   

class Usuario:
    def __init__(self, user=None, id=None, ctr=C_Usuario()):
        self.user = user
        self.id = id
        self.controller = ctr

    # [RF-0120] Envía credenciales a su controlador Usuario: Iniciar sesión del usuario
    def iniciar_sesion(self, username, password):
        auth, self.id = self.controller.loginVerificar(username, password)
        return auth

    # [RF-0121] Solicita datos a su controlador Usuario: Buscar contenidos con filtros
    def Buscar(self, query, filters):
        print(self.user, self.id)
        return self.controller.Buscar(query, filters)

    # [RF-0122] Envía solicitud a su controlador Usuario: Seleccionar un contenido específico
    def seleccionar(self, content_id):
        return self.controller.seleccionarContent(content_id)

    # [RF-0123] Solicita información a su controlador Usuario: Obtener los datos del usuario
    def getDataUser(self):
        return self.controller.getDataUser(self.id)

    # [RF-0124] Envía datos a su controlador Usuario: Registrar un nuevo usuario (placeholder)
    def registrarU(self, data):
        return 1

    # [RF-0125] Solicita información a su controlador Usuario: Obtener contenidos destacados o generales
    def getContentView(self):
        return self.controller.getContentView()

    # [RF-0126] Envía datos a su controlador Usuario: Validar y registrar un nuevo usuario
    def validarRegistro(self, us, ps, em):
        if not self.controller.validarRegistro(us):
            return 0
        self.controller.registrarUsuario(us, ps, em)
        return 1

    # [RF-0127] Verifica existencia a su controlador Usuario: Verificar si el usuario ya tiene un contenido
    def verificarContenido(self, idC):
        return self.controller.verificarContenido(self.id, idC)

    # [RF-0128] Envía respuesta a su controlador Usuario: Aceptar una notificación
    def aceptarNotificacion(self, idN):
        self.controller.aceptarNotificacion(idN)

    # [RF-0129] Solicita contenido a su controlador Usuario: Obtener contenido para descargar
    def obtenerContenidoDescarga(self, content_id):
        return self.controller.obtenerContenidoDescarga(content_id, self.id)


class Cliente(Usuario):
    def __init__(self, username, id):
        super().__init__(user=username, id=id, ctr=C_Cliente())
        self.saldo = None
        self.estado_cuenta = None

    # [RF-0130] Envía solicitud a su controlador Cliente: Solicitar recarga de saldo con tarjeta
    def ingresarMontoSolicitar(self, Ncard, amount, cardType):
        return self.controller.enviarSolicitud(Ncard, amount, cardType, self.id)

    # [RF-0131] Solicita información a su controlador Cliente: Obtener el saldo actual del cliente
    def getSaldo(self):
        return self.controller.obtenerSaldo(self.id)

    # [RF-0132] Envía pago a su controlador Cliente: Realizar el pago de un contenido
    def pagarContenido(self, idC):
        return self.controller.pagarContenido(self.id, idC)

    # [RF-0133] Solicita información a su controlador Cliente: Obtener descargas realizadas por el cliente
    def obtenerDescargasCliente(self):
        return self.controller.obtenerDescargasCliente(self.id)

    # [RF-0134] Solicita puntuación a su controlador Cliente: Obtener puntuación de contenido dada por un cliente
    def Obtener_Puntuacion(self, idU):
        return self.controller.Obtener_Puntuacion(idU)

    # [RF-0135] Envía puntuación a su controlador Cliente: Enviar una puntuación para un contenido
    def Enviar_Puntuacion(self, idC, score):
        try:
            self.controller.Enviar_Puntuacion(self.id, idC, score)
        except Exception as e:
            print(f"Error al enviar puntuación: {e}")
            return False
        return True

    # [RF-0136] Envía regalo a su controlador Cliente: Enviar un contenido a otro usuario como regalo
    def Enviar_destinatario(self, idC, destinatario):
        return self.controller.Enviar_destinatario(self.id, idC, destinatario)

    # [RF-0137] Solicita notificaciones a su controlador Cliente: Obtener notificaciones del cliente
    def obtenerNotificaciones(self):
        return self.controller.obtenerNotificaciones(self.id)

    # [RF-0138] Solicita validación a su controlador Cliente: Solicitar validación del saldo disponible
    def SolicitarValidarSaldo(self):
        return self.controller.SolicitarValidarSaldo(self.id)

    # [RF-0139] Envía solicitud a su controlador Cliente: Retirar saldo a una tarjeta del cliente
    def Retirar_Saldo(self, card, cardType):
        return self.controller.Retirar_Saldo(card, cardType, self.id)


class Administrador(Usuario):
    def __init__(self, username, id):
        super().__init__(user=username, id=id, ctr=C_Administrador())

    # [RF-0140] Solicita lista a su controlador Administrador: Obtener lista de solicitudes de recargas pendientes
    def obtenerRecargas(self):
        return self.controller.getRecargas()

    # [RF-0141] Envía aprobación a su controlador Administrador: Aprobar la recarga de saldo de un cliente
    def aprobarSaldoCliente(self, id_recarga):
        self.controller.aprobarRecarga(id_recarga)

    # [RF-0142] Envía datos a su controlador Administrador: Registrar nuevo contenido en el sistema
    def ingresarAgregarContenido(self, datos):
        self.controller.ingresarAgregarContenido(datos)

    # [RF-0143] Envía datos a su controlador Administrador: Actualizar información de contenido existente
    def actualizarContenido(self, datos):
        self.controller.actualizarContenido(datos)

    # [RF-0144] Solicita información a su controlador Administrador: Buscar información general sobre contenidos
    def buscar_info(self, data):
        return self.controller.buscar_info(data)

    # [RF-0145] Solicita selección a su controlador Administrador: Seleccionar un usuario específico por ID
    def seleccionar_user(self, id):
        return self.controller.seleccionarUser(id)

    # [RF-0146] Solicita datos a su controlador Administrador: Obtener descargas realizadas por un cliente
    def obtenerDescargasCliente(self, idU):
        return self.controller.obtenerDescargasCliente(idU)

    # [RF-0147] Solicita datos a su controlador Administrador: Obtener recargas realizadas por un cliente
    def obtenerRecargasCliente(self, idU):
        return self.controller.obtenerRecargasCliente(idU)
    
    # [RF-151] Envia id de un contenido para actulizar el estado de este al controlador Administrador.
    def actualizarEstadoContenido(self, idC):
        return self.controller.actualizarEstadoContenido(idC)
    
    # [RF-158] Solicita al controlador Administrador todas las promociones actuales.
    def obtenerPromociones(self):
        return self.controller.obtenerPromociones()
    
    # [RF-0168] El administrador enviar a su controlador administrador la asignacion de una promocion.
    def asignarPromocion(self, idC, idP):
        return self.controller.asignarPromocion(idC,idP)
    
    # [RF-0173] El administrador enviar a su controlador administrador la agregación de una promocion.
    def agregarPromocion(self, data):
        return self.controller.agregarPromocion(data)    