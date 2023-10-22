from personaje import Personaje
from typing import List
from utils import LETRAS
class Francotirador (Personaje):
    def __init__(self, vida_maxima = 3, danio =3, ):
        super().__init__(vida_maxima, danio)
        self.type = "Francotirador"

    def getInfo(self, ):
        return f"{self.type} está en {self.posicion} y tiene {self.vida_actual}/ {self.vida_maxima} de vida"
    
    def habilidad(self, posicion:str, equipo:List[Personaje]):
        self.enfriamiento_restante = 1
        salida = ""
        for personaje in equipo:
            if personaje.posicion == posicion:
                personaje.recibir_danio(self.danio)
                salida += f"{personaje.type} ha sido eliminado\n"
        return salida

    def getInfoHabilidad(self, ):
        return f"Disparar a una celda. Daño {self.danio}. ({self.type})"