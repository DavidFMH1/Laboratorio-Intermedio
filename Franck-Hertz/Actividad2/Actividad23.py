import numpy as np
import matplotlib.pyplot as plt
import csv

from itertools import islice
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from matplotlib.lines import Line2D

Spath = 'Franck-Hertz\\Actividad2\\Datos\\UH_'

def read_data(path, skip_rows = 3):
    with open(path, 'r') as file:
        lines = islice(file,skip_rows,None)
        data = [list(map(float,line.replace(',', '.').split())) for line in lines]
        
    col1, col2 = zip(*[(row[0], row[1]) for row in data])
    return np.array(list(col1)), np.array(list(col2))

han = []

for i in range(6):
    path = Spath + f'{58+2*i}'
    x,y = read_data(path)
    xfil, yfil = zip(*[(xi, yi) for xi,yi in zip(x,y) if xi < 50])
    xfil, yfil = np.array(list(xfil)), np.array(list(yfil))
    scatter = plt.scatter(xfil, yfil, label=f'Datos U2 {(58+2*i)/10}', s=5)
    han.append(scatter)

plt.legend(handles=han, scatterpoints=1, markerscale=5)

plt.title('Corriente en función del potencial')
plt.xlabel(r'$U_{1}$  $(V)$', fontsize=15)
plt.ylabel(r'$I_{A}$  $(nA)$', fontsize=15)
plt.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
plt.savefig('Franck-Hertz/Actividad2/UH_variable.png', dpi=300, bbox_inches='tight')