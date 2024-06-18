import socket

def send_image(file_path, host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    with open(file_path, 'rb') as f:
        data = f.read(1024)
        while data:
            client_socket.send(data)
            data = f.read(1024)
    
    # Enviar señal de finalización
    client_socket.send(b'END')
    print("Imagen enviada")
    client_socket.close()

if __name__ == '__main__':
    send_image('gatin.jpg')

