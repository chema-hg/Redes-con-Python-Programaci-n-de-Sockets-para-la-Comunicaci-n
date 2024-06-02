import socket
import pickle

jugando = True

# Crear un socket TCP/IP
servidor_preguntas = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Pedir al usuario que ingrese el nombre del equipo
nombre_equipo = input("¿Cual es el nombre de tu equipo? >>> ")

# Pedir al usuario que ingrese la dirección IP del servidor
serverIP = input("Introduce la dirección IP (e.j. 127.0.0.1) a la que quieres conectarte o presiona ENTER para usar LOCALHOST: ")
if serverIP == "":
    serverIP = "127.0.0.1"

# Conectar con el servidor
print(f"\n¡Bienvenido Equipo {nombre_equipo} al Gran Juego de las Preguntas!")
servidor_preguntas.connect((serverIP, 2065))

# Enviar un comando al servidor para unirse al juego
servidor_preguntas.sendall(pickle.dumps(["JOIN", nombre_equipo]))

while jugando:
    # Recibir datos del servidor
    response_data = servidor_preguntas.recv(1024)
    if not response_data:
        break
    response = pickle.loads(response_data)
    
    # Manejar las respuestas del servidor
    if response[0] == 1: # Respuesta de pregunta
        print(response[1])
        respuesta = input('Respuesta : ')
        servidor_preguntas.sendall(pickle.dumps(["4", respuesta]))
    elif response[0] == 2: # Esperando que todos los jugadores estén listos
        print(response[1])
        servidor_preguntas.sendall(pickle.dumps(["QUES", ""]))
    elif response[0] == 7: # Respuesta de correcto o incorrecto
        print(response[1])
        servidor_preguntas.sendall(pickle.dumps(["QUES", ""]))
    elif response[0] == 3: # Esperando que los otros jugadores respondan
        print("...esperandos las respuestas de los otros jugadores")
        servidor_preguntas.sendall(pickle.dumps(["QUES", ""]))

servidor_preguntas.close()
