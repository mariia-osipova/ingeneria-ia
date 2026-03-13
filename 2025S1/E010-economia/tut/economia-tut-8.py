import numpy as np
import matplotlib.pyplot as plt
import subprocess
from pathlib import Path
import sympy as sp

Q = np.linspace(0, 500, 400)

P1 = (240 - Q) / 5 #demanda Qd = 240 - 5P, 5P = 240 - Q, P = (240 - Q)/5
P2 =  Q/15 #oferta Qo = 15P, P = Q/15


plt.figure(figsize=(7, 7))

plt.plot(Q, P1, label='demanda (240 - Q)/5', linewidth=2)
plt.plot(Q, P2, label='oferta Q/15', color='red', linewidth=2)
#plt.plot(Q, P3, label='costos variables totales (CVT = 5 * Q + Q^2 / 2)', color='orange', linewidth=2)
#plt.plot(Q, P4, label='CVM = 5 + Q/2', color='violet', linewidth=2)
#plt.plot(Q, P5, label='demanda (P = 50 - 2Q)', color='green', linewidth=2)

# let's find an equilibrium perfect competition
Q_eq_cp = 180
P_eq_cp = 12

plt.plot([Q_eq_cp, Q_eq_cp], [0, P_eq_cp], 'gray', linestyle='--', linewidth=1)
plt.hlines(y=P_eq_cp,xmin=0,xmax=Q_eq_cp,colors='gray',linestyles='--',linewidth=1)

plt.scatter([Q_eq_cp],[P_eq_cp], color='black', zorder=5) #equilibrium
plt.text(Q_eq_cp + 1, P_eq_cp + 1,'E1', fontsize=14)


#tengo fiaca de calcular a mano los excedentes:

exc_cons = 0.5 * 180 * (48 - 12)
exc_prod = 0.5 * 180 * 12

print('excedente de consumidor: ', exc_cons, 'excedente de productor: ', exc_prod)

#mask = Q <= 180

#plt.fill_between(Q[mask], P1[mask], P_eq_cp, color='blue', alpha=0.2)
#plt.fill_between(Q[mask], P2[mask], P_eq_cp, color='green', alpha=0.2)


#now the state puts a tax on consumers $8.
#Pc = Pp + t
#before the demand curve was Qd = 240 - 5P. now it depends on (Pp + 8):
#Qo = 240 - 5(Pp + 8)
#Q = 240 - 5P - 40
#Q = 200 - 5P
#5P = 200 -Q
#P = (200 - Q) / 5

P3 = (200 - Q) / 5 #demanda con t

plt.plot(Q, P3, label='demanda con t (200-Q)/5', linewidth=2)

plt.legend(loc='upper left', fontsize=12)

#the supply curve is the same. let's find new point of optimal transaction quantity.
#(200-Q)/5 = Q/15

Q_eq_t = 150
P_eq_t = 10


plt.plot([Q_eq_t, Q_eq_t], [0, P_eq_t], 'gray', linestyle='--', linewidth=1)
plt.hlines(y=P_eq_t,xmin=0,xmax=Q_eq_t,colors='gray',linestyles='--',linewidth=1)

plt.scatter([Q_eq_t],[P_eq_t], color='black', zorder=5) #equilibrium
plt.text(Q_eq_t + 1, P_eq_t + 1,'E2', fontsize=14)

#shit. im fuckng tired. now let's find a point of P for this Q with an old demand curve to find the perdida de eficiencia.
#(240-150)/5

Q_eq_t = 150
P_d_perd = 18

plt.plot([Q_eq_t, Q_eq_t], [0, P_d_perd],color='gray', linestyle='--', linewidth=1)
plt.hlines(y=P_d_perd, xmin=0, xmax=Q_eq_t, color='gray', linestyle='--', linewidth=1)

plt.scatter([Q_eq_t], [P_d_perd], color='black', zorder=5)
plt.text(Q_eq_t + 1, P_d_perd + 1, 'B', fontsize=14)

#lets colour this fucking thing

mask = (Q >= 150) & (Q <= 180)

plt.fill_between(Q[mask], P1[mask], P2[mask], color='blue', alpha=0.2)

#lets calculate this fucking thing

peso_muerto = 0.5 * 8 * (180 - 150)
print('peso muerto: ', peso_muerto)

plt.ylabel('P', fontsize=14)
plt.xlabel('Q', fontsize=14)

plt.grid(True)

plt.xlim(0, 300)
plt.ylim(0,60)


#save
fname = Path("my_plot.png").resolve()
plt.savefig(fname, dpi=300, bbox_inches="tight")

# copy to memory (macOS) so i can use command + v then
script = f'''
set the clipboard to (read (POSIX file "{fname}") as «class PNGf»)
'''
subprocess.run(["osascript", "-e", script], check=True)

fname.unlink() #delete the file because i dont fucking need this in my code

plt.show()