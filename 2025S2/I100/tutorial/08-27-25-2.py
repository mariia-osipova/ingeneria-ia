
km = float(1.609344)

nombre = input("Ingrese nombre: ")
milas_input = float(input("Ingrese milas a convertir: "))

respuesta = float(milas_input*km)
redondeado = round(respuesta, 2)
print(f"Hola, {nombre}, la convercion resulta: {redondeado} km")
