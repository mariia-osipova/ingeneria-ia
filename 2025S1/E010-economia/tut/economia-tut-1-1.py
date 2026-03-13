import numpy as np
import matplotlib.pyplot as plt

# Определяем функцию полезности
def U(x, y):
    return np.sqrt(x * y)  # пример: функция Кобба-Дугласа

# Задаем диапазоны значений для x и y
x = np.linspace(0.1, 10, 400)
y = np.linspace(0.1, 10, 400)
X, Y = np.meshgrid(x, y)

# Вычисляем значение функции на сетке
Z = U(X, Y)

# Уровень полезности для построения кривой безразличия
c = 2.0  # можно изменить на нужное значение

# Строим контур, где U(x,y) = c
plt.figure(figsize=(8, 6))
contour = plt.contour(X, Y, Z, levels=[c], colors='blue')
plt.clabel(contour, inline=True, fontsize=10)
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Кривая безразличия: U(x, y) = {c}')
plt.grid(True)
plt.show()
