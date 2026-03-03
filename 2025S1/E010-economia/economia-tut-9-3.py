import numpy as np
import matplotlib.pyplot as plt
import subprocess
from pathlib import Path
import sympy as sp

Q = np.linspace(0, 500, 400)

#P = 10
P1 = 2 + 0.25 * Q #Cmg privado
P2 = 2 + 0.40 * Q #Cmg social
P3 = 2 * Q + 0.5 * Q ** 2 #CVT
P4 = 10 + Q * 0 #Img = const porq' es cp

plt.figure(figsize=(7, 7))

plt.plot(Q, P1, label='Cmg1', linewidth=2)
plt.plot(Q, P2, label='Cmg2', color='red', linewidth=2)
plt.plot(Q, P3, label='costos variables totales (CVT = 2 * Q + 0.5 * Q ** 2)', color='orange', linewidth=2)
plt.plot(Q, P4, label='Img', color='violet', linewidth=2)
#plt.plot(Q, P5, label='demanda (P = 50 - 2Q)', color='green', linewidth=2)


#lest find the fucking Q1 from a)


# 10 = 2 + 0.25 * Q
# Q = 32

Q_priv = 32
P_priv = 10

plt.plot([Q_priv, Q_priv], [0, P_priv], 'gray', linestyle='--', linewidth=1)
plt.hlines(y=P_priv,xmin=0,xmax=Q_priv,colors='gray',linestyles='--',linewidth=1)

plt.legend(loc='upper left', fontsize=12)

plt.scatter([Q_priv],[P_priv], color='black', zorder=5) #equilibrium
plt.text(Q_priv + 1, P_priv + 1,'E1', fontsize=14)


#tengo fiaca de calcular a mano los excedentes:
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

#P3 = (200 - Q) / 5 #demanda con t

#plt.plot(Q, P3, label='demanda con t (200-Q)/5', linewidth=2)

#plt.legend(loc='upper left', fontsize=12)

#the supply curve is the same. let's find new point of optimal transaction quantity.
#(200-Q)/5 = Q/15

#plt.plot([Q_eq_t, Q_eq_t], [0, P_eq_t], 'gray', linestyle='--', linewidth=1)
#plt.hlines(y=P_eq_t,xmin=0,xmax=Q_eq_t,colors='gray',linestyles='--',linewidth=1)

#plt.scatter([Q_eq_t],[P_eq_t], color='black', zorder=5) #equilibrium
#plt.text(Q_eq_t + 1, P_eq_t + 1,'E2', fontsize=14)

#shit. im fuckng tired. now let's find a point of P for this Q with an old demand curve to find the perdida de eficiencia.
#(240-150)/5


#plt.plot([Q_eq_t, Q_eq_t], [0, P_d_perd],color='gray', linestyle='--', linewidth=1)
#plt.hlines(y=P_d_perd, xmin=0, xmax=Q_eq_t, color='gray', linestyle='--', linewidth=1)

#plt.scatter([Q_eq_t], [P_d_perd], color='black', zorder=5)
#plt.text(Q_eq_t + 1, P_d_perd + 1, 'B', fontsize=14)

#lets colour this fucking thing

#mask = (Q >= 150) & (Q <= 180)

#plt.fill_between(Q[mask], P1[mask], P2[mask], color='blue', alpha=0.2)


plt.ylabel('P', fontsize=14)
plt.xlabel('Q', fontsize=14)

plt.grid(True)

plt.xlim(0, 30)
plt.ylim(0, 15)


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