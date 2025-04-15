import numpy as np
import matplotlib.pyplot as plt

# Генерируем значения z
x = np.linspace(-4, 4, 1000)
# Вычисляем плотность стандартного нормального распределения:
# f(x) = (1/√(2π)) * exp(-x²/2)
y = (1/np.sqrt(2*np.pi)) * np.exp(-0.5 * x**2)

plt.figure(figsize=(8, 4))
plt.plot(x, y, 'b-', lw=2, label='Стандартное нормальное распределение')

# Заштриховываем области: левый хвост (x < -1.96) и правый хвост (x > 1.96)
plt.fill_between(x, y, where=(x < -1.96), color='red', alpha=0.5, label='Левый хвост (2.5%)')
plt.fill_between(x, y, where=(x > 1.96), color='red', alpha=0.5, label='Правый хвост (2.5%)')

# Отмечаем критические значения
plt.axvline(-1.96, color='black', linestyle='--', label='-1.96')
plt.axvline(1.96, color='black', linestyle='--', label='+1.96')

plt.title('Стандартное нормальное распределение\n(Критические значения для α=0.05)')
plt.xlabel('z')
plt.ylabel('Плотность вероятности')
plt.legend()
plt.show()
