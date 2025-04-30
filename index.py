from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
import uuid
from templates.scripts.app_classes import Usuario,Cliente,Administrador

session_store = {}

def generate_session_id():
    return str(uuid.uuid4())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

paths_ulr = ["/login.html","/register.html", "/user_view.html", 
             "/admi_view.html","/addContent.html","/item_view.html",
             "/user_account.html"]

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
        return Usuario()
    
    def permises_web_current_user(self):
        self.send_response(403)
        self.end_headers()
        self.wfile.write(b"Usuario no autenticado")
        
    def do_GET(self):
        parsed_path = urlparse(self.path)

        current_usuario = self.get_current_user()

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
            self.wfile.write(json.dumps(current_usuario.getContentView()).encode("utf-8"))

        elif parsed_path.path == "/get_balance":
            if current_usuario:
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.getSaldo()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        elif parsed_path.path == "/user_data":
            if current_usuario:
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.getDataUser()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        elif parsed_path.path == "/get_recargas":
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
                    "categorys": "...",
                    "rating": rating,
                    "description": description,
                    "type": type_data
                }

                current_usuario.ingresarAgregarContenido(new_item)
                response = {"success": True, "message": "Contenido guardado"}

            else:
                self.permises_web_current_user()

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