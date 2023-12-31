from personaje import Personaje
from typing import List
from utils import LETRAS
from type_player import TypePlayer
class Inteligencia (Personaje):
    def __init__(self, vida_maxima = 2, danio =0, ):
        super().__init__(vida_maxima, danio)
        self.type = TypePlayer.Inteligencia

    def getInfo(self, ):
        return f"{self.type.value} está en {self.posicion} y tiene {self.vida_actual}/ {self.vida_maxima} de vida"
    
    def habilidad(self, posicion, equipo:List[Personaje]) -> [str,bool]:
        self.enfriamiento_restante = 1


         #equipo es una lista de jugadores y cada jugador tiene su posicion
        # revelar en un cuadrado de 2 x 2 alrededor de la posicion siendo la posicion la esquina superior izquierda
        
        lista_posiciones = [] #lista de posiciones que se van a revelar
        # b3 = > [b3, c3, b4, c4]
        # a1 = > [a1, b1, a2, b2]
        n = 2
        for j in range(int(posicion[1]), int(posicion[1]) + n):
            for k in range (LETRAS[posicion[0].upper()], LETRAS[posicion[0].upper()] + n):
                # get jey with k value
                for key, value in LETRAS.items():
                    if value == k:
                        k = key
                lista_posiciones.append(k + str(j))
        salida = ""
        for personaje in equipo:
            if personaje.posicion in lista_posiciones:
                salida += f"{personaje.type.value}  ha sido avistado en {personaje.posicion}\n"
        return len(salida) > 0 and [salida, True] or ["Ningún personaje ha sido revelado", False]
    
    
    def getInfoHabilidad(self, ):
        return f"Revelar a los enemigos en un área 2x2. ({self.type.value})"
