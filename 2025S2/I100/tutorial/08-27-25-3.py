lado_1 = float(input("1: "))
lado_2 = float(input("2: "))
lado_3 = float(input("3: "))

if lado_1 <= 0 or lado_2 <= 0 or lado_3 <= 0:
    print("wtf")
elif lado_1 + lado_2 < lado_3 or lado_2 + lado_3 < lado_1 or lado_1 + lado_3 < lado_2:
    print("bye")

elif lado_1 == lado_2 == lado_3:
    print("eq")
elif lado_1 == lado_2 or lado_1 == lado_3 or lado_2 == lado_3:
    print("iso")
elif lado_1 != lado_2 and lado_1 != lado_3:
    print("es")
