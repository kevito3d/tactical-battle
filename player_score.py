class PlayerScore:
    nombre=""
    score=0
    def __init__(self, score=0, nombre="") -> None:
        self.score=score
        self.nombre=nombre
    
    def setScore(self, score):
        self.score=score
    
    def getScore(self):
        return self.score
    
    def getNombre(self):
        return self.nombre

    def __str__(self) -> str:
        return self.nombre + ":" + str(self.score) 