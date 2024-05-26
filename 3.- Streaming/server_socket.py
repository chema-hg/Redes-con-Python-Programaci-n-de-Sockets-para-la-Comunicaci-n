import socket

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 8081 # Port to listen on (non-privileged ports are > 1023)

def enviar_texto(client_socket, texto):
    texto = texto + "\n"
    data = texto.encode()
    client_socket.send(data)
    
def obtener_texto(client_socket):
    buffer = ""
    socket_abierto = True
    
    while socket_open:
        # Lee cualquier dato desde el socket
        data = client_socket.recv(1024)
        # Si no se reciben más datos el socket debe cerrarse.
        if not data:
            socket_abierto = False
        # Añadir datos al buffer.
        buffer = buffer + data.decode()
        # Si hay un caracter de fin de mensaje en el buffer
        posicion_caracter_fin = buffer.find("\n")
        # Si el valor es más grande que -1, un /n debe existir.
        while posicion_caracter_fin > -1:
            # obtiene el mensaje del buffer
            mensaje = buffer[:posicion_caracter_fin]
            # eliminamos el mensaje del buffer
            buffer = buffer[posicion_caracter + 1:]
            # yield en el mensaje (lo explicamos luego)
            yield mensaje
            # ¿Hay otro caracter de fin de mensaje el buffer
            posicion_caracter_fin = buffer.find("\n")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Vincula el socket a una dirección y puerto específicos
    s.bind((HOST, PORT))

    # Escucha conexiones entrantes (el argumento especifica el tamaño máximo de la cola de conexiones)
    s.listen()

    print("Servidor escuchando en el puerto 8081...")

    # Aceptar una conexión
    client_socket, client_address = s.accept()
    with client_socket:
        print(f"Conexión aceptada de {client_address}")
        
        mensaje = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis pretium neque velit, et mattis justo lacinia non. Sed ultrices, nisi vitae sagittis porta, tortor enim tincidunt ex, vel faucibus ex nisl non turpis. In hac habitasse platea dictumst. Curabitur volutpat vestibulum elit, non condimentum felis interdum at. Proin vel tristique turpis, non rutrum metus. Nullam quam odio, sollicitudin vel ligula a, molestie imperdiet lorem. Etiam ut ante nisl. Donec mollis pulvinar risus non finibus."
        enviar_texto(client_socket, mensaje)
        
        

