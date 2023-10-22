from personaje import Personaje
class Medico (Personaje):
    def __init__(self, vida_maxima = 1, danio =0, ):
        super().__init__(vida_maxima, danio)
        self.type = "Medico"
    
    def getInfo(self, ):
        return f"{self.type} está en {self.posicion} y tiene {self.vida_actual}/ {self.vida_maxima} de vida"

    def habilidad(self, personaje):
        self.enfriamiento_restante = 1
        personaje.vida_actual += 1
        if personaje.vida_actual > personaje.vida_maxima:
            personaje.vida_actual = personaje.vida_maxima

    def getInfoHabilidad(self, ):
        return f"Curar a un compañero. ({self.type})"