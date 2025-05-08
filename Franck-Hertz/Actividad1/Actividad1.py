import numpy as np
import matplotlib.pyplot as plt
import csv

from itertools import islice
from scipy.optimize import curve_fit
from scipy.signal import find_peaks
from matplotlib.lines import Line2D

Spath = 'Franck-Hertz\\Actividad1\\Datos\\T_constante175'

def read_data(path, skip_rows = 3):
    with open(path, 'r') as file:
        lines = islice(file,skip_rows,None)
        data = [list(map(float,line.replace(',', '.').split())) for line in lines]
        
    col1, col2 = zip(*data)
    return list(col1), list(col2)

plt.figure(figsize=(7,5.5))

han = []

for i in range(2,6):
    Path = Spath + f'({i})'
    x, y = read_data(Path)
    xfil, yfil = zip(*[(xi, yi) for xi,yi in zip(x,y) if xi < 46])
    xfil, yfil = np.array(list(xfil)), np.array(list(yfil))
    mind, _ = find_peaks(-yfil, distance=10, prominence=0.18)
    mind = np.array(mind)
    mins = xfil[mind]
    print(mins)
    for min in mins:
        plt.vlines(x=min, ymin=0, ymax=yfil[xfil == min], color='black', linestyle='--', linewidth=0.6)
    scatter = plt.scatter(xfil,yfil, label=f'Datos {i-1}',s = 1)
    han.append(scatter)

linea_punteada = Line2D([0], [0], color='black', linestyle='--', linewidth=1, label='Mínimos locales')

han.insert(0, linea_punteada)

plt.legend(handles=han, scatterpoints=1, markerscale=5)

plt.title('Corriente en función del potencial')
plt.xlabel(r'$U_{1}$  $(V)$', fontsize=15)
plt.ylabel(r'$I_{A}$  $(nA)$', fontsize=15)
plt.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
plt.savefig('Franck-Hertz/Actividad1/Datos_T_cte.png', dpi=300, bbox_inches='tight')