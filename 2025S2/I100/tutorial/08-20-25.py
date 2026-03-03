cantidad_A = int(input("Ingrese la cantidad de alumnos de la comicion A: "))
cantidad_B = int(input("Ingrese la cantidad de alumnos de la comicion B: "))
cantidad_C = int(input("Ingrese la cantidad de alumnos de la comicion C: "))

total = cantidad_A + cantidad_B + cantidad_C

porc_1 = (cantidad_A / total) * 100
porc_2 = (cantidad_B / total) * 100
porc_3 = (cantidad_C / total) * 100

print(f"Hay {total} alumnos en todas las comiciones\n"
      f"Comicion A: {porc_1} %\n"
      f"Comicion B: {porc_2} %\n"
      f"Comicion C: {porc_3} %")
