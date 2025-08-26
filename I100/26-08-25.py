clave = str("Python1234")

intents = 0

while intents < 2:
    clave_ing = str(input("ingress the key: "))

    if clave == clave_ing:
        print("access permitido")
        break
    else:
        intents += 1

else: print("access denied")



