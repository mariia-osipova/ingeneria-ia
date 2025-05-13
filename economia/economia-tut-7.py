import numpy as np
import matplotlib.pyplot as plt
import subprocess
from pathlib import Path

Q = np.linspace(0, 500, 400)

P1 = 5 + Q #demanda
P2 = 20 + 0 * Q #precio = ingreso marginal


plt.figure(figsize=(7, 7))

plt.plot(Q, P1, label='demanda (P = 5 + Q)')
plt.plot(Q, P2, label='precio del mercado competitivo (P = 20)', color='red', linewidth=2)

plt.xlim(0, 50)
plt.ylim(0, 50)

plt.ylabel('P', fontsize=14)
plt.xlabel('Q', fontsize=14)

plt.legend(fontsize=12)
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