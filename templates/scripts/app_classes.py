import datetime
import sqlite3

path_bd = 'templates/static/db/downez.db'

class E_Usuarios:
    def __init__(self):
        self.conn = sqlite3.connect(path_bd)
        self.cursor = self.conn.cursor()

    def verificarLogin(self, username, password):
        query = "SELECT auth, id FROM usuarios WHERE username = ? AND pswd = ?"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()
        if result:
            return result[0], result[1]  # tipo (Administrador/Cliente), id_usuario
        return None, None

    def obtenerUser(self, id_usuario):
        query="SELECT username, email, saldo FROM usuarios WHERE id = ?"
        self.cursor.execute(query, (id_usuario,))
        resultado = self.cursor.fetchone()

        if resultado:
            return {
                "username": resultado[0],
                "email": resultado[1],  
                "saldo": resultado[2]
            }
        return None

    def obtenerSaldo(self, id):
        query = "SELECT saldo FROM usuarios WHERE id = ?"
        self.cursor.execute(query, (id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # saldo
        return None

    def actualizarSaldo(self,id, cantidad):
        query = "UPDATE usuarios SET saldo = saldo + ? WHERE id = ?"
        self.cursor.execute(query, (cantidad, id))
        self.conn.commit()


class E_Recargas:
    def __init__(self):
        self.conn = sqlite3.connect(path_bd)
        self.cursor = self.conn.cursor()

    def registrarSolicitud(self, monto, user_id):
        fecha = str(datetime.datetime.now())
        query = "INSERT INTO recargas (id_user, monto, fecha) VALUES (?, ?, ?)"
        self.cursor.execute(query, (user_id, monto, fecha))
        self.conn.commit()

    def obtenerListaPeticiones(self):
        query = """
            SELECT 
                recargas.id_recarga, 
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
        query = "SELECT id_user, monto FROM recargas WHERE id_recarga = ? AND estado = 'pendiente'"
        self.cursor.execute(query, (id_recarga,))
        result = self.cursor.fetchone()
        if result:
            id_user, monto = result
            query_set = "UPDATE recargas SET estado = 'aprobada' WHERE id_recarga = ?"
            self.cursor.execute(query_set, (id_recarga,))
            self.conn.commit()
            return id_user, monto
        return None, None
    

class E_Contenidos:
    def __init__(self):
        self.conn = sqlite3.connect(path_bd)
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
    
    def getContent(self, content_id):
        query = "SELECT * FROM contenidos WHERE id = ?"
        self.cursor.execute(query, (content_id,))
        row = self.cursor.fetchone()
        
        if row:
            keys = [desc[0] for desc in self.cursor.description]
            return dict(zip(keys, row))
        else:
            return None
        

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
    
    def getContentView(self):
        contenidos = E_Contenidos()
        return contenidos.obtenerContenidos()
    
    def getContent(self, content_id):
        contenidos = E_Contenidos()
        return contenidos.getContent(content_id)
    
class C_Usuario:
    def __init__(self):
        self.id = None
    
    def getDataUser(self, id_user):
        usuarios = E_Usuarios()
        return usuarios.obtenerUser(id_user)

    def Buscar(self, query,filters):
        content_manager = C_Content()
        return content_manager.consultarDatos(query,filters)
    
    def seleccionarContent(self, content_id):
        content_manager = C_Content()
        return content_manager.getContent(content_id)
    
    def loginVerificar(self, username, password):
        usuarios = E_Usuarios()
        return usuarios.verificarLogin(username,password)
    
    def getContentView(self):
        content_manager = C_Content()
        return content_manager.getContentView()
    
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

    def ingresarAgregarContenido(self, datos):
        content_manager = C_Content()
        content_manager.registrarContenido(datos)

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
    
class Cliente(Usuario):
    def __init__(self, username, id):
        super().__init__(user=username,id=id,ctr=C_Cliente())
        self.saldo = None
        self.estado_cuenta = None

    def ingresarMontoSolicitar(self, Ncard, amount, cardType):
        return self.controller.enviarSolicitud(Ncard, amount, cardType, self.id)
    
    def getSaldo(self):
        return self.controller.obtenerSaldo(self.id)

class Administrador(Usuario):
    def __init__(self, username, id):
        super().__init__(user=username,id=id,ctr=C_Administrador())

    def obtenerRecargas(self):
        return self.controller.getRecargas()
    
    def aprobarSaldoCliente(self, id_recarga):
        self.controller.aprobarRecarga(id_recarga)
    
    def ingresarAgregarContenido(self, datos):
        self.controller.ingresarAgregarContenido(datos)
