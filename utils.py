# pares

from typing import List
from personaje import Personaje
import json


LETRAS = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "F": 6,
    "G": 7,
    "H": 8,
    "I": 9,
    "J": 10
}


def limpiar_terminal():
    print(chr(27) + "[2J")

def validar_celda(celda:str, max_col, max_row) -> bool:
    # Para comprobar si una celda "B5" está dentro es una posición válida del
    #tablero que comprende entre A1 y (max_col, max_row)
    # si celda no es un srt return false
    if not isinstance(celda, str):
        return False
    if len(celda) != 2:
        return False
    if not celda[0].upper() in LETRAS.keys():
        return False
    if not celda[1].isdigit():
        return False
    if int(celda[1]) > max_row:
        return False
    if LETRAS[celda[0].upper()] > max_col:
        return False
    # print("celda valida")
    return True

def comprobar_celda_disponible(celda, equipo: List[Personaje]) -> bool:
    # Para comprobar si un miembro del equipo ya ocupa una celda dada
    # equipon es una lista de personajes, y cenda es una posicion, donde cada personaje tiene un atributo posicion
    for personaje in equipo:
        if personaje.posicion == celda:
            return False
    return True

def validar_celda_contigua(celda1, celda2) -> bool:
    # Para comprobar si la celda 1 es contigua a la celda 2
    # para saber si son contiguas tiene que estar en vertical o horizontal y la distancia entre ellas tiene que ser 1
    # validar horizontalmente
    horizontal = LETRAS[celda1[0].upper()] - LETRAS[celda2[0].upper()]

    vertical = int(celda1[1]) - int(celda2[1])

    if horizontal == 0 and abs(vertical) == 1:
        return True
    elif vertical == 0 and abs(horizontal) == 1:
        return True
    else:
        return False

def convertToBytes(data):
    return bytes(json.dumps(data), encoding="latin-1")

# serializar un diccionario
def convertToBytes(data):
    return bytes(json.dumps(data), encoding="latin-1")

def convertToDict(data):
    # si no es nada return None
    if not data:
        return None
    return json.loads(data.decode("latin-1"))