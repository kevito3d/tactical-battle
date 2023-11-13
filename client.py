import socket
import sys
from phase_game import PhaseGame
from utils import convertToBytes, convertToDict, limpiar_terminal



def main ():
    # Inicializamos el juego
    # pedir nombre del jugador
    nombre = input("Introduce tu nombre: ")

    
    # Crear un socket TCP/IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # get ip from command line argument y si no hay argumento, usa localhost
    ip = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    # get port from command line argument y si no hay argumento, usa 1234
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1234

    # Conectarse al servidor
    server_address = (ip, port)
    print(f'connecting to {server_address}')
    sock.connect(server_address)

    # Enviar nombre del jugador para unirse a la partida
    try:
        # Send data
        message = {
            'message': nombre,
            'phase': PhaseGame.JOIN.value
            }
        sock.sendto(convertToBytes(message), server_address)

        end_ganme = False
        while not end_ganme:

            # Receive response

            data = sock.recv(1024)
            data = convertToDict(data)
            # print(data["phase"])
            if data["phase"] ==None:
                print(data["message"])
            if data["phase"] == PhaseGame.INIT.value:
                pos = input(data["message"])
                sock.sendto(convertToBytes(pos), server_address)
            if data["phase"] == PhaseGame.WAIT_DICE.value:
                # show dice
                limpiar_terminal()
                print(data["message"]) 
            if data["phase"] == PhaseGame.TURN.value:
                # show board
                limpiar_terminal()
                print(data["message"]["informe"])
                print(data["message"]["situacion"]+"\n")
                menu = data["message"]["menu"]
                for key, value in menu.items():
                    print(f"{key}. {value['texto']}")
        
                opt = None
                        # validate opt if is in menu
                print(menu.keys())
                while opt ==None or opt not in menu.keys():
                    try: 
                        opt = input("Seleccione una opción: ")
                        
                    except ValueError:
                        print("opción no válida")
                sock.sendto(convertToBytes(opt), server_address)
            if data["phase"] == PhaseGame.TURN_ACTION.value:
                pos = input(data["message"])
                sock.sendto(convertToBytes(pos), server_address)

            if data["phase"] == PhaseGame.WAIT_TURN.value:
                print("Esperando tu turno...")
            if data["phase"] == PhaseGame.END.value:
                print(data["message"])
                end_ganme =True
            
    
            
    finally:
        print('closing socket')
        sock.close()
    

if __name__ == "__main__":
    main()





