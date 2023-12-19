from medico import Medico
from inteligencia import Inteligencia
from francotirador import Francotirador
from artillero import Artillero
from personaje import Personaje
from typing import List
from utils import validar_celda, comprobar_celda_disponible, validar_celda_contigua
from type_player import TypePlayer
from phase_game import PhaseGame
from cliente_jugador import ClienteJugador

class Jugador:
    max_col = 4
    max_row = 4
    oponente = None
    # equipo es una lista de personajes
    equipo= []
    informe = ""
    posiscionados = False
    phase_game = PhaseGame.JOIN.value
    turns = 0
    def __init__(self, cliente:ClienteJugador):
        self.cliente = cliente
        self.crear_equipo()
        # self.phase_game = PhaseGame.WAIT.value
        # if wait:
        #     self.phase_game = PhaseGame.WAIT.value
        #     self.cliente.datatoSend("Ahora estas en cola, esperando jugador.....", self.phase_game)
        # else:
        #     self.cliente.datatoSend("Partida encontrada, es momento de posicionar a tus personajes", None)
        #     self.posicionar_equipo()
    
    def filtrar_vida_baja(self, )->List[Personaje]:
        equipo_vida_baja = []
        # filtrar los personajes que tienen vida baja
        for personaje in self.equipo:
            if personaje.vida_actual < personaje.vida_maxima and personaje.estoy_vivo():
                equipo_vida_baja.append(personaje)
        return equipo_vida_baja
            
    def curar(self, ListaPersonajes:List[Personaje]):
        count = 0
        for personaje in ListaPersonajes:
            count += 1
            print(f"{count}. {personaje.type.value} {personaje.getVidaActual()}")
        option = -1
        while option < 1 or option > len(ListaPersonajes):
            self.cliente.datatoSend("seleccione el personaje a curar: ",PhaseGame.TURN_ACTION.value)
            option =  self.cliente.recivirData(converToInt=True)
        personajeacURAR = ListaPersonajes[option-1]
        # get personaje medico in equipo
        medico = None
        for personaje in self.equipo:
            if personaje.type.value == "Medico":
                medico = personaje
        medico.habilidad(personajeacURAR)
        return ["Curado", False]
    
    def disparar_en_area(self, ):
        self.cliente.datatoSend("Indica las coordenadas de la esquina superior izquierda en la que disparar (área 2x2): ",PhaseGame.TURN_ACTION.value)
        coordenada =  self.cliente.recivirData()
        while not validar_celda(coordenada, self.max_col, self.max_row):
            self.cliente.datatoSend("coordenada no válida",None)
            self.cliente.datatoSend("Indica las coordenadas de la esquina superior izquierda en la que disparar (área 2x2): ", PhaseGame.TURN_ACTION.value)
            coordenada =  self.cliente.recivirData()
        # find artillero in equipo
        artillero = None
        for personaje in self.equipo:
            if personaje.type.value == "Artillero":
                artillero = personaje
        return artillero.habilidad(coordenada, self.oponente.equipo)

    def revelar_enemigos(self, ):
        self.cliente.datatoSend("Indica las co(ordenadas de la esquina superior izquierda en la que revelar (área 2x2): ",PhaseGame.TURN_ACTION.value)
        coordenada =  self.cliente.recivirData()
        while not validar_celda(coordenada, self.max_col, self.max_row):
            self.cliente.datatoSend("coordenada no válida",None)
            self.cliente.datatoSend("Indica las coordenadas de la esquina superior izquierda en la que revelar (área 2x2): ",PhaseGame.TURN_ACTION.value)
            coordenada = self.cliente.recivirData() 
        # find inteligencia in equipo
        inteligencia = None
        for personaje in self.equipo:
            if personaje.type.value == "Inteligencia":
                inteligencia = personaje
        return inteligencia.habilidad(coordenada, self.oponente.equipo)
    
    def matar_enemigo(self, ):
        self.cliente.datatoSend("Indica las coordenadas de la celda a la que disparar: ",PhaseGame.TURN_ACTION.value)
        coordenada = self.cliente.recivirData()
        while not validar_celda(coordenada, self.max_col, self.max_row):
            self.cliente.datatoSend("coordenada no válida",None)
            self.cliente.datatoSend("Indica las coordenadas de la celda a la que disparar: ",PhaseGame.TURN_ACTION.value)
            coordenada = self.cliente.recivirData()
        # find francotirador in equipo
        francotirador = None
        for personaje in self.equipo:
            if personaje.type.value == TypePlayer.Franco.value:
                francotirador = personaje
        resultado = francotirador.habilidad(coordenada, self.oponente.equipo)
        
        return resultado

    def mover(self, personaje:Personaje):
        self.cliente.datatoSend(f"Indica la nueva posición contigua para {personaje.type.value}: ", PhaseGame.TURN_ACTION.value)
        nueva_posicion = self.cliente.recivirData()
        nueva_posicion = nueva_posicion.upper()
        while not validar_celda(nueva_posicion, self.max_col, self.max_row) or not comprobar_celda_disponible(nueva_posicion, self.equipo) or not validar_celda_contigua( personaje.posicion,nueva_posicion):
            # print("ups, esa celda no es válida o ya está ocupada, o no es contigua")
            self.cliente.datatoSend(f"Indica la nueva posición contigua para {personaje.type.value}: ", PhaseGame.TURN_ACTION.value)
            nueva_posicion = self.cliente.recivirData()
            nueva_posicion = nueva_posicion.upper()
        personaje.mover(nueva_posicion)
        return ["Nada que Reporta",False]

    def disminuir_enfriamiento(self, list_personajes:List[Personaje]):
        for personaje in list_personajes:
            personaje.disminuir_enfriamiento()
        return True

    def menu(self, equipo:List[Personaje])->dict:
        menu={}
        counter = 1
        for personaje in equipo:
            # meter un callback en el menu
            if not personaje.estoy_vivo():
                continue

            personajes = []
            for personajeEquipo in self.equipo:
                if personaje.type.value != personajeEquipo.type.value :
                    personajes.append(personajeEquipo)
            reseteo =self.disminuir_enfriamiento
            menu[counter] ={ "texto":f"Mover {personaje.type.value}", "accion":  self.mover, "parametro":personaje, "reseteo":reseteo, "jugadores_reseteo":self.equipo}
            counter += 1
            if  not personaje.estoy_en_enfriamiento():
                accion = None
                if personaje.type.value == TypePlayer.Medico.value:
                    if len(self.filtrar_vida_baja()) > 0:
                        accion = lambda : self.curar(self.filtrar_vida_baja())
                        # reseteo = 
                        # filtrar todos los personajes menos el medico
                        
                    else:
                        continue

                elif personaje.type.value == TypePlayer.Artillero.value :
                    accion = self.disparar_en_area

                elif personaje.type.value == TypePlayer.Inteligencia.value:
                    accion = self.revelar_enemigos

                elif personaje.type.value == TypePlayer.Franco.value:
                    accion = self.matar_enemigo
                
                menu[counter] = {
                    "texto":personaje.getInfoHabilidad(),
                    "accion": accion,
                    "reseteo":reseteo,
                    "jugadores_reseteo":personajes
                    # curar es true 
                    }
                counter += 1
        return menu
    
    def recibir_accion(self, accion:str)->None:
        self.informe = accion
            

    def turno(self, equipo:List[Personaje] )->bool:
        final = False
        print ("---- INFORME ----")
        if self.informe != "":
            print(self.informe + "\n")
            self.informe = ""
        else:
            print("Nada que reportar \n")
        
        print(self.getSituacion())
        # counter = 1
        # for personaje in equipo:
        menu = self.menu(equipo)
   
        for key, value in menu.items():
            print(f"{key}. {value['texto']}")
        
        opt = None
        
            # return False
        # validate opt if is in menu
        while opt ==None or opt not in menu.keys():
            try: 
                opt = int(input("Seleccione una opción: "))
            except ValueError:
                print("opción no válida")
                # print("escribe bien la opción")
        
        # execute action
        # si la accion tiene parametro
        resultado_accion = ""
        moviendo = False
        if "parametro" in menu[opt].keys(): # cuandio me muevo
            moviendo = True
            resultado_accion= menu[opt]["accion"](menu[opt]["parametro"])
        else:
            resultado_accion =menu[opt]["accion"]()
        
        self.turns += 1
            
        
        # reseteo
        menu[opt]["reseteo"](
            menu[opt]["jugadores_reseteo"]
        )
        if not moviendo:
            print ("\n---- RESULTADO DE LA ACCION ----")
            print(resultado_accion[0], )
        if resultado_accion[1]:
            self.oponente.recibir_accion(resultado_accion[0])
            # find if exist francotirador and artillero in team enemy
            counter = 0
            for personaje in self.oponente.equipo:
                if personaje.type.value == TypePlayer.Franco.value or personaje.type.value == TypePlayer.Artillero.value:
                    counter += 1
            if counter == 0:
                final = True
            

        return final
            
    def getEquipo(self, ) -> List[Personaje]:
        return self.equipo
    
    def calcular_puntaje(self, win:bool)->int:
        score=0
        punts_by_turns=0
        if win:
            score = 1000
            punts_by_turns=max(0,(20-self.turns)) * 20
        else:
           if self.turns > 10:
               punts_by_turns = (self.turns-10) * 20

        punts_by_live = 0
        # 100 puntos por cada jugador vivo
        for personaje in self.equipo:
            if personaje.estoy_vivo():
                punts_by_live += 100
        # 100 puntos por cada jugador enemigo muerto
        punts_by_player_dead = 0
        for personaje in self.oponente.getEquipo():
            if not personaje.estoy_vivo():
                punts_by_player_dead += 100
        
        score += punts_by_turns + punts_by_live + punts_by_player_dead
        return score
        
            
    def getInforme(self, ) -> str:
        return self.informe
    def getSituacion(self, )->str:
        situacion = "---- SITUACION DEL EQUIPO ----\n"
        for personaje in self.equipo:
            if not personaje.estoy_vivo():
                continue
            situacion += personaje.getInfo() + "\n"
        # return self.informe
        return situacion

    def set_oponente(self, oponente):
        self.oponente = oponente
        
    
    def getOPponente(self, ) -> "Jugador":
        return self.oponente

    def crear_equipo(self, ):
        medico = Medico()
        inteligencia = Inteligencia()
        francotirador = Francotirador()
        artillero = Artillero()
        self.equipo = [medico, inteligencia, francotirador, artillero]
        

    def posicionar_equipo(self, ):
        # posisciones = ["b3", "b4", "a3", "a4"]
        # ahora ponerlos en lka primera fila
        # posisciones = ["a1", "b1", "c1", "d1"]
        # counter = 0
        for personaje in self.equipo:
            self.cliente.datatoSend(f"Posiciona a tu {personaje.type.value} en el tablero: ", self.phase_game)
            pos = self.cliente.recivirData()
            while not validar_celda(pos, self.max_col, self.max_row) or not comprobar_celda_disponible( pos.upper(), self.equipo):
                print("")
                self.cliente.datatoSend("ups, esa celda no es válida o ya está ocupada", None)
                self.cliente.datatoSend(f"Posiciona a tu {personaje.type.value} en el tablero: ", self.phase_game)
                pos = self.cliente.recivirData()
            # pos = posisciones[counter]
            # counter += 1
            personaje.posicion = pos.upper()
        

        return True

    
