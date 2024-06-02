import socketserver
from threading import Event

# Clase que crea el servidor multihilo
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

# CLase que define que pasa cuando se conecte el cliente
class QuizGame(socketserver.BaseRequestHandler): # La clase puede llamarse como se quiera.
    def handle(self): # Se debe conservar el nombre de este metodo que es el que dice que se va a hacer.
        self.request.sendall(b"Hello, world")

if __name__ == "__main__":
    HOST, PORT = "localhost", 2065
    with ThreadedTCPServer((HOST, PORT), QuizGame) as server:
        print(f"Server running on {HOST}:{PORT}")
        server.serve_forever()
