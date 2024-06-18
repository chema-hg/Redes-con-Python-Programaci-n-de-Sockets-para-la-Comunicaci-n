import socket

def udp_client(server_host, server_port, file_path, buffer_size):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    with open(file_path, 'rb') as f:
        while (chunk := f.read(buffer_size)):
            # := operador walrus introducido a partir de python 3.8
            # asigna y devuelve el contendido de la variable.
            client_socket.sendto(chunk, (server_host, server_port))
    
    client_socket.sendto(b"END", (server_host, server_port))
    print(f"Imagen enviada a {server_host}:{server_port}")

    client_socket.close()

# Parámetros del cliente
server_host = '127.0.0.1'
server_port = 12345
file_path = 'gatin.jpg'
buffer_size = 1024

udp_client(server_host, server_port, file_path, buffer_size)
