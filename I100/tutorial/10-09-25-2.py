import random

numero = random.randint(1, 200)
print(numero)

def adivinar():
    numero_jugador = int(input("Ingrese un numero: "))
    i = 1

    while i < 10:
        if numero_jugador == numero:
            print(f"congrats bitch, adivinaste el numero {numero}, con {i} attempts")
            break
        elif numero_jugador > numero:
            print(f"El numero {numero_jugador} es mayor al numero de la compu")
            numero_jugador = int(input("Ingrese un numero de vuelta: "))
            i += 1
        else:
            print(f"El numero {numero_jugador} es menor al numero de la compu")
            numero_jugador = int(input("Ingrese un numero: "))
            i += 1
        print("too many attempts bitch")

adivinar()



