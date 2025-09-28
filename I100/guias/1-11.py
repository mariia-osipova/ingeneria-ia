from xml.sax.saxutils import prepare_input_source

q_personas = 5
precio_bebidas = 410 #(+picadas)
precio_postre = 800
precio_pizza_6 = 1020
precio_pizza_8 = 1380

precio_nada = 0

q_porcionez_pizza_tot = 4 * q_personas

q_pizzas_6 = 1
q_pizzas_8 = 1

q_porciones_6 = 6
q_porciones_8 = 8

precio_pizzas_total = precio_pizza_6 * 2 + precio_pizza_8
precio_pizzas_total_1 = precio_pizzas_total_2 = precio_pizzas_total/2

index_personas = {1,2,3,4,5}
precios = (precio_pizzas_total_1, precio_pizzas_total_2, precio_bebidas, precio_postre, precio_nada)

for x, y in zip(precios, index_personas):
    print(y, "gasto", x)

precio_total = precio_pizzas_total + precio_bebidas + precio_postre
precio_por_cabeza = precio_total/q_personas

print(precio_por_cabeza, "= dinero por cabeza")

falta = 0
deuda = 0
num_personas_en_falta = 0
num_personas_en_deuda = 0

rows, cols = 3, q_personas
matrix = [[0]*cols for _ in range(rows)]

positions_falta = []
positions_deuda = []

matrix[0] = [1,2,3,4,5]
matrix[1] = [precio_pizzas_total_1, precio_pizzas_total_2, precio_bebidas, precio_postre, precio_nada]

for j in range(cols):
    person = matrix[0][j]
    precio = matrix[1][j]
    precio_new = matrix[2][j]

    if precio > precio_por_cabeza:
        precio_new = precio - precio_por_cabeza
        matrix[2][j] = precio_new
        positions_falta.append((2, j, precio_new))

    elif precio < precio_por_cabeza:
        precio_new = precio - precio_por_cabeza
        matrix[2][j] = precio_new
        positions_deuda.append((2, j, precio_new))

# for j, in range(cols):


print(matrix)

# print(positions_falta)
# print(positions_deuda)

row_of_justice = matrix[2]

for (x,y,z) in positions_falta:
    print("a", y+1, "le falta", z)

for (x,y,z) in positions_deuda:
    print(y+1, "deuda", -z)

row_of_justice = []
print(row_of_justice)



# for (x_f,y_f,z_f), (x_d, y_d, z_d), x in zip(positions_falta, positions_deuda, row_of_justice):






# for x, y in zip(precios, index_personas):
#     if x > precio_por_cabeza:
#         print("a", y, "le falta", x - precio_por_cabeza)
#         falta += x - precio_por_cabeza
#         print(falta, "= falta")
#         num_personas_en_falta += 1
#         print("num personas en falta =", num_personas_en_falta)
#
#     elif x < precio_por_cabeza:
#         print(y, "debe", abs(x - precio_por_cabeza))
#         deuda += abs(x - precio_por_cabeza)
#         print("deuda total =", deuda)
#         num_personas_en_deuda += 1
#         print("num personas en deuda =",num_personas_en_deuda)
#
#     else:
#         print(y, "no debe nada")

