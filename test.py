# leer un fichero para leerlo y escribirlo
# from lde import LDE
# from player_score import PlayerScore
# file = open("ranking_simple.txt", "r")

# lines = file.readlines()

# lista = LDE()
# for line in lines:
#     # quitar el ultimo caracter
#     line = line[:-1]
#     [name, score]= line.split(":")
#     lista.enlistar(int(score), name)

# lista.imprimir()

# from cola import Cola
# # Instancia de la clase
# c = Cola()
# # Inserccion de nodos
# c.encolar(5)
# c.encolar(7)
# c.encolar(9)
# # Imprimimos la lista de nodos
# c.mostrar()
# # Extraemos un elemento
# extraido = c.desencolar()
# print(extraido)
# c.mostrar()
# encontrado = c.buscar(5)
# if encontrado:
#     print("Encontrado")
# else:
#     print("Nope")