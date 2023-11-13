from enum import Enum
class PhaseGame(Enum):

    
    # join new player
    JOIN = 1
    # wait for players
    WAIT = 2
    # order my pieces
    INIT = 3

    # tesperando dados
    WAIT_DICE = 4
    # wait for player turn
    WAIT_TURN = 4
    # player turn
    TURN = 5
    TURN_ACTION = 6
    # end game
    END = 7