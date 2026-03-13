import numpy as np
import matplotlib.pyplot as plt

# Создаем две области: x от -5 до -0.1 и от 0.1 до 5
x1 = np.linspace(-5, -0.1, 300)
x2 = np.linspace(0.1, 5, 300)
y1 = -1 / x1**2
y2 = -1 / x2**2

plt.figure(figsize=(8,6))
plt.plot(x1, y1, label="$f'(x) = -1/x^2$")
plt.plot(x2, y2, label="$f'(x) = -1/x^2$")
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)
plt.xlabel("x")
plt.ylabel("$f'(x)$")
plt.title("График производной функции $f(x)=1/x$, где $f'(x) = -1/x^2$")
plt.legend()
plt.ylim(-100, 0)
plt.show()
