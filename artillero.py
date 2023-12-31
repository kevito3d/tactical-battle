from personaje import Personaje
from typing import List
from utils import LETRAS
from type_player import TypePlayer
class Artillero (Personaje):
    def __init__(self, vida_maxima = 2, danio =1, ):
        super().__init__(vida_maxima, danio)
        self.type = TypePlayer.Artillero

    def getInfo(self, ):
        return f"{self.type.value} está en {self.posicion} y tiene {self.vida_actual}/ {self.vida_maxima} de vida"
    
    def habilidad(self, posicion, equipo:List[Personaje])-> [str,bool]:
        #equipo es una lista de jugadores y cada jugador tiene su posicion
        # revelar en un cuadrado de 2 x 2 alrededor de la posicion siendo la posicion la esquina superior izquierda
        self.enfriamiento_restante = 1
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
                personaje.recibir_danio(self.danio)
                
                salida += f"{personaje.type.value} ha sido herido en la posicion {personaje.posicion} [Vida Restante {personaje.getVidaActual()}] \n"
        # if personaje.vida_actual == 0:
                #     # remove this player from equipo
                #     equipo.remove(personaje)
        for personaje in equipo:
            if personaje.vida_actual == 0:
                equipo.remove(personaje)
        return len(salida) > 0 and [salida, True] or ["Ningún personaje ha sido herido", False]

    def getInfoHabilidad(self, ):
        return f"Disparar en área (2x2). Daño {self.danio}. ({self.type.value})"
   