import socket
import pickle
from time import sleep
import pygame

# Parámetros del servidor
host = '127.0.0.1'
port = 12345
buffer_size = 2048
output_file = 'gatin_out.jpg'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))

print(f"Servidor UDP escuchando en {host}:{port}")

pygame.init()
screen = None
running = True

while True:
    data, addr = server_socket.recvfrom(buffer_size)
    mensaje = pickle.loads(data)
    if mensaje == "END":
        print("Transferencia completa.")
        break
    # print(f"Recibiendo datos de {addr} --> {mensaje}")
    if not screen:
            # Recibir las dimensiones de la imagen
            width, height = mensaje
            print(f"Las dimensiones de la imagen son {width},{height}")
            screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption("Imagen recibida")
    else:
            # Recibir los píxeles Pej. ((639, 423), (35, 35, 37))
            index = mensaje[0]
            pixel = mensaje[1]
            x = index[0]
            y = index[1]
            screen.set_at((x, y), pixel)
            pygame.display.flip()
    
server_socket.close()
pygame.quit()

print("Conexión finalizada.")