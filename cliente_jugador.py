import socket
from utils import convertToBytes, convertToDict
from phase_game import PhaseGame
from player_score import PlayerScore
class ClienteJugador():
    payerScore=None
    # bandera para saber si estoy recibiendo datos
    recivingData = True
    def __init__(self, connection: socket.socket, client_address) -> None:
        
        self.connection = connection
        self.client_address =client_address
    
    def setPayerScore(self, nombre:PlayerScore):
        self.payerScore = nombre
    
    def getPlayerScore(self)->PlayerScore:
        return self.payerScore

    def datatoSend(self,message,phase:PhaseGame or None):
        message = {
        'message': message,
        'phase': phase
        }
        data = convertToBytes(message)

        if self.connection.fileno() != -1:


            self.connection.sendto(data, self.client_address)

    def recivirData(self, converToInt = False):
        
        try:
            data = self.connection.recv(1024, )
            dataConvert = convertToDict(data)
            if converToInt:
                return int(dataConvert)
            self.recivingData = False
            return dataConvert
        except:
            # mandar una excepcion personalizada
            Exception("estoy recibiendo y mandando")
       