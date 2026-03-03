nombre = "<NAME>"
apellido = "<APELLIDO>"
edad = "<EDAD>"
nota_p1 = 10
nota_p2 = 1
nota_p3 = 3

datos = {
    "nombre" : nombre,
    "apellido" : apellido,
    "edad" : edad,
    "notas" : {"parcial 1" : nota_p1, "parcial 2" : nota_p2, "parcial 3" : nota_p3 },
}

promedio = ((datos["notas"]["parcial 1"]) + (datos["notas"]["parcial 2"]) + (datos["notas"]["parcial 3"]))/ 3

promedio = round(promedio,2)

print(promedio)