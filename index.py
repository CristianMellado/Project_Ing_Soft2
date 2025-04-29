from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os

db = {
    "users": {
        "admi": {"pswd": "123", "auth": 1},
        "alex": {"pswd": "ok", "auth": 0}
    }
}

content = [{"id":1,
        "type":"video",
        "src": "static/video/1.mp4",
        "title": "lol gameplay warwick",
        "author": "Autor del video",
        "price": "$10",
        "extension": "mp4",
        "category": "Categoría del video",
        "rating": "4.5",
        "description": "Descripción del video"
    },
    {
        "id":2,
        "type":"audio",
        "src": "static/audio/1.mp3",
        "title": "Married life",
        "author": "Autor del video",
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
        "author": "Autor del video",
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
        "author": "Autor de la imagen   ",
        "price": "$10",
        "extension": "jpg",
        "category": "Categoría de la imagen",
        "rating": "4.5",
        "description": "Descripción de  la imagen"
    }
]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

paths_ulr = ["/login.html","/register.html", "/user_view.html", 
             "/admi_view.html","/addContent.html","/item_view.html"]


class C_Content:
    def get_id(self):
        return 1
    def registrarContent(self, data):
        content[data["type"]].append(data["content"])

    def consultarDatos(self, query, filters):
        query = query.lower().strip()
        resultados = []

        for item in content:
            if len(filters)==0 or item["type"] in filters:
                titulo = item.get('title', '').lower()
                author = item.get('author', '').lower()
                if query in titulo or query in author:
                    resultados.append({
                        'title': titulo,
                        'author': author,
                        'id': item["id"]
                    })
                    
        return resultados
    def getContent(self, content_id):
        return next((item for item in content if item["id"] == content_id), None)

class Usuario:
    def __init__(self):
        self.id = None
        self.user = None
        self.saldo = None
    def loggin(self):
        self.id, self.user,self.saldo = 1,2,3
        
class C_Cliente(Usuario):
    def __init__(self):
        super().__init__()
        self.estado_cuenta = None
    def Buscar(self, query,filters):
        content_manager = C_Content()
        return content_manager.consultarDatos(query,filters)
    def seleccionar(self, content_id):
        content_manager = C_Content()
        return content_manager.getContent(content_id)

class C_Administrador(Usuario):
    def __init__(self):
        super().__init__()
    
    def agregar_contenido(self, datos):
        content_manager = C_Content()
        content_manager.registrarContent(datos)

administrador_manager = C_Administrador()
cliente_manager = C_Cliente()

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header("Content-type", content_type)
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
                ".html": "text/html",
                ".js": "application/javascript",
                ".css": "text/css",
                ".jpg": "image/jpeg",
                ".png": "image/png",
                ".mp4": "video/mp4",
                ".mp3": "audio/mpeg"
            }
            content_type = mime_types.get(ext, "application/octet-stream")
            self.serve_file(file_path, content_type)
        
        elif parsed_path.path == "/main_view_content":
            self._set_headers()
            self.wfile.write(json.dumps(content).encode("utf-8"))
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

        if parsed_path.path == "/signin":
            name = data.get("name")
            password = data.get("password")

            if isinstance(name, list): name = name[0]
            if isinstance(password, list): password = password[0]

            if name in db["users"] and db["users"][name]["pswd"] == password:
                response = {"success": True, "url": "user_view.html"}
                if db["users"][name]["auth"]:
                    response["url"] = "admi_view.html"
            else:
                response = {"success": False, "message": "Credenciales inválidas"}

            self._set_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif parsed_path.path == "/register":
            name = data.get("name")
            password = data.get("password")

            if isinstance(name, list): name = name[0]
            if isinstance(password, list): password = password[0]

            if name in db["users"]:
                response = {"success": False, "message": "Usuario ya existe"}
            else:
                db["users"][name] = {"pswd": password, "auth": 0}
                response = {"success": True, "message": "Usuario registrado correctamente"}
            print(db)

            self._set_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))
        
        elif parsed_path.path == "/search_content":
            #print(data, data.get("query"))
            datos_encontrados = cliente_manager.Buscar(data.get("query"), data.get("filters"))
            #print(datos_encontrados)
            self._set_headers()
            self.wfile.write(json.dumps(datos_encontrados).encode("utf-8"))

        elif parsed_path.path == "/get_content_by_id":
            content_id = data.get("id")
            try:
                content_id = int(content_id)
            except (ValueError, TypeError):
                self._set_headers()
                self.wfile.write(json.dumps({"error": "ID inválido"}).encode("utf-8"))
                return

            found_item = cliente_manager.seleccionar(content_id)

            self._set_headers()
            if found_item:
                self.wfile.write(json.dumps(found_item).encode("utf-8"))
            else:
                self.wfile.write(json.dumps({"error": "Contenido no encontrado"}).encode("utf-8"))
        
        elif parsed_path.path == "/save_content":
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
                administrador_manager.agregar_contenido({
                    "type": type_data,
                    "content": new_item
                })
                response = {"success": True, "message": "Contenido guardado"}
            else:
                response = {"success": False, "message": "Tipo de contenido inválido"}

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
