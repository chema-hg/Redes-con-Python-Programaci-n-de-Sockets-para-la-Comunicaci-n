import socket
from time import time, ctime
from platform import node
import pickle
from sys import version

fecha_actual_unix = time()

fecha_actual = ctime(fecha_actual_unix)
nombre_red = node()
version_python = version

print("fecha_actual:", fecha_actual)
print ('Descripción:', node()) 
print(version_python)

# mensaje = fecha_actual + "\n" + nombre_red + "\n" + version_python
# data = mensaje.encode()
mensaje = (fecha_actual, nombre_red, version_python)
# pickle.dumps((mensaje) convierte el mesaje en bytes sea cual sea el tipo de datos.
data = pickle.dumps(mensaje)

HOST = "127.0.0.1"  # El nombre del servidor o IP del mismo
PORT = 8081  # El puerto usado por el servidor

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    client_socket.sendall(data)