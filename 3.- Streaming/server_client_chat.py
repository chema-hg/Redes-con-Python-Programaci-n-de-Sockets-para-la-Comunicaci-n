import socket

TCP_IP = "0.0.0.0"  # IP address to bind to
TCP_PORT = 8081  # Port to bind to or connect to
BUFFER_SIZE = 1024  # Buffer size for receiving data
END_MESSAGE = "%end%"  # Special message to indicate end of communication

def enviar_texto(sending_socket, texto):
    """Envía texto a través de un socket, añadiendo una nueva línea al final."""
    texto += "\n"
    data = texto.encode()
    sending_socket.send(data)

def obtener_texto(receiving_socket):
    """Generador que recibe texto desde un socket y devuelve mensajes completos."""
    buffer = ""
    while True:
        data = receiving_socket.recv(BUFFER_SIZE)
        if not data:
            break
        buffer += data.decode()
        while "\n" in buffer:
            mensaje, buffer = buffer.split("\n", 1)
            yield mensaje

def iniciar_servidor():
    """Inicializa el servidor y maneja las conexiones entrantes."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor_socket:
        servidor_socket.bind((TCP_IP, TCP_PORT))
        servidor_socket.listen()
        print(f"Servidor vinculado a {TCP_IP}:{TCP_PORT}\nEsperando conexión...")

        conexion, client_address = servidor_socket.accept()
        with conexion:
            print(f"Cliente conectado desde {client_address[0]}:{client_address[1]}")
            enviar_texto(conexion, "¡Bienvenido al servidor! Teclea %end% para finalizar...")
            manejar_comunicacion(conexion)

def conectar_cliente():
    """Conecta al cliente a un servidor especificado."""
    serverIP = input("Introduce la dirección IP (e.g. 127.0.0.1) o deja en blanco para LOCALHOST: ") or "127.0.0.1"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexion:
        conexion.connect((serverIP, TCP_PORT))
        print(f"Conectado al servidor {serverIP}:{TCP_PORT}")
        manejar_comunicacion(conexion)

def manejar_comunicacion(conexion):
    """Maneja la comunicación bidireccional entre cliente y servidor."""
    try:
        for mensaje in obtener_texto(conexion):
            print(">> ", mensaje)
            if mensaje == END_MESSAGE:
                break
            nuevo_mensaje = input("Escribe un mensaje > ")
            enviar_texto(conexion, nuevo_mensaje)
    except Exception as e:
        print(f"Error en la comunicación: {e}")
    finally:
        print("Conexión cerrada.")

def main():
    """Función principal que selecciona modo de operación: servidor o cliente."""
    while True:
        ser_cli = input("Elige: iniciar un servidor (1) o conectarte a uno - cliente (2) > ")
        if ser_cli in ('1', '2'):
            break

    if ser_cli == '1':
        iniciar_servidor()
    else:
        conectar_cliente()

    print("¡Programa terminado! Sockets cerrados.")

if __name__ == "__main__":
    main()
