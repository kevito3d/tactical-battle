import socket
from utils import convertToBytes, convertToDict
from phase_game import PhaseGame
class ClienteJugador():
    nombre=""
    def __init__(self, connection: socket.socket, client_address) -> None:
        
        self.connection = connection
        self.client_address =client_address
    
    def setNombre(self, nombre):
        self.nombre = nombre

    def datatoSend(self,message,phase:PhaseGame or None):
         message = {
            'message': message,
            'phase': phase
            }
         data = convertToBytes(message)
         self.connection.sendto(data, self.client_address)

    def recivirData(self, converToInt = False):
        try:
            data = self.connection.recv(1024)
            dataConvert = convertToDict(data)
            if converToInt:
                return int(dataConvert)
            return dataConvert
        except socket.error as e:
            print(e)
            return None