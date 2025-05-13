import numpy as np
import matplotlib.pyplot as plt
import subprocess
from pathlib import Path

Q = np.linspace(0, 500, 400)

P1 = 5 + Q #Cmg
P2 = 20 + 0 * Q #precio = ingreso marginal
P3 = 5 * Q + Q**2 / 2 #CVT
P4 = 5 + Q / 2 #CVM

plt.figure(figsize=(7, 7))

plt.plot(Q, P1, label='costo marginal (Cmg = 5 + Q)')
plt.plot(Q, P2, label='precio del mercado competitivo (P = 20)', color='red', linewidth=2)
plt.plot(Q, P3, label='costos variables totales (CVT = 5 * Q + Q^2 / 2)', color='orange', linewidth=2)
plt.plot(Q, P4, label='CVM = 5 + Q/2', color='violet', linewidth=2)
plt.legend(loc='upper left', fontsize=12)

# let's find an equilibrium
Q_eq = 20 - 5    # =15
P_eq = 20

plt.plot([Q_eq, Q_eq], [0, P_eq], 'gray', linestyle='--', linewidth=1)

plt.scatter([Q_eq],[P_eq], color='black', zorder=5) #equilibrium
plt.text(Q_eq + 1, P_eq + 1,'E (15, 20)', fontsize=14)

plt.xlim(0, 50)
plt.ylim(0,50)
#plt.ylim(0,500)

plt.ylabel('P', fontsize=14)
plt.xlabel('Q', fontsize=14)

plt.grid(True)

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