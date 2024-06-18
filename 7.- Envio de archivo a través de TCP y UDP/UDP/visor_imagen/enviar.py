import socket
import pickle
from time import sleep


from PIL import Image #libreria gratuita para editar imagenes en python (Pillow)

image = Image.open("gatin.jpg") # carga una imagen

width, height = image.size # devuelve una tupla con el tamaño de la imagen

print(width, height)

udp_client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #crea una conexion UDP

# Enviamos la dimension de la imagen
dimension = (width, height)
data = pickle.dumps(dimension)
udp_client.sendto(data, ("127.0.0.1", 12345))
sleep(1)

for y in range(height):
    for x in range(width):
        pos = (x, y)
        rgba = image.getpixel(pos) # (red, green, blue, trasparencia) 
        message = (pos, rgba)
        data = pickle.dumps(message)
        udp_client.sendto(data, ("127.0.0.1", 12345))
        sleep(0.005)

mensaje = "END"
data = pickle.dumps(mensaje)
udp_client.sendto(data, ("127.0.0.1", 12345))



        
       
        
        
        