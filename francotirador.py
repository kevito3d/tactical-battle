from personaje import Personaje
from typing import List
from type_player import TypePlayer

class Francotirador (Personaje):
    def __init__(self, vida_maxima = 3, danio =3, ):
        super().__init__(vida_maxima, danio)
        self.type = TypePlayer.Franco

    def getInfo(self, ):
        return f"{self.type.value} está en {self.posicion} y tiene {self.vida_actual}/ {self.vida_maxima} de vida"
    
    def habilidad(self, posicion:str, equipo:List[Personaje])-> [str,bool]:
        self.enfriamiento_restante = 1
        salida = ""
        for personaje in equipo:
            if personaje.posicion == posicion.upper():
                personaje.recibir_danio(self.danio)
                if personaje.vida_actual == 0:
                    # remove this player from equipo
                    equipo.remove(personaje)
                salida += f"{personaje.type.value} ha sido eliminado\n"
        return len(salida) > 0 and [salida, True] or ["Ningún personaje ha sido herido" , False]

    def getInfoHabilidad(self, ):
        return f"Disparar a una celda. Daño {self.danio}. ({self.type.value})"