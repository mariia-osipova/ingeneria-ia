def promedio():
    nota = float(input("Ingresa la nota: "))
    i = 0
    suma = 0
    while nota != -1:
        i += 1
        suma += nota
        print(i)
        print(suma)
        print(suma / i)
        nota = float(input("Ingresa la nota: "))

    if i > 0:
        print(f"El promedio de la nota es: {suma / i}")
    else:
        print("no se ingresaron notas")

promedio()