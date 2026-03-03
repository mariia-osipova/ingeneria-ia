personas = [
    { 'nombre': 'Juan', 'edad': 17 },
    { 'nombre': 'Pedro', 'edad': 18 },
    { 'nombre': 'Esteban', 'edad': 15 }
]

lista_edades = []

for i in personas:
    lista_edades.append(i['edad'])

max_index = lista_edades.index(max(lista_edades))
print(personas[max_index]['nombre'])

