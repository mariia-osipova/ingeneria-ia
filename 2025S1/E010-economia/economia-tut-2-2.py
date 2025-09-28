import matplotlib.pyplot as plt
import numpy as np

# Определяем диапазоны для осей
x_original = np.linspace(0, 12, 300)  # для исходной бюджетной прямой
x_new = np.linspace(0, 5, 300)          # для новой бюджетной прямой

# Исходная бюджетная прямая: 5x+6y=60  =>  y = 10 - (5/6)x
y_original = 10 - (5/6)*x_original

# Новая бюджетная прямая: 12x+6y=60  =>  y = 10 - 2x
y_new = 10 - 2*x_new

# Задаём ключевые точки:
A = (6, 5)    # Исходное равновесие на старой бюджетной прямой
B = (2, 6)    # Компенсированная точка на новой бюджетной прямой (с эффектом замещения)
C = (3, 4)    # Новое равновесие на новой бюджетной прямой (после эффекта дохода)

plt.figure(figsize=(8,6))

# Рисуем исходную бюджетную прямую
plt.plot(x_original, y_original, label='Исходная: 5x+6y=60', color='blue')
# Рисуем новую бюджетную прямую
plt.plot(x_new, y_new, label='Новая: 12x+6y=60', color='red')

# Отмечаем точки
plt.plot(A[0], A[1], 'bo', label='A = (6,5)')
plt.plot(B[0], B[1], 'go', label='B = (2,6)')
plt.plot(C[0], C[1], 'ro', label='C = (3,4)')

# Добавляем стрелки: от A к B (эффект замещения)
plt.annotate("", xy=B, xytext=A, arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
plt.text((A[0]+B[0])/2 - 0.8, (A[1]+B[1])/2 + 0.5, 'Эффект замещения', fontsize=9)

# От стрелка от B к C (эффект дохода)
plt.annotate("", xy=C, xytext=B, arrowprops=dict(arrowstyle="->", color='black', lw=1.5))
plt.text((B[0]+C[0])/2 + 0.1, (B[1]+C[1])/2 - 0.5, 'Эффект дохода', fontsize=9)

# Настройки графика
plt.xlabel('Coca-Cola (единицы)')
plt.ylabel('Papas fritas (единицы)')
plt.title('Эффекты замещения и дохода\n(точка B=(2,6) на новой бюджетной прямой)')
plt.legend()
plt.grid(True)
plt.xlim(0, 13)
plt.ylim(0, 12)

plt.show()
