from cliente_jugador import ClienteJugador
class Nodo:
    siguiente=None
    jugador=None

    def __init__(self, jugador) -> None:
        self.jugador= jugador

    def getSiguiente(self):
        return self.siguiente
    
    def setSiguiente(self, sig):
        self.siguiente = sig

    def getJugador(self):
        return self.jugador
         

class Cola:
    cabecera=None
    final=None
    tamanio=0

    def encolar(self, jugador):
        nuevo=Nodo(jugador)
        if self.esVacia():
            self.cabecera=nuevo
            self.final=nuevo
        else:
            self.final.setSiguiente(nuevo)
            self.final=nuevo
        self.tamanio+=1
    
    def desencolar(self)-> ClienteJugador or None:
        devolver=self.cabecera
        if self.esVacia():
            return devolver
        # si el tamanio es 1
        if self.tamanio==1:
            self.cabecera=None
            self.final=None
        else:
            self.cabecera=self.cabecera.getSiguiente()
        self.tamanio-=1
        return devolver.getJugador()
    
    def esVacia(self):
        return self.tamanio==0
    
    def peek(self):
        if self.esVacia():
            return None
        return self.cabecera.getJugador()
    def mostrar(self):
        # Uso actual para ir moviéndome entre nodos
        actual = self.cabecera # Empiezo en el primer elemento
        while actual is not None: # Recorro hasta el final
            print(actual.getJugador(), end=" => ")
            actual = actual.getSiguiente() # paso al siguiente
        print()

    def buscar(self, dato):
        # Uso actual para ir moviéndome entre nodos
        actual = self.cabecera # Empiezo en la cima
        while actual is not None: # Recorro hasta el final
            if actual.getJugador() == dato: # Si encuentro, devuelvo True
                return True
            actual = actual.getSiguiente()
        # Si llego al final sin encontrarlo, devuelvo False
        return False

        
        
    


        