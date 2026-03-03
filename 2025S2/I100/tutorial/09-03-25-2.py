from numpy.ma.extras import row_stack

matrix = [[1, 2, 3, 4, 5],
          [6, 7, 8, 9, 10],
          [11, 12, 13, 14, 15],
          [16, 17, 18, 19, 20],
          [21, 22, 23, 24, 25]
          ]

suma_2 = sum(matrix[1])

for i in range(len(matrix)):
    suma_diagonal = matrix[i][i]
    i =+ 1

print(suma_2)
print(suma_diagonal)
