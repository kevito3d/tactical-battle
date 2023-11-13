import sys
import socket
import threading
from phase_game import PhaseGame
from utils import convertToBytes, convertToDict
from cliente_jugador import ClienteJugador
from jugador import Jugador
from typing import List
import random
from type_player import TypePlayer

def main(loby:List[Jugador]):

    # Crear un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # get ip from command line argument y si no hay argumento, usa localhost
    ip = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    # get port from command line argument y si no hay argumento, usa 1234
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1234

    # Vincula el socket a la dirección y al puerto
    server_address = (ip, port)
    print(f'starting up on {server_address}')
    sock.bind(server_address)

    # Escuchando conexiones entrantes
    sock.listen(1)
    while True:
        # Espera una conexión
        print('waiting for a connection')
        # gamesactives = 0
        connection , client_address = sock.accept()

        loby.append(Jugador(cliente=ClienteJugador(connection, client_address)))
        

        # gamesactives += 1
        
        # Inicia el juego en un nuevo hilo
        # abrir hilo para cada juego
        # si tengo a dos personas en el loby que jueges esas dos en un hijo de ejecucion aparte
        if len(loby) == 1:
            thread = threading.Thread(target=newGame, args=(loby[0], None))
        if len(loby) == 2:
            thread = threading.Thread(target=newGame, args=(loby[1], loby[0]))
            # add to the last element of the list the opponent
            # set opponent

            loby.clear()
        thread.start()

def newGame(jugador: Jugador, oponente: Jugador or None):
    # Inicializamos el juego
    if oponente != None:
        jugador.set_oponente(oponente)
        oponente.set_oponente(jugador)
        jugador.phase_game = PhaseGame.JOIN.value
    
    while jugador.phase_game!=PhaseGame.END.value:

        if jugador.phase_game == PhaseGame.JOIN.value:
            # recibir data del cliente
            data = jugador.cliente.recivirData()
            jugador.cliente.setNombre(data["message"])
            if oponente!=None:
                # pasar a la siguiente fase ambos
                jugador.phase_game = PhaseGame.INIT.value
                oponente.phase_game = PhaseGame.INIT.value
            else:
                jugador.cliente.datatoSend("Esperando a otro jugador", None)
                jugador.phase_game = PhaseGame.WAIT.value
                
       

        elif jugador.phase_game == PhaseGame.INIT.value:
            
                # esperar 1 segundo para que el otro jugador reciba el mensaje
            # dar a conocer el noimbre del oponente
            # jugador.cliente.datatoSend(f"Oponente: {jugador.getOPponente().cliente.nombre}",None)
        
            jugador.cliente.datatoSend("Partida encontrada, es momento de posicionar a tus personajes",None )
            jugador.posicionar_equipo()

            # en este punto tengo que esperar a que el otro jugador posicione a sus personajes
            if jugador.getOPponente().phase_game == PhaseGame.INIT.value:
                jugador.cliente.datatoSend("Esperando a otro jugador", PhaseGame.WAIT.value)
                jugador.phase_game = PhaseGame.WAIT.value
            else:
                jugador.cliente.datatoSend("es hora de tirar los dados", None)
                if jugador.getOPponente().phase_game == PhaseGame.WAIT.value:
                    jugador.getOPponente().cliente.datatoSend("es hora de tirar los dados", None)
                # hacer un randon entre 1 y 2
                random_int = random.randint(1, 2)
                # si es 1 juego yo primero
                if random_int == 1:
                    # jugador.cliente.datatoSend("Es tu turno", None)
                    jugador.phase_game = PhaseGame.TURN.value
                else:
                    jugador.getOPponente().cliente.datatoSend("Es tu turno", None)
                    jugador.getOPponente().phase_game = PhaseGame.TURN.value
                    jugador.phase_game = PhaseGame.WAIT_TURN.value

        else:
            if jugador.phase_game == PhaseGame.TURN.value:
                informe = ""
                menuTosend= {}
                jugador.cliente.datatoSend("Es tu turno", None)
                if len(jugador.getInforme()) > 0:


                    informe +="---- INFORME ----\n"
                    informe+= jugador.getInforme()
                else:
                    informe+="No hay informe"
                
                situacion= jugador.getSituacion()

                menu = jugador.menu(jugador.getEquipo())
                # de todos los objetos solo dejar el texto
                for key, value in menu.items():
                    menuTosend[key] = {"texto":value["texto"]}
                

                jugador.cliente.datatoSend(
                    {"informe":informe,"situacion":situacion, "menu":menuTosend}, 
                    jugador.phase_game
                )
                # esperar a que el jugador elija una opcion
                opt =  jugador.cliente.recivirData(converToInt=True)
                resultado_accion = ""
                moviendo = False
                if "parametro" in menu[opt].keys(): # cuandio me muevo
                    moviendo = True
                    resultado_accion= menu[opt]["accion"](menu[opt]["parametro"])
                else:
                    try:
                        resultado_accion =menu[opt]["accion"]()
                    except:
                        print("error")
                
                # reseteo
                menu[opt]["reseteo"](
                    menu[opt]["jugadores_reseteo"]
                )
                if not moviendo:
                    jugador.cliente.datatoSend("\n---- RESULTADO DE LA ACCION ----",None)
                    jugador.cliente.datatoSend(resultado_accion[0],None )
                if resultado_accion[1]:
                    jugador.getOPponente().recibir_accion(resultado_accion[0])
                    # find if exist francotirador and artillero in team enemy
                    counter = 0
                    for personaje in jugador.getOPponente().getEquipo():
                        if personaje.type.value == TypePlayer.Franco.value or personaje.type.value == TypePlayer.Artillero.value:
                            counter += 1
                    if counter == 0:
                        jugador.phase_game = PhaseGame.END.value
                        jugador.getOPponente().phase_game = PhaseGame.END.value
                        jugador.cliente.datatoSend("***** Has ganado la partida! *****", jugador.phase_game)
                        jugador.getOPponente().phase_game = PhaseGame.END.value
                        jugador.getOPponente().cliente.datatoSend("***** Has perdido la partida! *****", jugador.getOPponente().phase_game)
                jugador.phase_game = PhaseGame.WAIT_TURN.value
                jugador.getOPponente().phase_game = PhaseGame.TURN.value




            


        
            
       
if __name__ == '__main__':
    lobyy = []
    main(lobyy)