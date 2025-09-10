from math import inf

n = int(input())
minX = inf
minY = inf

maxX = - inf
maxY = - inf

for i in range(n):
    x, y = map(int, input().split())

    minX = min(x, minX)
    minY = min(y, minY)
    maxX = max(x, maxX)
    maxY = max(y, maxY)

print(2* (maxX- minX + 2 + maxY- minY + 2))
