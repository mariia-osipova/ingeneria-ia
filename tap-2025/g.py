a, b, c = map(int, input().split()) #map = un generador que aplica la funccion a cu

# a, b, c = (int(x) for x in input().split())

if (b-a) % c == 0:
    print("S")
else:
    print("N")
