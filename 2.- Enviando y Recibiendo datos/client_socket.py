import socket

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 8081  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    data = client_socket.recv(1024)
    mensaje = data.decode()
    print(mensaje)
    
    
    

