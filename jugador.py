from medico import Medico
from inteligencia import Inteligencia
from francotirador import Francotirador
from artillero import Artillero
from personaje import Personaje
from typing import List
from utils import validar_celda, comprobar_celda_disponible
class Jugador:
    max_col = 4
    max_row = 4
    oponente = None
    # equipo es una lista de personajes
    equipo= []
    informe = ""
    nombre = ""
    posiscionados = False
    def __init__(self, nombre):
        self.nombre = nombre
        self.crear_equipo()
        self.posicionar_equipo()
    
    def filtrar_vida_baja(self, )->List[Personaje]:
        equipo_vida_baja = []
        # filtrar los personajes que tienen vida baja
        for personaje in self.equipo:
            if personaje.vida_actual < personaje.vida_maxima:
                equipo_vida_baja.append(personaje)
        return equipo_vida_baja
            
    def curar(self, ListaPersonajes:List[Personaje]):
        count = 1
        for personaje in ListaPersonajes:
            print(f"{count}. {personaje.type} {personaje.getVidaActual()}")
        option = int(input("seleccione el personaje a curar: "))
        while option < 1 or option > len(ListaPersonajes):
            option = int(input("seleccione el personaje a curar: "))
        personaje = ListaPersonajes[option-1]
        # get personaje medico in equipo
        medico = None
        for personaje in self.equipo:
            if personaje.type == "Medico":
                medico = personaje
        medico.habilidad(personaje)
    
    def disparar_en_area(self, ):
        coordenada = input("Indica las coordenadas de la esquina superior izquierda en la que disparar (área 2x2): ")
        while not validar_celda(coordenada, self.max_col, self.max_row):
            print ("coordenada no válida")
            coordenada = input("Indica las coordenadas de la esquina superior izquierda en la que disparar (área 2x2): ")
        # find artillero in equipo
        artillero = None
        for personaje in self.equipo:
            if personaje.type == "Artillero":
                artillero = personaje
        return artillero.habilidad(coordenada, self.oponente.equipo)

    def revelar_enemigos(self, ):
        coordenada = input("Indica las coordenadas de la esquina superior izquierda en la que revelar (área 2x2): ")
        while not validar_celda(coordenada, self.max_col, self.max_row):
            print ("coordenada no válida")
            coordenada = input("Indica las coordenadas de la esquina superior izquierda en la que revelar (área 2x2): ")
        # find inteligencia in equipo
        inteligencia = None
        for personaje in self.equipo:
            if personaje.type == "Inteligencia":
                inteligencia = personaje
        return inteligencia.habilidad(coordenada, self.oponente.equipo)
    
    def matar_enemigo(self, ):
        coordenada = input("Indica las coordenadas de la celda a la que disparar: ")
        while not validar_celda(coordenada, self.max_col, self.max_row):
            print ("coordenada no válida")
            coordenada = input("Indica las coordenadas de la celda a la que disparar: ")
        # find francotirador in equipo
        francotirador = None
        for personaje in self.equipo:
            if personaje.type == "Francotirador":
                francotirador = personaje
        return francotirador.habilidad(coordenada, self.oponente.equipo)



        
    

    def menu(self, equipo:List[Personaje])->dict:
        menu={}
        counter = 1
        for personaje in equipo:
            menu[counter] ={ "texto":f"Mover {personaje.type}", "accion":personaje.mover}
            counter += 1
            if not personaje.estoy_en_enfriamiento():
                accion = None
                if personaje.type == "Medico" and len(self.filtrar_vida_baja()) > 0:
                    accion = self.curar
                elif personaje.type == "Artillero":
                    accion = self.disparar_en_area
                elif personaje.type == "Inteligencia":
                    accion = self.revelar_enemigos
                elif personaje.type == "Francotirador":
                    accion = self.matar_enemigo

                menu[counter] = {
                    "texto":personaje.getInfoHabilidad(),
                    "accion": accion
                    }
                counter += 1
        return menu
            

    def turno(self, equipo:List[Personaje] )->bool:
        if self.informe != "":
            print(self.informe)
        print(self.getSituacion())
        # counter = 1
        # for personaje in equipo:
        menu = self.menu(equipo)

        for key, value in menu.items():
            print(f"{key}. {value['texto']}")
        
        opt = int(input("Seleccione una opción: "))
        # validate opt if is in menu
        while opt not in menu.keys():
            print("opción no válida")
            opt = int(input("Seleccione una opción: "))
        
        # execute action
        menu[opt]["accion"]()
        


            

        return False
            

            

    def getSituacion(self, ):
        informe = ""
        for personaje in self.equipo:
            informe += personaje.getInfo() + "\n"
        # return self.informe
        return informe

    def set_oponente(self, oponente):
        self.oponente = oponente

    def crear_equipo(self, ):
        medico = Medico()
        inteligencia = Inteligencia()
        francotirador = Francotirador()
        artillero = Artillero()
        self.equipo = [medico, inteligencia, francotirador, artillero]
        

    def posicionar_equipo(self, ):
        
        for personaje in self.equipo:
            pos = input(f"Posiciona a tu {personaje.type} en el tablero: ")
            while not validar_celda(pos, self.max_col, self.max_row) or not comprobar_celda_disponible( pos, self.equipo):
                print("ups, esa celda no es válida o ya está ocupada")
                pos = input(f"Posiciona a tu {personaje.type} en el tablero: ")
            personaje.posicion = pos

        return True


    def realizar_accion(self, )-> str:
        pass

    def recibir_accion(self, )->None | dict:
        pass
