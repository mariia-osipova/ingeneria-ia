
print("ingresa t1")
temperatura1 = int(input())

print("ingresa t2")
temperatura2 = int(input())

print("ingresa t3")
temperatura3 = int(input())


if temperatura1 > 100:
    t1 = True

else:
    t1 = False

if temperatura2 > 100:
    t2 = True
else:
    t2 = False

if temperatura3 > 100:
    t3 = True
else:
    t3 = False

if (t1 and t2 and not t3) or (t3 and t1 and not t2) or (t2 and t3 and not t1):
    print("alerta")
elif (t1 and t2 and t3):
    print("peligro")
elif (t1 or t3 or t2):
    print("precaucion")
else:
    print("estable")
