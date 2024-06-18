import socket

def start_server(host='0.0.0.0', port=12345):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Servidor escuchando en {host}:{port}")
    
    client_socket, addr = server_socket.accept()
    print(f"Conexión establecida con {addr}")
    
    with open('gatin_out.png', 'wb') as f:
        while True:
            data = client_socket.recv(1024)
            if data == b'END':
                break
            f.write(data)
    
    print("Imagen recibida y guardada como 'gatin_out.png'")
    client_socket.close()
    server_socket.close()
    print("Servidor cerrado")

if __name__ == '__main__':
    start_server()
