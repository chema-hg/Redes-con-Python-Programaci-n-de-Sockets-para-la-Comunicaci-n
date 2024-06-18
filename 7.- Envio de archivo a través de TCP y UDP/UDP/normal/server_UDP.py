import socket

def udp_server(host, port, buffer_size, output_file):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    
    print(f"Servidor UDP escuchando en {host}:{port}")
    
    with open(output_file, 'wb') as f:
        while True:
            data, addr = server_socket.recvfrom(buffer_size)
            if data == b"END":
                print("Transferencia completa.")
                break
            f.write(data)
            print(f"Recibiendo datos de {addr}")

    server_socket.close()

# Parámetros del servidor
host = '127.0.0.1'
port = 12345
buffer_size = 1024
output_file = 'gatin_out.jpg'

udp_server(host, port, buffer_size, output_file)
