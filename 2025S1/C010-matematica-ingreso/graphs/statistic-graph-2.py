import numpy as np
import matplotlib.pyplot as plt

# Генерируем значения z от -4 до 4
x = np.linspace(-4, 4, 1000)
# Вычисляем плотность стандартного нормального распределения:
# f(x) = (1/√(2π)) * exp(-x²/2)
y = (1 / np.sqrt(2 * np.pi)) * np.exp(-0.5 * x**2)

plt.figure(figsize=(8, 4))
plt.plot(x, y, 'b-', lw=2, label='Стандартное нормальное распределение')

# Заштриховываем область нижнего хвоста (x < -1.96)
plt.fill_between(x, y, where=(x < -1.96), color='red', alpha=0.5, label='Нижний хвост (2.5%)')
# Заштриховываем область верхнего хвоста (x > 1.96)
plt.fill_between(x, y, where=(x > 1.96), color='red', alpha=0.5, label='Верхний хвост (2.5%)')

# Отмечаем критические значения линиями
plt.axvline(-1.96, color='black', linestyle='--', lw=1.5, label='Критическое значение -1.96')
plt.axvline(1.96, color='black', linestyle='--', lw=1.5, label='Критическое значение 1.96')

plt.title('Стандартное нормальное распределение\nКритические значения для α = 0.05')
plt.xlabel('z')
plt.ylabel('Плотность вероятности')
plt.legend(loc='upper left')
plt.show()
