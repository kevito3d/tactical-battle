class Personaje:
    vida_maxima=0
    vida_actual=0
    danio=0
    enfriamiento_restante=0
    posicion=""
    equipo=[]
    type=""
    def __init__(self, vida_maxima, danio, ):
        self.vida_maxima=vida_maxima
        self.vida_actual=vida_maxima
        self.danio=danio

    def setPosicion(self, posicion):
        self.posicion=posicion
    
    def getPosicion(self, ):
        return self.posicion
    
    def getVidaActual(self, ):
        return f"[ {self.vida_actual}/{self.vida_maxima} ]"
    
    def getVidaMaxima(self, ):
        return self.vida_maxima
    
    def resetear_enfriamiento(self, ):
        self.enfriamiento_restante=0
    
    def estoy_en_enfriamiento(self, ):
        return self.enfriamiento_restante > 0

    def tengo_full_vida(self, ):
        return self.vida_actual == self.vida_maxima
    
    
    
    def recibir_danio(self, danio):
        self.vida_actual -= danio
        if self.vida_actual < 0:
            self.vida_actual = 0


    def mover(self, ):
        pass

    def habilidad(self, ):
        pass