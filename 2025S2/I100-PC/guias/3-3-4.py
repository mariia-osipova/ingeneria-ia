datos = {
    "posicion" : [1,2,3,4],
    "pais" : ["Argentina", "Francia", "Croacia", "Marruecos"],
    "continente" : ["America", "Europa", "Europa", "Africa"],
    "capitan" : ["Lionel Messi", "Hugo Lloris", "Luka Modric", "Romain Saiss"],
    "entrenador" : ["Lionel Scaloni", "Didier Deschamps", "Zlatko Dalic", "Walid Regragui"],
    "mundiales ganados" : [[1978, 1986], [1998, 2018], [], []]
}

print(len(datos["pais"]))

datos["mundiales ganados"][0] += [2022]

year = 2022
for i in range(0, len(datos["mundiales ganados"])):
    if year in datos["mundiales ganados"][i]:
        ganador = datos["capitan"][i]
        break

else:
    ganador = 'there was no team that won this year in the list.'

print(datos["mundiales ganados"])
print(ganador)
print(len(datos["mundiales ganados"][0]))

