from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import json
import os
import cgi
import uuid
from templates.scripts.app_classes import Usuario,Cliente,Administrador,C_Contenidos
import threading
import time

session_store = {}

def generate_session_id():
    """
    Genera un identificador único de sesión.

    Retorna:
        str: UUID generado como cadena.
    """    
    return str(uuid.uuid4())

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

paths_ulr = ["/login.html","/register.html", "/user_view.html", 
             "/admi_view.html","/addContent.html","/item_view.html",
             "/user_account.html", "/user_info.html", "/item_info_edit.html",
             "/item_view_admi.html", "/item_shop.html","/transacciones.html"]

# [RF-0001] parte del loguin, para designar un role.
def autenticar(username, password):
    """
    Autentica al usuario y asigna el rol correspondiente.

    Parámetros:
        username (str): Nombre de usuario.
        password (str): Contraseña del usuario.

    Retorna:
        Usuario: Objeto de tipo Administrador, Cliente o Usuario (por defecto si falla).
    """    
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
    """
    Manejador HTTP personalizado para servir archivos estáticos, autenticar usuarios
    y responder a solicitudes GET del sistema.
    """
    def _set_headers(self, content_type="application/json", extra_headers=None):
        """
        Configura los encabezados HTTP de la respuesta.

        Parámetros:
            content_type (str): Tipo de contenido (por defecto 'application/json').
            extra_headers (dict): Encabezados adicionales opcionales.
        """        
        self.send_response(200)
        self.send_header("Content-type", content_type)
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()

    def serve_file(self, path, content_type="text/html"):
        """
        Sirve un archivo desde el sistema de archivos.

        Parámetros:
            path (str): Ruta del archivo a servir.
            content_type (str): Tipo de contenido (por defecto 'text/html').
        """        
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

    # [RNF-0035] verifica desde los cookies de la pagina el id de la sesión para verificar a los distintos usuarios usando el aplicativo.
    def get_current_user(self):
        """
        Obtiene el usuario actual en base al ID de sesión guardado en las cookies.

        Retorna:
            Usuario: Usuario autenticado o una instancia vacía si no hay sesión válida.
        """        
        cookie = self.headers.get("Cookie")
        if cookie:
            for item in cookie.split(";"):
                if "session_id" in item:
                    session_id = item.split("=")[1].strip()
                    return session_store.get(session_id)
        return Usuario()
    
    # [RNF-0032] Función que retorna al interfaz un mensaje de permisos denegados con 403 y que no se autentico el usuario.
    def permises_web_current_user(self):
        """
        Devuelve una respuesta HTTP 403 indicando que el usuario no está autenticado.
        """        
        self.send_response(403)
        self.end_headers()
        self.wfile.write(b"Usuario no autenticado")
        
    def do_GET(self):
        """
        Maneja las solicitudes HTTP GET, sirve archivos estáticos,
        páginas HTML y rutas de API.
        """        
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

        # [RF-0018] retorna el saldo de cierto cliente.
        elif parsed_path.path == "/get_balance":
            if current_usuario:
                self._set_headers()
                self.wfile.write(json.dumps({"success":True, "saldo":current_usuario.getSaldo()}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0019] solicita la información del cliente actualmente logueado.
        elif parsed_path.path == "/user_data":
            if current_usuario:
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.getDataUser()).encode("utf-8"))
            else:
                self.permises_web_current_user()
        
        # [RF-0013] envia al frontend las solicitudes de saldo pendientes de los clientes.
        elif parsed_path.path == "/get_recargas":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerRecargas()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0021] Solicita las notificaciones del cliente actualmente logueado, tanto de regalos o recargas.
        elif parsed_path.path == "/get_notificaciones":
            if current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerNotificaciones()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0023] retorna el role del inicio de sesion, si es cliente, administrador, o un usuario.
        elif parsed_path.path == "/get_user_role":
            if current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                self.wfile.write(json.dumps({"role":"Cliente"}).encode("utf-8"))
            elif current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps({"role":"Administrador"}).encode("utf-8"))                
            else:
                self._set_headers()
                self.wfile.write(json.dumps({"role":"User"}).encode("utf-8")) 

        # [RF-0020] solicita las compras del cliente actualmente logueado.
        elif parsed_path.path == "/get_user_downloads":
            if current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerDescargasCliente()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0003] api que verifica si es posible cerrar la cuenta de un cliente.
        elif parsed_path.path == "/close_account":
            if current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                self.wfile.write(json.dumps({'success':current_usuario.SolicitarValidarSaldo()}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0034] solicita el cierre de sesión de un cliente o administrador.
        elif parsed_path.path == "/logout_account":
            if current_usuario:
                print(session_store)
                cookie_header = self.headers.get("Cookie")
                session_id = None

                if cookie_header:
                    cookies = dict(cookie.strip().split("=", 1) for cookie in cookie_header.split(";") if "=" in cookie)
                    session_id = cookies.get("session_id")

                if session_id and session_id in session_store:
                    del session_store[session_id]

                # Invalida la cookie enviando una expiración pasada
                expired_cookie = "session_id=deleted; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT"
                self.send_response(302)
                self.send_header("Set-Cookie", expired_cookie)
                self.send_header("Location", "/login.html")
                self.end_headers()
                print(session_store)
            else:
                self.permises_web_current_user()

        # [RF-0157] Ruta que retorna todas las promociones al administrador.
        elif parsed_path.path == "/get_promociones":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerPromociones()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0193] Ruta que retorna todas las categorias al administrador.
        elif parsed_path.path == "/get_categorys":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtener_categorias()).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0197] Solicita y envia el top ranking de clientes con más descargas.
        elif parsed_path.path == "/get_downloads_ranking":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerRankingUsuariosPorDescargas()).encode("utf-8"))
            else:
                self.permises_web_current_user()      

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta GET no encontrada")

    # [RNF-0033] Función que leé en binario la información enviada por el método post con archivos subidos de tipo contenido.
    def recibirContenidoDesdeFrontend(self, id=False):
            """
            Recibe y procesa archivos de contenido enviados desde el frontend vía POST.

            Parámetros:
                id (bool): Si es True, se incluye el ID del contenido (modo edición).

            Retorna:
                tuple: Un diccionario con el estado de la operación y un objeto `new_item` con la información del contenido.
                    En caso de error, el segundo valor es None.
            """            
            form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'},
            )


            fileitem = form['file']
            if fileitem.filename or id:
                binary_data = None
                extension = None
                
                if fileitem.filename:
                    filename = fileitem.filename
                    binary_data = fileitem.file.read()  # Aquí están los bytes del archivo
                    extension = filename.split('.')[-1]

                title = form.getvalue("content-title")
                author = form.getvalue("content-author")
                price = form.getvalue("content-price")
                content_type = form.getvalue("content-type")
                category = form.getvalue("content-category")
                description = form.getvalue("content-description")

                new_item = {
                        "src": binary_data,  # Guarda como BLOB
                        "title": title,
                        "author": author,
                        "price": price,
                        "extension":extension,
                        "category": category,
                        "rating": 0,
                        "description": description,
                        "type": content_type
                    }
                    
                if id:
                    new_item['id'] = form.getvalue("id")
                    
                #current_usuario.ingresarAgregarContenido(new_item)
                return {"success": True, "message": "Contenido guardado"}, new_item
                #print(binary_data)
                #print(new_item)
            else:
                return {"success": False, "message": "No se recibió archivo"}, None

    def do_POST(self):
        """
        Maneja solicitudes HTTP POST. Dependiendo del path, ejecuta funciones de autenticación,
        carga de contenido u otros procesos definidos en el backend.
        """
        parsed_path = urlparse(self.path)
        content_type = self.headers.get('Content-Type', '')

        data = {}
        form = None
        current_usuario = self.get_current_user()

        if not content_type.startswith('multipart/form-data'):
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                data = parse_qs(body)

        # [RF-0001] API para poder validar el iniciar sesión.
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

        # [RF-0014] recibe una cadena de texto para buscarla en los contenidos existentes.
        elif parsed_path.path == "/search_content":
            if current_usuario:
                resultados = current_usuario.Buscar(data.get("query"), data.get("filters"))
                self._set_headers()
                self.wfile.write(json.dumps({'data':resultados, 'auth':isinstance(current_usuario, Administrador)}).encode("utf-8"))
            else:
                self.permises_web_current_user()
        
        # [RF-0015] recibe una cadena de texto para buscarla en los contenidos y usuarios existentes.
        elif parsed_path.path == "/search_info":
            if current_usuario:
                print(data)
                self._set_headers()
                resultados = current_usuario.buscar_info(data)
                print(resultados)
                self.wfile.write(json.dumps(resultados).encode("utf-8"))
            else:
                self.permises_web_current_user()
        
        # [RF-0011] verifica y solicita el saldo a un cliente.
        elif parsed_path.path == "/request_balance":
            if current_usuario:
                response = current_usuario.ingresarMontoSolicitar(data.get("tarjeta"), data.get("cantidad"), data.get("cardType"))
                self._set_headers()
                self.wfile.write(json.dumps(response).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0012] Aprueba la solicitud de saldo de un cliente.
        elif parsed_path.path == "/accept_recarga":
            if current_usuario:
                current_usuario.aprobarSaldoCliente(int(data.get("id_recarga")))
                self._set_headers()
                self.wfile.write(json.dumps({"success":True}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0022] Acepta la notificación y la marca como leida.
        elif parsed_path.path == "/accept_notificacion":
            if current_usuario:
                current_usuario.aceptarNotificacion(int(data.get("id_notificacion")))
                self._set_headers()
                self.wfile.write(json.dumps({"success":True}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0028] Solicita información de cierto contenido al servidor.
        elif parsed_path.path == "/get_content_by_id":
            if current_usuario:
                content_id = int(data.get("id", 0))
                found = current_usuario.seleccionar(content_id)
                self._set_headers()
                self.wfile.write(json.dumps(found or {"error": "Contenido no encontrado"}).encode("utf-8"))
            else:
                self.permises_web_current_user()
        
        #[RF-0006] El cliente o administrador descargan un contenido.
        elif parsed_path.path == "/download_content":
            if current_usuario:
                content_id = int(data.get("id", 0))
                mime_type, bin_data, filename = current_usuario.obtenerContenidoDescarga(content_id)
                if mime_type!=None:
                    self.send_response(200)
                    self.send_header("Content-Type", mime_type)
                    self.send_header("Content-Disposition", f"attachment; filename={filename}")
                    self.send_header("Content-Length", str(len(bin_data)))
                    self.end_headers()
                    self.wfile.write(bin_data)
                else:
                    self.send_error(404, "Contenido no encontrado")
            else:
                self.permises_web_current_user()

        # [RF-0027] solicita informacion como id, saldo, estado cuenta, etc. de un cliente.
        elif parsed_path.path == "/get_user_by_id":
            if current_usuario:
                id = int(data.get("id", 0))
                found = current_usuario.seleccionar_user(id)
                self._set_headers()
                self.wfile.write(json.dumps(found or {"error": "usuario no encontrado"}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0009] El administrador agrega un contenido nuevo.
        elif parsed_path.path == "/save_content":
            if current_usuario and isinstance(current_usuario, Administrador):
                res, content = self.recibirContenidoDesdeFrontend()
                if content:
                    current_usuario.ingresarAgregarContenido(content)
                self._set_headers()
                self.wfile.write(json.dumps(res).encode("utf-8"))
            else:
                self.permises_web_current_user()
        
        # [RF-0010] El administrador edita un contenido existente.
        elif parsed_path.path == "/update_content":
            if current_usuario and isinstance(current_usuario, Administrador):
                res, content = self.recibirContenidoDesdeFrontend(id=True)
                if content:
                    print(content)
                    current_usuario.actualizarContenido(content)
                self._set_headers()
                self.wfile.write(json.dumps(res).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0002] apartado que recibe los datos de un usuario para registrarlo.
        elif parsed_path.path == "/register":
            name = data.get("username")
            password = data.get("password")
            email = data.get("email")

            if isinstance(name, list): name = name[0]
            if isinstance(password, list): password = password[0]
            if isinstance(email, list): email = email[0]

            new_user = Usuario()
            print(name, password, email)
            resultado = new_user.validarRegistro(data)

            if resultado == 0:
                response = {"success": False, "message": "El usuario ya existe."}
            elif resultado == 1:
                response = {"success": True, "message": "Registro exitoso."}
            else:
                response = {"success": False, "message": "Error al registrar usuario."}

            self._set_headers()
            self.wfile.write(json.dumps(response).encode("utf-8"))

        # [RF-0005] verifica si el cliente o administrador pueden descargar un contenido.
        elif parsed_path.path == "/verificate_downloaded_content":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps({'success':True, "hasRated":False}).encode("utf-8"))
            elif current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                canDownload = current_usuario.verificarContenido(data.get("id"))
                self.wfile.write(json.dumps(canDownload).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0029] Utilizada para ver la información del contenido y establecer el botón de pagar.
        elif parsed_path.path == "/pagarContenido":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps({'success':True, 'hasRated':True}).encode("utf-8"))
            elif current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                canDownload = current_usuario.pagarContenido(data.get("id"))
                self.wfile.write(json.dumps({'success':canDownload}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0008] verifica y registra una puntuación para cierto contenido.
        elif parsed_path.path == "/rate_content":
            if current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                #print((data.get("id"), data.get("score")), "ratee")
                hasRated = current_usuario.Enviar_Puntuacion(data.get("id"), data.get("score"))
                self.wfile.write(json.dumps({'success':hasRated}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        #[RF-0007] verifica y envia un regalo a un cliente.
        elif parsed_path.path == "/gift_content":
            if current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                print(data.get("id"), data.get("destinatario"))
                canGift = current_usuario.Enviar_destinatario(data.get("id"), data.get("destinatario"))
                self.wfile.write(json.dumps(canGift).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0004] Extrae el credito de una cuenta de un cliente.
        elif parsed_path.path == "/withdraw_balance":
            if current_usuario and isinstance(current_usuario, Cliente):
                self._set_headers()
                res = {'success':current_usuario.Retirar_Saldo(data.get("tarjeta"), data.get("cardType"))}
                self.wfile.write(json.dumps(res).encode("utf-8"))
            else:
                self.permises_web_current_user()
        
        # [RF-0027] solicita informacion del historial de compras de un cliente.
        elif parsed_path.path == "/get_user_downloads_info":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerDescargasCliente(data.get("id"))).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0027] solicita informacion del historial de compras de un cliente.
        elif parsed_path.path == "/get_user_downloads_info_time":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerDescargasClienteTime(data.get("id"))).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0027] solicita informacion del historial de recargas de un cliente.
        elif parsed_path.path == "/get_user_refills_info":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.obtenerRecargasCliente(data.get("id"))).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0150] Función que controla el estado del botón eliminar o restaurar contenido.      
        elif parsed_path.path == "/update_content_state":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.actualizarEstadoContenido(data.get("id"))).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0167] Función que asigna cierta promoción a un contenido.     
        elif parsed_path.path == "/asignar_promocion":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                a, b = data.get("id_contenido"), data.get("id_promocion")
                self.wfile.write(json.dumps({'success':current_usuario.asignarPromocion(a,b)}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0172] Función que envia y guarda los datos de una nueva categoria. 
        elif parsed_path.path == "/crear_promocion":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps({'success':current_usuario.agregarPromocion(data)}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0194] Ruta que asignar una categoria a un contenido, solo permitida por el administrador.
        elif parsed_path.path == "/asignar_category":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                a, b = data.get("id_contenido"), data.get("id_categoria")
                self.wfile.write(json.dumps({'success':current_usuario.asignarCategoria(a,b)}).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0195] Ruta que crea una nueva categoria, solo permitida por el administrador.
        elif parsed_path.path == "/crear_category":
            if current_usuario and isinstance(current_usuario, Administrador):
                self._set_headers()
                self.wfile.write(json.dumps(current_usuario.agregarCategoria(data)).encode("utf-8"))
            else:
                self.permises_web_current_user()

        # [RF-0016] retorna los contenidos más descargados
        elif parsed_path.path == "/top_content_downloaded":
            self._set_headers()
            parameter = data.get("parameter")
            self.wfile.write(json.dumps(C_Contenidos.getTopContent(parameter)).encode("utf-8"))   

        # [RF-02012] retorna los contenidos más descargados
        elif parsed_path.path == "/get_transacciones_generales":
            self._set_headers()
            self.wfile.write(json.dumps(current_usuario.getTable(data.get("tipo"))).encode("utf-8"))    

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Ruta POST no encontrada")

# [RF-0196] Función que utiliza un thread para poder correr en segundo plano el control de tiempo de vigencia de las promociones.
def limpieza_periodica():
    while True:
        print("\nControlador de Promociones, actualizando.\n")
        gestor = C_Contenidos()
        gestor.limpiarPromocionesVencidas()
        time.sleep(3600)  # 1 hora
        #time.sleep(86400)  # 24 horas

def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler):
    """
    Inicia un servidor HTTP en el puerto 3000 usando la clase de manejador especificada.

    Parámetros:
        server_class (HTTPServer): Clase del servidor a usar (por defecto, HTTPServer).
        handler_class (BaseHTTPRequestHandler): Clase del manejador de solicitudes (por defecto, SimpleHTTPRequestHandler).

    Comportamiento:
        El servidor se ejecuta de forma indefinida hasta que se interrumpa manualmente.
    """    
    server_address = ('', 3000)
    httpd = server_class(server_address, handler_class)
    print("Servidor corriendo en http://localhost:3000/")
    httpd.serve_forever()

if __name__ == "__main__":
    # Iniciar hilo de limpieza automática
    hilo_limpieza = threading.Thread(target=limpieza_periodica, daemon=True)
    hilo_limpieza.start()

    #Iniciar servidor    
    run()
