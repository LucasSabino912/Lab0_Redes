socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # TCP
socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   # UDP
```

### 2. 🌐 DNS (Domain Name System)
Cuando escribís `www.google.com`, la computadora no sabe a qué dirección IP conectarse. El **DNS es el "directorio telefónico" de internet**: traduce nombres como `www.famaf.unc.edu.ar` a IPs como `200.16.16.70`.

El código implementa su propio cliente DNS (en vez de usar el del sistema operativo), enviando mensajes UDP al servidor **Quad9 (9.9.9.9)** según el protocolo **RFC 1035**.

### 3. 📦 Protocolo HTTP
Es el protocolo que usan los navegadores para pedir páginas web. El cliente envía un **request**:
```
GET http://host/pagina HTTP/1.0\r\n
Host: host\r\n
\r\n
```
Y el servidor responde con un **status + headers + body**:
```
HTTP/1.0 200 OK\r\n
Content-Type: text/html\r\n
\r\n
<html>...</html>




struct.pack(">HH", 1, 1)  # dos enteros de 2 bytes, big-endian
```

### 5. 🏗️ Arquitectura del programa
```
URL ingresada
     │
     ▼
parse_server() / parse_port()   → extrae "www.host.com" y 80
     │
     ▼
dns_resolve()                   → "www.host.com" → "1.2.3.4"
     │
     ├── _dns_build_query()     → arma el mensaje DNS binario
     ├── socket UDP → Quad9     → envía/recibe
     └── _dns_parse_response()  → extrae la IP de la respuesta
     │
     ▼
connect_to_server()             → abre socket TCP a "1.2.3.4:80"
     │
     ▼
send_request()                  → envía "GET /ruta HTTP/1.0..."
     │
     ▼
get_response()                  → lee status, headers y guarda body en archivo






# ── PARSING DE URL ─────────────────────────────────────────────
def parse_server(url):
    # Extrae solo el hostname de una URL completa
    # "http://www.host.com:8080/path" → "www.host.com"

def parse_port(url):
    # Extrae el puerto, o devuelve 80 si no hay uno explícito
    # "http://host:3128/path" → 3128

# ── CLIENTE DNS (bajo nivel, RFC 1035) ─────────────────────────
def _dns_encode_name(hostname):
    # Codifica "www.host.com" al formato binario DNS (QNAME)
    # Cada etiqueta va precedida de su longitud: \x03www\x04host\x03com\x00

def _dns_build_query(hostname, query_id):
    # Construye el mensaje de consulta DNS completo (header + question)
    # query_id es un número aleatorio para identificar la respuesta

def _dns_skip_name(data, pos):
    # Avanza sobre un nombre DNS en la respuesta (puede estar comprimido)

def _dns_parse_one_rr(data, pos):
    # Lee un "Resource Record" de la respuesta DNS
    # Si es tipo A (IPv4), devuelve la IP; si no, devuelve None

def _dns_parse_response(data, query_id):
    # Parsea la respuesta DNS completa y extrae la primera IP tipo A

def dns_resolve(hostname):
    # FUNCIÓN PRINCIPAL DNS: recibe "www.host.com", devuelve "1.2.3.4"
    # Usa todo lo anterior. 'localhost' → '127.0.0.1' directo sin consultar

# ── CONEXIÓN TCP ───────────────────────────────────────────────
def connect_to_server(server_name, port):
    # Resuelve el nombre, abre socket TCP y se conecta
    # Devuelve el socket listo para usar

# ── HTTP ───────────────────────────────────────────────────────
def send_request(connection, url):
    # Envía el GET request HTTP por el socket

def read_line(connection):
    # Lee bytes del socket hasta encontrar '\n'

def check_http_response(header):
    # Verifica que la primera línea sea "HTTP/x.x 200 ..."

def get_response(connection, filename):
    # Lee la respuesta completa: status, headers y guarda el body en archivo

# ── ORQUESTADOR ────────────────────────────────────────────────
def download(url, filename):
    # Une todo: parsea URL → conecta → pide → guarda

def main():
    # Lee argumentos de línea de comandos y llama a download()


Parsing de URL
parse_server(url) — Dada una URL completa, extrae solo el nombre del servidor. Por ejemplo http://www.google.com/index.html → www.google.com. Si la URL tiene puerto (:8080), lo descarta.
parse_port(url) — Extrae el número de puerto de la URL. Si no hay ninguno explícito, devuelve 80 que es el puerto estándar de HTTP.

Construcción del mensaje DNS
_dns_encode_name(hostname) — Convierte un nombre de dominio al formato binario que entiende el protocolo DNS. El protocolo no manda el texto directamente sino que cada parte va precedida de su longitud. Por ejemplo a.b se convierte en \x01a\x01b\x00.
_dns_build_query(hostname, query_id) — Arma el mensaje completo de consulta DNS que se va a enviar por la red. Incluye un encabezado con un ID de identificación y la pregunta "¿cuál es la IP de este hostname?".

Parsing de la respuesta DNS
_dns_skip_name(data, pos) — Cuando llega la respuesta DNS, necesitamos avanzar sobre los nombres para llegar a los datos útiles. Esta función se encarga de saltar un nombre (que puede estar comprimido) y devuelve la posición siguiente.
_dns_parse_one_rr(data, pos) — Lee un registro de la respuesta DNS. Si ese registro es de tipo A (que es el tipo que contiene una IPv4), devuelve la IP. Si es otro tipo, la descarta.
_dns_parse_response(data, query_id) — Procesa la respuesta DNS completa: verifica que el ID coincida, que no haya errores, y extrae la primera IP que encuentre.

Función principal DNS
dns_resolve(hostname) — Es la que usás desde afuera. Recibe un nombre como www.google.com y devuelve una IP como 142.250.80.36. Internamente crea un socket UDP, manda la consulta a Quad9 (9.9.9.9), recibe la respuesta y la parsea. Para localhost devuelve 127.0.0.1 directamente sin consultar nada.

Conexión TCP
connect_to_server(server_name, port) — Primero resuelve el nombre a IP con dns_resolve, luego abre un socket TCP y se conecta al servidor. Devuelve el socket ya conectado y listo para mandar datos.

Comunicación HTTP
send_request(connection, url) — Manda el pedido HTTP por el socket. El pedido tiene la forma GET <url> HTTP/1.0 más el header Host. Es básicamente un texto formateado de una manera específica que el servidor entiende.
read_line(connection) — Lee bytes del socket de a uno hasta encontrar un salto de línea \n. Se usa para leer las líneas de la respuesta HTTP de a una.
check_http_response(header) — Verifica que la primera línea de la respuesta HTTP diga 200, que significa éxito. Si dice 404, 301, 500, etc., devuelve False.
get_response(connection, filename) — Lee la respuesta HTTP completa. Primero verifica el status con check_http_response, luego descarta los headers, y finalmente guarda el cuerpo (el contenido real de la página) en el archivo indicado.

Orquestadores
download(url, filename) — Une todo el flujo: parsea la URL, conecta al servidor, manda el request, recibe la respuesta y la guarda. Maneja los errores posibles.
main() — Lee los argumentos de la línea de comandos (-o archivo y la URL) y llama a download. Es el punto de entrada del programa.



dns_resolve() # Cliente DNS por UDP
connect_to_server() # Conexiòn TCP