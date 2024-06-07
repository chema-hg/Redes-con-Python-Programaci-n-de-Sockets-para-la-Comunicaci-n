import socket
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(("0.0.0.0", 20001))
print("Servidor UDP activo y escuchando...")

data, client_address = udp_server.recvfrom(1024)
udp_server.sendto(data, client_address)