n = int(input())
minX = 0
minY = 0

maxX = 10**20
maxY = 10**20

for i in range(n):
    x, y = map(int, input().split())

    minX = min(x, minX)
    minY = min(y, minY)
    maxX = max(x, maxX)
    maxY = max(y, maxY)

print(2* (maxX- minX + 2 + maxY- minY + 2))
