print("Platos preferidos \n=================")

print("Ingrese el primer plato:")
primer_plato = input()

print("Ingrese el precio:")
primer_precio = int(input())

print("Ingrese el segundo plato:")
segundo_plato = input()

print("Ingrese el precio:")
segundo_precio = int(input())

print("Ingrese el tercer plato:")
tercer_plato = input()

print("Ingrese el precio:")
tercer_precio = int(input())

precio_minimo=min(primer_precio, segundo_precio, tercer_precio)
precio_maximo=max(primer_precio, segundo_precio, tercer_precio)

precio_promedio = (primer_precio + segundo_precio + tercer_precio) / 3

print("Resumen \n=================")

n = len("=================")

len_1 = len(str(primer_plato))
len_2 = len(str(segundo_plato))
len_3 = len(str(tercer_plato))

falta_1 = (n - len_1)
falta_2 = (n - len_2)
falta_3 = (n - len_3)

space_1 = falta_1 * " "
space_2 = falta_2 * " "
space_3 = falta_3 * " "

print(primer_plato, space_1, "$", primer_precio)
print(segundo_plato, space_2, "$", segundo_precio)
print(tercer_plato, space_3, "$", tercer_precio)

print("")

print("--------------------")

str_precio_max = "Precio mas alto:"
str_precio_min = "Precio mas bajo:"
str_precio_promedio = "Precio promedio:"

len_4 = len(str(str_precio_max))

falta_4 = int(n - len_4)

space_4 = falta_4 * " "
print(str_precio_max, space_4, "$", precio_maximo)
print(str_precio_min, space_4, "$", precio_minimo)
print(str_precio_promedio, space_4, "$", precio_promedio)