import socketserver
from collections import namedtuple
from random import choice
from threading import Event
import pickle

'''
Comandos:
COLOCA TUS COMANDOS AQUÍ
QUES - comando de pregunta
UNIR - solicitud de unirse al principio
1 - Se utiliza para enviar una pregunta al cliente después de una solicitud
2 - Se utiliza para enviar "Espera el evento listo para empezar" al cliente.
4 - Se utiliza para enviar una respuesta al servidor después de una pregunta
7 - Se utiliza para enviar una respuesta "Correcta" o "Incorrecta" después de una respuesta
'''

NUMERO_DE_JUGADORES = 2
jugadores = []
listo_para_empezar = Event()
contestadas = 0
esperando_respuestas = Event()
pregunta_Actual = None
Pregunta = namedtuple('Pregunta', ['p', 'respuesta'])
# Pregunta = namedtuple('Pregunta', 'p respuesta')
juego_Preguntas = [
    Pregunta("¿Como se llama un polígono de tres lados?", "Triángulo"),
    Pregunta("¿Cuál es el quinto planeta del sistema solar?", "Jupiter"),
    Pregunta("¿Cuál es la capital de Francia?", "Paris"),
    Pregunta("¿Quién dijo la frase: 'Solo se que no se nada'?", "Socrates"),
    Pregunta("¿Cuál es el antónimo de rico?", "Pobre")
]

# Creamos el servidor multihilo
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class QuizGame(socketserver.BaseRequestHandler):
    def handle(self):
        global jugadores
        global contestadas
        global pregunta_Actual

        while True:
            try:
                data = self.request.recv(1024)
                if not data:
                    break
                request = pickle.loads(data)
            except EOFError:
                break
            
            if request[0] == "JOIN":
                nombre_equipo = request[1]
                jugadores.append(nombre_equipo)
                print(f'El Equipo {nombre_equipo} está conectado.')
                if len(jugadores) == NUMERO_DE_JUGADORES:
                    listo_para_empezar.set()
                
                if listo_para_empezar.is_set() == False:
                    mensaje = "[Server]...esperando que los otros jugadores se unan"
                else:
                    mensaje = "[Server]...empezando"
                self.enviar_mensaje([2, mensaje])
                listo_para_empezar.wait()
                
            if request[0] == "QUES":
                if pregunta_Actual == None:
                    pregunta_Actual = choice(juego_Preguntas)
                    esperando_respuestas.clear()
                self.enviar_mensaje((1, pregunta_Actual.p))
                
            if request[0] == "4":
                if request[1] == pregunta_Actual.respuesta:
                    self.enviar_mensaje((7, "Correcto"))
                else:
                    self.enviar_mensaje((7, "Incorrecto"))
                contestadas += 1
                
                if contestadas == len(jugadores):
                    contestadas = 0
                    pregunta_Actual = None
                    esperando_respuestas.set()
                
                esperando_respuestas.wait()

    def enviar_mensaje(self, mensaje):
        self.request.sendall(pickle.dumps(mensaje))

if __name__ == "__main__":
    HOST, PORT = "localhost", 2065
    with ThreadedTCPServer((HOST, PORT), QuizGame) as server:
        print(f"Servidor ejecutándose en {HOST}:{PORT}")
        server.serve_forever()
