import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8081  # The port used by the server

def obtener_texto(client_socket):
    buffer = ""
    socket_abierto = True
    
    while socket_abierto:
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
            buffer = buffer[posicion_caracter_fin + 1:]
            # yield en el mensaje (lo explicamos luego)
            yield mensaje
            # ¿Hay otro caracter de fin de mensaje el buffer
            posicion_caracter_fin = buffer.find("\n")
            
 
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    for mensaje in obtener_texto(client_socket):
        print(mensaje)
    
    
    

