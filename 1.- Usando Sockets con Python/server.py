import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincula el socket a una dirección y puerto específicos
server_socket.bind(('0.0.0.0', 8081))

# Escucha conexiones entrantes (el argumento especifica el tamaño máximo de la cola de conexiones)
server_socket.listen(5)

print("Servidor escuchando en el puerto 8081...")

# Aceptar una conexión
client_socket, client_address = server_socket.accept()
print(f"Conexión aceptada de {client_address}")
