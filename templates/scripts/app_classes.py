import datetime
import sqlite3

DB_PATH = 'templates/static/db/downez.db'

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    return conn

class E_Usuarios:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def verificarLogin(self, username, password):
        query = "SELECT auth, id FROM usuarios WHERE username = ? AND pswd = ?"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            return result[0], result[1]  # tipo (Administrador/Cliente), id_usuario
        return None, None

    def obtenerUser(self, id_usuario):
        query="SELECT username, email, saldo, estado FROM usuarios WHERE id = ?"
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

    def obtenerSaldo(self, id):
        query = "SELECT saldo FROM usuarios WHERE id = ?"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        print(result)
        if result:
            return result[0]
        return None

    def actualizarSaldo(self,id, cantidad):
        query = "UPDATE usuarios SET saldo = saldo + ? WHERE id = ?"
        self.cursor.execute(query, (cantidad, id))
        self.conn.commit()

    def validarDatos(self, username):
        query = "SELECT id FROM usuarios WHERE username = ?"
        self.cursor.execute(query, (username,))
        result = self.cursor.fetchone()
        return result is None # si es none, es porque no se encontro, por ende no existe ese usuario a registrar :D
    
    def UsuarioExiste(self, username, idU):
        query = "SELECT id FROM usuarios WHERE username = ? AND id != ?"
        self.cursor.execute(query, (username,idU))
        result = self.cursor.fetchone()
        return -1 if result is None else result[0]
        
    def registrarUsuario(self, username, password, email):
        query = "INSERT INTO usuarios (username, pswd, email) VALUES (?, ?, ?)"
        print("A")
        self.cursor.execute(query, (username, password, email))
        self.conn.commit()
    
    def buscar_info_usuarios(self, query):
        q_like = f"%{query.lower()}%"
        sql = "SELECT id, username, email, estado FROM usuarios WHERE CAST(id AS TEXT) LIKE ? OR LOWER(username) LIKE ?"
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

class E_Movimientos:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def registrarMovimiento(self, idU, idC, precio):
        query = "INSERT INTO movimientos (id_contenido, id_usuario, precio, fecha) VALUES (?, ?, ?, ?)"
        fecha = str(datetime.datetime.now())
        self.cursor.execute(query, (idU, idC, precio, fecha))
        self.conn.commit()

    def actualizarSaldo(self, idU, precio):
        query_set = "UPDATE usuarios SET saldo = saldo - ? WHERE id = ?"
        self.cursor.execute(query_set, (precio, idU))
        self.conn.commit()

class E_UsuarioContenido:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def verificarContenido(self, idu, idc):
        query = "SELECT id_contenido, id_usuario FROM usuarioContenido WHERE id_contenido = ? AND id_usuario = ?"
        self.cursor.execute(query, (idc,idu,))
        result = self.cursor.fetchone()
        #print(result)
        if(result is None): return False
        return True
    
    def registrarCompra(self, idU, idC, type="compra"):
        query = "INSERT INTO usuarioContenido (id_contenido, id_usuario, type) VALUES (?, ?, ?)"
        self.cursor.execute(query, (idC, idU, type))
        self.conn.commit()

    def obtenerDescargasCliente(self, id_usuario):
        query = """
            SELECT c.title, c.rating, c.type, c.author, c.id
            FROM usuarioContenido uc
            JOIN contenidos c ON uc.id_contenido = c.id
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
                "id": row[4]
            })
        return lista
    
class E_Puntuaciones:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def Registrar_Puntuacion(self, user_id, id_contenido, puntuacion):
        # Paso 1: Insertar nueva puntuación
        insert_query = "INSERT INTO puntuaciones (id_contenido, id_cliente, puntuacion) VALUES (?, ?, ?)"
        self.cursor.execute(insert_query, (id_contenido, user_id, puntuacion))
        self.conn.commit()

        # Paso 2: Calcular el nuevo promedio de puntuaciones
        promedio_query = "SELECT AVG(puntuacion) FROM puntuaciones WHERE id_contenido = ?"
        self.cursor.execute(promedio_query, (id_contenido,))
        promedio = self.cursor.fetchone()[0]

        # Paso 3: Actualizar el campo 'rating' en la tabla contenidos
        update_query = "UPDATE contenidos SET rating = ? WHERE id = ?"
        self.cursor.execute(update_query, (promedio, id_contenido))
        self.conn.commit()

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

    def registrarNotificacionRegalo(self, idU, idC, msg):
        query = "INSERT INTO notificaciones (id_usuario, id_contenido, messagge) VALUES (?, ?, ?)"
        self.cursor.execute(query, (idU, idC, msg))
        self.conn.commit()

    def registrarNotificacionRecarga(self, idU, msg):
        query = "INSERT INTO notificaciones (id_usuario, id_contenido, messagge) VALUES (?, ?, ?)"
        self.cursor.execute(query, (idU, -1, msg))
        self.conn.commit()

    def obtenerListaNotificaciones(self, idU):
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
        self.cursor.execute(query, (idU,))
        result = self.cursor.fetchall()

        lista = [{"id_notificacion": row[0],
                    "id_contenido": row[1],
                    "title": row[2],
                    "messagge": row[3]} for row in result]
        return lista
    
    def obtenerListaNotificacionesRecargas(self, idU):
        query = """
                SELECT 
                    id,
                    id_contenido, 
                    messagge
                FROM 
                    notificaciones
                WHERE 
                    id_usuario = ? AND id_contenido = -1
            """
        self.cursor.execute(query, (idU,))
        result = self.cursor.fetchall()

        lista = [{"id_notificacion": row[0],
                    "id_contenido": row[1],
                    "title": 0,
                    "messagge": row[2]} for row in result]
        return lista
        
    def aceptarNotificacion(self, id_noti):
        query_delete = "DELETE FROM notificaciones WHERE id = ?"
        self.cursor.execute(query_delete, (id_noti,))
        self.conn.commit()
            
class E_Recargas:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()

    def registrarSolicitud(self, monto, user_id):
        fecha = str(datetime.datetime.now())
        query = "INSERT INTO recargas (id_user, monto, fecha) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user_id, monto, fecha))
        self.conn.commit()

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
                recargas.estado = 'pendiente'
        """
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        lista = [{"id_recarga": row[0],
                "usuario": row[1],
                "monto": row[2],
                "fecha": row[3],
                "estado": row[4]} for row in result]

        return lista
    
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
    

class E_Contenidos:
    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        
    def registrarContenido(self, data):
        query = """
            INSERT INTO contenidos (
                src,
                title,
                author,
                price,
                extension,
                categorys,
                rating,
                description,
                types
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(query, (
            data["src"],
            data["title"],
            data["author"],
            float(data["price"]),
            data["extension"],
            data["categorys"],
            float(data["rating"]),
            data["description"],
            data["type"]
        ))

        self.conn.commit()

    def obtenerContenidos(self):
        query = "SELECT id, src, title, author, price, description, rating, type,category FROM contenidos"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        lista = []
        for row in result:
            lista.append({
                "id": row[0],
                "src": row[1],
                "title": row[2],
                "author": row[3],
                "price": row[4],
                "description":row[5],
                "rating":row[6],
                "type":row[7],
                "category":row[8]
            })
        return lista
    
    def Buscar_info(self, query="", filters=None):
        if filters is None:
            filters = []

        sql = "SELECT id, title, author, type FROM contenidos WHERE 1=1"
        params = []

        tipos = [f.lower() for f in filters if f.lower() in ["imagen", "video", "audio"]]
        if tipos:
            placeholders = ", ".join(["?"] * len(tipos))
            sql += f" AND LOWER(type) IN ({placeholders})"
            params.extend(tipos)

        filters_lower = [f.lower() for f in filters]

        if query:
            if "id" in filters_lower:
                sql += " AND CAST(id AS TEXT) LIKE ?"
                params.append(f"%{query}%")
            else:
                if "author" in filters_lower:
                    sql += " AND LOWER(author) LIKE ?"
                    params.append(f"%{query.lower()}%")
                else:
                    sql += " AND (LOWER(title) LIKE ? OR CAST(id AS TEXT) LIKE ? OR LOWER(author) LIKE ?)"
                    params.extend([f"%{query.lower()}%", f"%{query.lower()}%",f"%{query.lower()}%"])

        self.cursor.execute(sql, params)
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
    
    def getContent(self, content_id):
        query = "SELECT * FROM contenidos WHERE id = ?"
        self.cursor.execute(query, (content_id,))
        row = self.cursor.fetchone()
        
        if row:
            keys = [desc[0] for desc in self.cursor.description]
            return dict(zip(keys, row))
        else:
            return None
        
    def obtenerPrecio(self, content_id):
        query = "SELECT price FROM contenidos WHERE id = ?"
        self.cursor.execute(query, (content_id,))
        row = self.cursor.fetchone()[0]
        return row
                
    def verificarPromocion(self, idC):
        return 0
        
class C_Puntuacion:
    def __init__(self):
        pass

    def Obtener_Puntuacion(self, idU, idC):
        e_pun = E_Puntuaciones()
        return e_pun.Existe_Puntuacion(idU, idC)
    
    def Enviar_Puntuacion(self, idU, idC, score):
       e_pun = E_Puntuaciones()
       e_pun.Registrar_Puntuacion(idU,idC,score)

class C_Transacciones:
    def __init__(self):
        pass
    def verificarMetPago(self, Ncard, cardType):
        generate_Bancos_disponibles = lambda a: a in ["mastercard","bcp","visa"]
        return generate_Bancos_disponibles(cardType)
    
    def realizarPago(self, user_id, amount, Ncard):
        pagoTarjeta = lambda a,b : 1
        if pagoTarjeta(amount, Ncard):
            controller = E_Recargas()
            controller.registrarSolicitud(amount, user_id)
            return 0
        return 1
    def obtenerListaPeticiones(self):
        controller = E_Recargas()
        return controller.obtenerListaPeticiones()
    
    def aprobarRecarga(self, id_recarga):
        controller = E_Recargas()
        id_user, cantidad = controller.aprobarRecarga(id_recarga)
        return id_user, cantidad
    
    def ProcesarPrecioFinal(self, idC):
        return 1
    
    def registrarTransaccion(self, idU,idC, precio):
        controller = E_Movimientos()
        controller.registrarMovimiento(idU, idC, precio)

    def actualizarSaldo(self, idU, precio):
        controller = E_Usuarios()
        controller.actualizarSaldo(idU, precio) 

class C_Content:
    def get_id(self):
        return 1
    def registrarContenido(self, data):
        contenidos = E_Contenidos()
        contenidos.registrarContenido(data)

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
    
    def solicitar_info_contenido(self, query, filters):
        contenidos = E_Contenidos()
        return contenidos.Buscar_info(query,filters)
     
    @staticmethod
    def getContentView():
        contenidos = E_Contenidos()
        return contenidos.obtenerContenidos()
    
    def getContent(self, content_id):
        contenidos = E_Contenidos()
        return contenidos.getContent(content_id)
    
    def obtenerPrecio(self, content_id):
        contenidos = E_Contenidos()
        return contenidos.obtenerPrecio(content_id)
    
    def verificarPromocion(self, idC):
        contenidos = E_Contenidos()
        return contenidos.verificarPromocion(idC)
    
    def Obtener_Puntuacion(self, idU, idC):
        c_pun = C_Puntuacion()
        return c_pun.Obtener_Puntuacion(idU, idC)
    
    def Enviar_Puntuacion(self, idU, idC, score):
       ctr = C_Puntuacion()
       ctr.Enviar_Puntuacion(idU,idC,score)

class C_Usuario:
    def __init__(self):
        self.id = None
    
    def getDataUser(self, id_user):
        usuarios = E_Usuarios()
        return usuarios.obtenerUser(id_user)

    def Buscar(self, query,filters):
        # content_manager = C_Content()
        # return content_manager.consultarDatos(query,filters)
        content_manager = C_Content()
        resultados = content_manager.solicitar_info_contenido(query, filters)
        return resultados
    
    def seleccionarContent(self, content_id):
        content_manager = C_Content()
        return content_manager.getContent(content_id)
    
    def loginVerificar(self, username, password):
        usuarios = E_Usuarios()
        return usuarios.verificarLogin(username,password)
    
    def getContentView(self):
        content_manager = C_Content()
        return content_manager.getContentView()

    def validarRegistro(self, user):
        us = E_Usuarios()
        return us.validarDatos(user)

    def registrarUsuario(self, user,ps,em):
        us = E_Usuarios()
        us.registrarUsuario(user,ps,em)

    def verificarContenido(self, idU, idC):
        e_usContenido = E_UsuarioContenido()
        content_manager = C_Content()
        res = {'success':e_usContenido.verificarContenido(idU, idC), 
               'hasRated':content_manager.Obtener_Puntuacion(idU, idC)}
        return res


class C_Cliente(C_Usuario):
    def __init__(self):
        super().__init__()

    def enviarSolicitud(self, Ncard, amount, cardType, id_user):
        controller = C_Transacciones()
        if not controller.verificarMetPago(Ncard,cardType):
            return {"success": False, "message":"Metodo de pago invalido"}
        if controller.realizarPago(id_user, amount, Ncard):
            return {"success": False, "message":"Saldo insuficiente"}
        return {"success": True}
    
    def obtenerSaldo(self, id_user):
        usuarios = E_Usuarios()
        return usuarios.obtenerSaldo(id_user)
    
    def registrarCompra(self, idU, idC, type='compra'):
        uscont = E_UsuarioContenido()
        uscont.registrarCompra(idU,idC,type)
        
    def pagarContenido(self, idU, idC, id_des=None):
        controller_trans = C_Transacciones()
        controller_cont = C_Content()
        saldo = self.obtenerSaldo(idU) 

        if controller_cont.verificarPromocion(idC):
            precioFinal = controller_trans.ProcesarPrecioFinal(idC)
        else:
            precioFinal = controller_cont.obtenerPrecio(idC)
            print(precioFinal)

        if saldo > precioFinal:
            controller_trans.actualizarSaldo(idU, -precioFinal)
            controller_trans.registrarTransaccion(idU, idC, precioFinal)
        else:
            return False
        if id_des == None:
            self.registrarCompra(idU, idC)
        else:
            self.registrarCompra(id_des, idC, "regalo")
        return True
    
    def obtenerDescargasCliente(self, idU):
        uscont = E_UsuarioContenido()
        return uscont.obtenerDescargasCliente(idU)
    
    def Obtener_Puntuacion(self, idU):
        ctr = C_Content()
        return ctr.Obtener_Puntuacion(idU)
    
    def Enviar_Puntuacion(self, idU, idC, score):
       ctr = C_Content()
       ctr.Enviar_Puntuacion(idU,idC,score)

    def Enviar_destinatario(self, idU, idC, destinatario):
        res = {'success':False}
        e_us = E_Usuarios()
        id_des = e_us.UsuarioExiste(destinatario, idU)
        if id_des==-1:
            res['msg']="El destinatario no existe."
        else:
            e_uscont = E_UsuarioContenido()
            if e_uscont.verificarContenido(id_des, idC):
                res['msg'] = 'El destinatario ya tiene el contenido.'
            else:
                if not self.pagarContenido(idU, idC,id_des=id_des):
                    res['msg'] = 'Dinero insuficiente para la compra.'
                else:
                    res['success'] = True
                    e_notifi = E_Notificaciones()
                    from_user = e_us.obtenerUser(idU)['username']
                    e_notifi.registrarNotificacionRegalo(id_des, idC, f"Regalo de parte de {from_user}.")
        return res
    
    def obtenerNotificaciones(self, idU):
        e_notifi = E_Notificaciones()
        res = e_notifi.obtenerListaNotificaciones(idU)
        res.extend(e_notifi.obtenerListaNotificacionesRecargas(idU))
        return res
    
    def aceptarNotificacion(self, idN):
        e_notifi = E_Notificaciones()
        e_notifi.aceptarNotificacion(idN)
    
class C_Administrador(C_Usuario):
    def __init__(self):
        super().__init__()

    def getRecargas(self, estado=1):
        controller = C_Transacciones()
        return controller.obtenerListaPeticiones()
    
    def aprobarRecarga(self, id_recarga):
        controller = C_Transacciones()
        id_user,cantidad = controller.aprobarRecarga(id_recarga)
        print(id_user,cantidad)
        usuarios = E_Usuarios()
        usuarios.actualizarSaldo(id_user, cantidad)
        e_noti = E_Notificaciones()
        e_noti.registrarNotificacionRecarga(id_user,f"Recarga de ${cantidad} aprobada.")

    def ingresarAgregarContenido(self, datos):
        content_manager = C_Content()
        content_manager.registrarContenido(datos)

    def buscar_info(self, data):
        resultados = []
        filters = data['filters']
        if 'cliente' not in filters:
            content_manager = C_Content()
            resultados = content_manager.solicitar_info_contenido(data['query'], filters)
        if not ('audio' in filters or 'video' in filters or 'imagen' in filters or 'author' in filters):
            usuarios = E_Usuarios()
            resultados += usuarios.buscar_info_usuarios(data['query'])

        return resultados
    
    def seleccionarUser(self, id):
        usuarios = E_Usuarios()
        return usuarios.obtenerUser(id)
    
class Usuario:
    def __init__(self,user=None,id=None, ctr=C_Usuario()):
        self.user = user
        self.id = id
        self.controller = ctr
        
    def iniciar_sesion(self, username, password):
        auth, self.id = self.controller.loginVerificar(username,password)
        return auth
    
    def Buscar(self, query,filters):
        print(self.user, self.id)
        return self.controller.Buscar(query,filters)
    
    def seleccionar(self, content_id):
        return self.controller.seleccionarContent(content_id)
    
    def getDataUser(self):
        return self.controller.getDataUser(self.id)
    
    def registrarU(self, data):
        return 1
    
    def getContentView(self):
        return self.controller.getContentView()
    
    def validarRegistro(self, us, ps, em):
        if not self.controller.validarRegistro(us):
            return 0
        self.controller.registrarUsuario(us,ps,em)
        return 1
    
    def verificarContenido(self, idC):
        return self.controller.verificarContenido(self.id, idC)
    def aceptarNotificacion(self, idN):
        self.controller.aceptarNotificacion(idN)
    
class Cliente(Usuario):
    def __init__(self, username, id):
        super().__init__(user=username,id=id,ctr=C_Cliente())
        self.saldo = None
        self.estado_cuenta = None

    def ingresarMontoSolicitar(self, Ncard, amount, cardType):
        return self.controller.enviarSolicitud(Ncard, amount, cardType, self.id)
    
    def getSaldo(self):
        return self.controller.obtenerSaldo(self.id)
    
    def pagarContenido(self, idC):
        return self.controller.pagarContenido(self.id, idC)
    def obtenerDescargasCliente(self):
        return self.controller.obtenerDescargasCliente(self.id)
    def Obtener_Puntuacion(self, idU):
        return self.controller.Obtener_Puntuacion(idU)
    def Enviar_Puntuacion(self, idC, score):
        try:
            self.controller.Enviar_Puntuacion(self.id,idC,score)
        except:
            return False
        return True
    
    def Enviar_destinatario(self, idC, destinatario):
        return self.controller.Enviar_destinatario(self.id, idC, destinatario)
    def obtenerNotificaciones(self):
        return self.controller.obtenerNotificaciones(self.id)
    
class Administrador(Usuario):
    def __init__(self, username, id):
        super().__init__(user=username,id=id,ctr=C_Administrador())

    def obtenerRecargas(self):
        return self.controller.getRecargas()
    
    def aprobarSaldoCliente(self, id_recarga):
        self.controller.aprobarRecarga(id_recarga)
    
    def ingresarAgregarContenido(self, datos):
        self.controller.ingresarAgregarContenido(datos)
    
    def buscar_info(self, data):
        return self.controller.buscar_info(data)
    
    def seleccionar_user(self, id):
        return self.controller.seleccionarUser(id)
