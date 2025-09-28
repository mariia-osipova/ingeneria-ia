producto=input("Ingrese el primer producto: ")
precio=float(input("Ingrese el precio: "))
cantidad=int(input("Ingrese el cantidad: "))

producto2 = input("Ingrese el segundo producto: ")
precio2 = float(input("Ingrese el precio: "))
cantidad2 = int(input("Ingrese el cantidad: "))

producto3 = input("Ingrese el ultimo producto: ")
precio3 = float(input("Ingrese el precio: "))
cantidad3 = int(input("Ingrese el cantidad: "))


dict_name = {
    "producto": [producto, producto2, producto3]
}

dict_precio = {
    "precio": [precio, precio2, precio3]
}

dict_cantidad = {
    "cantidad": [cantidad, cantidad2, cantidad3]
}

d = {
    "producto": producto,
    "precio": precio,
    "cantidad": cantidad,
}

d2 = {
    "producto": producto2,
    "precio": precio2,
    "cantidad": cantidad2,
}

d3 = {
    "producto": producto3,
    "precio": precio3,
    "cantidad": cantidad3,
}

print(d["producto"], d["precio"], d["cantidad"], d3["producto"], d3["precio"], d3["cantidad"])