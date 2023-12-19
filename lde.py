from player_score import PlayerScore
class Nodo:
    siguiente=None
    anterior=None
   
    
    def __init__(self, playerScore) -> None:
        self.playerScore=playerScore

    def getSiguiente(self):
        return self.siguiente
    
    def setSiguiente(self, sig):
        self.siguiente = sig

    def getAnterior(self):
        return self.anterior
    
    def setAnterior(self, ant):
        self.anterior=ant

    def getPlayer(self):
        return self.playerScore
    
class LDE:
    cabecera=None
    final=None
    
    def enlistar(self, playerScore:PlayerScore):
        nuevo=Nodo(playerScore)
        if self.cabecera==None:
            self.cabecera=nuevo
            self.final=nuevo
            return
        # si esta por encima de la cabecera
        if playerScore.getScore()>=self.cabecera.getPlayer().getScore():
            nuevo.setSiguiente(self.cabecera)
            self.cabecera.setAnterior(nuevo)
            self.cabecera=nuevo
            return
        # si esta por atras del final
        if playerScore.getScore()<self.final.getPlayer().getScore():
            nuevo.setAnterior(self.final)
            self.final.setSiguiente(nuevo)
            self.final=nuevo
            return
        # si el dato toca meterlo por enmedio
        aux=self.cabecera
        while aux.getPlayer().getScore()>playerScore.getScore():
            aux=aux.getSiguiente()
        # en este punto el aux se encontrara en una posicion adelante del dato que quiero meter
        aux.getAnterior().setSiguiente(nuevo)
        nuevo.setAnterior(aux.getAnterior())
        nuevo.setSiguiente(aux)
        aux.setAnterior(nuevo)

    def imprimir(self):
        aux=self.cabecera
        while aux!=None:
            print(aux.getPlayer())
            aux=aux.getSiguiente()
