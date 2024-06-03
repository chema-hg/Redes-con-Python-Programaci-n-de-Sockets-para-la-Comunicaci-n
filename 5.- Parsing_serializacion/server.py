import socket
import pickle

HOST = '127.0.0.1' # Standard loopback interface address (localhost)
PORT = 8081 # Port to listen on (non-privileged ports are > 1023)

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
        
        mensaje = "Hola,¡Gracias por conectarte!"
        data = client_socket.recv(1024)
#         mensaje = data.decode()
        mensaje = pickle.loads(data)
        # hace lo contrario, convierte bytes a sus originales.
        print(mensaje)