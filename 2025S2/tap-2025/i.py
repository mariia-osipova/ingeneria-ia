def readInts():
    return map(int, input().split())
n, m = readInts()

ret = [0] * (n+1)
for ronda in range(m):
    X, Y = readInts()
    c = list(readInts())
    c1 = c.count(1)
    opcionX = X//(c1 +1)
    if opcionX >= Y:
        ret[n] += opcionX
    else:
        ret[n] += Y
        if c1 != 0:
            opcionX = X//c1
    for i in range(n):
        if c[i] == 2:
            ret[i] += Y
        else:
            ret[i] += opcionX

print(" ".join(map(str, ret)))

#print(*ret)