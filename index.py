from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
import uuid
import datetime

session_store = {}

def generate_session_id():
    return str(uuid.uuid4())
db = [
    {"pswd": "ok", "auth": 0, "username":"alex","id":2,"saldo":150,"estado":1,"email":"abc@gmail.com"},
    {"pswd": "123", "auth": 1,"username":"admi","id":1, "saldo":-1, "estado":1,"email":"admi@gmail.com"}
]

e_recargas = [{"id_user":2,"id_recarga":1,"cantidad": 500.0, "fecha":"28-04-2025 10:37:05", "estado":1}]

content = [{"id":1,
        "type":"video",
        "src": "static/video/1.mp4",
        "title": "lol gameplay warwick",
        "author": "franciso bejar",
        "price": "$10",
        "extension": "mp4",
        "categorys": "Categoría del video",
        "rating": "4.5",
        "description": "Descripción del video"
    },
    {
        "id":2,
        "type":"audio",
        "src": "static/audio/1.mp3",
        "title": "Married life",
        "author": "francete moriarty",
        "price": "$10",
        "extension": "mp3",
        "category": "Categoría del video",
        "rating": "4.5",
        "description": "Descripción del video"
    }, {
        "id":3,
        "type":"audio",
        "src": "static/audio/2.mp3",
        "title": "Lefestin",
        "author": "charles de jumps",
        "price": "$15",
        "extension": "mp3",
        "category": "Categoría del sonido",
        "rating": "4.8",
        "description": "Descripción del audio"
    },{
        "id":4,
        "type":"imagen",
        "src": "https://github.com/DretcmU/DOWNEZ/blob/main/templates/static/image/Dedos%20dibujados.jpg?raw=true",
        "title": "Dedos dibujados",
        "author": "Konam bursts",
        "price": "$10",
        "extension": "jpg",
        "category": "Categoría de la imagen",
        "rating": "4.5",
        "description": "Descripción de  la imagen"
    }
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

paths_ulr = ["/login.html","/register.html", "/user_view.html", 
             "/admi_view.html","/addContent.html","/item_view.html",
             "/user_account.html"]

class E_Usuarios:
    def __init__(self):
        pass
    def verificarLogin(self, username, password):
        for item in db:
            user = item["username"]
            if user == username and item["pswd"] == password:
                return item["auth"], item['id']  # 1 = Admin, 0 = Cliente
        return None,None
    
    def obtenerUser(self, id):
        for item in db:
            if item["id"] == id:
                data = {"username":item["username"], "email":item["email"], "saldo":item["saldo"]}
                return data
        return None
    
    def obtenerSaldo(self, id):
        for item in db:
            if item["id"] == id:
                return item["saldo"]
        return None
    
    def actualizarSaldo(self,id, cantidad):
        for item in db:
            if item["id"] == id:
                item["saldo"] += cantidad

class E_Recargas:
    def __init__(self):
        pass
    def __get_id_re__(self):
        return len(e_recargas)+1
    
    def registrarSolicitud(self, monto, user_id):
        e_recargas.append({"id_user":user_id,"id_recarga": self.__get_id_re__(), 
                           "cantidad":monto, "fecha":str(datetime.datetime.now()), "estado":1})

    def obtenerListaPeticiones(self):
        list_peti = [item for item in e_recargas if item["estado"]==1]
        return list_peti
    
    def aprobarRecarga(self, id_recarga):
        for item in e_recargas:
            if item["id_recarga"] == id_recarga:
                print("A")
                item["estado"] = 0
                return item["id_user"], item["cantidad"]
        return None,None
    
class E_Contenidos:
    def __init__(self):
        pass

    def registrarContenido(self, data):
        content.append(data)

    def obtenerContenidos(self):
        return content

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
    
    def getContent(self, content_id):
        return next((item for item in content if item["id"] == content_id), None)
    
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
        self.cotroller = ctr
        
    def iniciar_sesion(self, username, password):
        auth, self.id = self.cotroller.loginVerificar(username,password)
        return auth
    
    def Buscar(self, query,filters):
        print(self.user, self.id)
        return self.cotroller.Buscar(query,filters)
    
    def seleccionar(self, content_id):
        return self.cotroller.seleccionarContent(content_id)
    
    def getDataUser(self):
        return self.cotroller.getDataUser(self.id)
    
    def registrarU(self, data):
        return 1
    
class Cliente(Usuario):
    def __init__(self, username, id):
        super().__init__(user=username,id=id,ctr=C_Cliente())
        self.saldo = None
        self.estado_cuenta = None

    def ingresarMontoSolicitar(self, Ncard, amount, cardType):
        return self.cotroller.enviarSolicitud(Ncard, amount, cardType, self.id)
    
    def getSaldo(self):
        return self.cotroller.obtenerSaldo(self.id)

class Administrador(Usuario):
    def __init__(self, username, id):
        super().__init__(user=username,id=id,ctr=C_Administrador())

    def obtenerRecargas(self):
        return self.cotroller.getRecargas()
    
    def aprobarSaldoCliente(self, id_recarga):
        self.cotroller.aprobarRecarga(id_recarga)
    
    def ingresarAgregarContenido(self, datos):
        self.controller.ingresarAgregarContenido(datos)
    
def autenticar(username, password):
    temp_user = Usuario()
    auth = temp_user.iniciar_sesion(username, password)
    
    if auth == 1:
        user = Administrador(username, temp_user.id)
    elif auth == 0:
        user = Cliente(username, temp_user.id)
    else:
        print("Credenciales incorrectas")
        user = temp_user
    return user

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, content_type="application/json", extra_headers=None):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()

    def serve_file(self, path, content_type="text/html"):
        try:
            with open(path, "rb") as f:
                self.send_response(200)
                self.send_header("Content-type", content_type)
                self.end_headers()
                self.wfile.write(f.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Archivo no encontrado")

    def get_current_user(self):
        cookie = self.headers.get("Cookie")
        if cookie:
            for item in cookie.split(";"):
                if "session_id" in item:
                    session_id = item.split("=")[1].strip()
                    return session_store.get(session_id)
        return None
    
    def permises_web_current_user(self):
        self.send_response(403)
        self.end_headers()
        self.wfile.write(b"Usuario no autenticado")
        
    def do_GET(self):
        parsed_path = urlparse(self.path)

        if parsed_path.path == "/":
            self.serve_file(os.path.join(BASE_DIR, "templates", "main_view.html"))
        elif parsed_path.path in paths_ulr:
            self.serve_file(os.path.join(BASE_DIR, "templates", parsed_path.path[1:]))
        elif parsed_path.path.startswith("/static") or parsed_path.path.startswith("/styles") or parsed_path.path.startswith("/scripts"):
            file_path = os.path.join(BASE_DIR, "templates", parsed_path.path[1:])
            ext = os.path.splitext(file_path)[1]
            mime_types = {
                ".html": "text/html", ".js": "application/javascript", ".css": "text/css",
                ".jpg": "image/jpeg", ".png": "image/png", ".mp4": "video/mp4", ".mp3": "audio/mpeg"
            }
            content_type = mime_types.get(ext, "application/octet-stream")
            self.serve_file(file_path, content_type)

        elif parsed_path.path == "/main_view_content":
            self._set_headers()
            self.wfile.write(json.dumps(content).encode("utf-8"))

        elif parsed_path.path == "/get_balance":
            current_usuario = self.get_current_user()
            if current_usuario:
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.getSaldo()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        elif parsed_path.path == "/user_data":
            current_usuario = self.get_current_user()
            if current_usuario:
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.getDataUser()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        elif parsed_path.path == "/get_recargas":
            current_usuario = self.get_current_user()
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerRecargas()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta GET no encontrada")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            data = parse_qs(body)

        current_usuario = self.get_current_user()

        if parsed_path.path == "/signin":
            name = data.get("name")
            password = data.get("password")
            if isinstance(name, list): name = name[0]
            if isinstance(password, list): password = password[0]

            user = autenticar(name, password)

            if isinstance(user, Cliente) or isinstance(user, Administrador):
                session_id = generate_session_id()
                session_store[session_id] = user
                extra_headers = {"Set-Cookie": f"session_id={session_id}; Path=/"}
                redirect_url = "admi_view.html" if isinstance(user, Administrador) else "user_view.html"
                response = {"success": True, "url": redirect_url}
                self._set_headers(extra_headers=extra_headers)
            else:
                response = {"success": False, "message": "Credenciales inválidas"}
                self._set_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif parsed_path.path == "/search_content":
            if current_usuario:
                resultados = current_usuario.Buscar(data.get("query"), data.get("filters"))
                self._set_headers()
                self.wfile.write(json.dumps(resultados).encode("utf-8"))
            else:
                self.permises_web_current_user()

        elif parsed_path.path == "/request_balance":
            if current_usuario:
                response = current_usuario.ingresarMontoSolicitar(data.get("tarjeta"), data.get("cantidad"), data.get("cardType"))
                self._set_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
            else:
                self.permises_web_current_user()

        elif parsed_path.path == "/accept_recarga":
            if current_usuario:
                current_usuario.aprobarSaldoCliente(int(data.get("id_recarga")))
                self._set_headers()
                self.wfile.write(json.dumps({"success":True}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        elif parsed_path.path == "/get_content_by_id":
            if current_usuario:
                content_id = int(data.get("id", 0))
                found = current_usuario.seleccionar(content_id)
                self._set_headers()
                self.wfile.write(json.dumps(found or {"error": "Contenido no encontrado"}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        elif parsed_path.path == "/save_content":
            if current_usuario:
                type_data = data.get("typeData")
                src = data.get("src")
                title = data.get("title")
                author = data.get("author")
                price = data.get("price")
                extension = data.get("extension")
                category = data.get("category")
                rating = 2.5
                description = data.get("description")

                if isinstance(type_data, list): type_data = type_data[0]
                if isinstance(src, list): src = src[0]
                if isinstance(title, list): title = title[0]
                if isinstance(author, list): author = author[0]
                if isinstance(price, list): price = price[0]
                if isinstance(extension, list): extension = extension[0]
                if isinstance(category, list): category = category[0]
                if isinstance(description, list): description = description[0]

                new_item = {
                    "src": src,
                    "title": title,
                    "author": author,
                    "price": price,
                    "extension": extension,
                    "category": category,
                    "rating": rating,
                    "description": description
                }

                if type_data in content:
                    #content[type_data].append(new_item)
                    current_usuario.ingresarAgregarContenido(new_item)
                    response = {"success": True, "message": "Contenido guardado"}
                else:
                    response = {"success": False, "message": "Tipo de contenido inválido"}

            else:
                self.permises_web_current_user()

            print(content)
            self._set_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta POST no encontrada")


def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    server_address = ('', 3000)
    httpd = server_class(server_address, handler_class)
    print("Servidor corriendo en http://localhost:3000/")
    httpd.serve_forever()

if __name__ == "__main__":
    run()