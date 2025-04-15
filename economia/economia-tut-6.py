import numpy as np
import matplotlib.pyplot as plt

Q = np.linspace(0, 500, 400)

P1 = Q/5
P2 = -Q/2 + 175
P3 = 50 - Q * 0

plt.figure(figsize=(7, 7))

plt.plot(Q, P1, label='oferta (P = Q/5)')
plt.plot(Q, P2, label='demanda (P = -Q/2 + 175)', color='red', linewidth=2)
plt.plot(Q, P3, label=' (P = 50)', color='grey', linewidth=2,  linestyle='--')

plt.xlim(0, 500)
plt.ylim(0, 200)

plt.ylabel('P', fontsize=14)
plt.xlabel('Q', fontsize=14)

plt.legend(fontsize=12)
plt.grid(True)

mask = Q <= 250  #P=50, Q1=5*50=250

plt.fill_between(Q[mask], P1[mask], 50, color='blue', alpha=0.2)
plt.fill_between(Q[mask], P2[mask], 50, color='green', alpha=0.2)

plt.show()

