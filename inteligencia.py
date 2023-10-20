from personaje import Personaje
from typing import List
from utils import LETRAS
class Inteligencia (Personaje):
    def __init__(self, vida_maxima = 2, danio =0, ):
        super().__init__(vida_maxima, danio)
        self.type = "Inteligencia"

    def getInfo(self, ):
        return f"{self.type} está en {self.posicion} y tiene {self.vida_actual}/ {self.vida_maxima} de vida"
    
    def habilidad(self, posicion, equipo:List[Personaje]):
        #equipo es una lista de jugadores y cada jugador tiene su posicion
        # revelar en un cuadrado de 2 x 2 alrededor de la posicion siendo la posicion la esquina superior izquierda
        
        lista_posiciones = [] #lista de posiciones que se van a revelar
        # b3 = > [b3, c3, b4, c4]
        # a1 = > [a1, b1, a2, b2]
        n = 2
        for j in range(posicion[1]-1, posicion[1] + n):
            for k in range (LETRAS[posicion[0]], LETRAS[posicion[0]]-1 + n):
                lista_posiciones.append(LETRAS[k] + str(j))
        salida = ""
        for personaje in equipo:
            if personaje.posicion in lista_posiciones:
                salida += f"{personaje.type} en la posicion {personaje.posicion} fue revelado\n"
        return salida
    
    
    def getInfoHabilidad(self, ):
        return f"Revelar a los enemigos en un área 2x2. ({self.type})"
