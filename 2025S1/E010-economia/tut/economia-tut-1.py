import matplotlib.pyplot as plt
import numpy as np

# Создаём массив значений для оси X (количество ложек сахара)
x = np.linspace(0, 6, 300)
# Функция удовлетворения: параболическая кривая с максимумом при x = 2 (оптимальное количество сахара)
y = -1 * (x - 2)**2 + 5

plt.figure(figsize=(8, 5))
plt.plot(x, y, label='Функция удовлетворения', color='blue')

# Определяем точки A, B, C
x_points = [0, 2, 4]
y_points = [-1*(xi - 2)**2 + 5 for xi in x_points]
plt.scatter(x_points, y_points, color='red')

# Подписываем точки
plt.text(0, y_points[0], ' A: 0 ложек', fontsize=10, ha='right', va='bottom')
plt.text(2, y_points[1], 'B: 2 ложки', fontsize=10, ha='center', va='bottom')
plt.text(4, y_points[2], 'C: 4 ложки', fontsize=10, ha='left', va='bottom')

# Подписи осей и заголовок
plt.xlabel('Количество сахара (ложки)')
plt.ylabel('Удовлетворение')
plt.title('Зависимость удовлетворения от количества сахара в кофе')
plt.legend()
plt.grid(True)
plt.show()
