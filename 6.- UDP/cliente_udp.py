import socket

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

mensaje = "Primer mensaje a traves de UDP".encode()

udp_client.sendto(mensaje, ("127.0.0.1",20001))

data, server_address = udp_client.recvfrom(1024)

mensaje = data.decode()

print(mensaje, '-> enviado por el servidor', server_address)