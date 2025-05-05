import numpy as np
import matplotlib.pyplot as plt
import csv

from itertools import islice
from scipy.signal import find_peaks
from scipy.optimize import curve_fit

Spath = 'Franck-Hertz\\Actividad2\\Datos\\Tconstante_'

def read_data(path, skip_rows = 3):
    with open(path, 'r') as file:
        lines = islice(file,skip_rows,None)
        data = [list(map(float,line.replace(',', '.').split())) for line in lines]
        
    col1, col2 = zip(*data)
    return np.array(list(col1)), np.array(list(col2))

for i in range(0,4):
    Path = Spath + f'{180+i*5}'
    x, y = read_data(Path)
    xfil, yfil = zip(*[(xi, yi) for xi,yi in zip(x,y) if yi < 47])
    xfil, yfil = np.array(list(xfil)), np.array(list(yfil))
    mind, _ = find_peaks(-yfil, distance=10, prominence=0.2)
    mind = np.array(mind)
    mins = xfil[mind]
    for min in mins:
        plt.axvline(x=min, color='red', linestyle='--', linewidth=1)
    plt.scatter(xfil,yfil, label=f'Datos {180+i*5}',s = 5)


plt.ylabel('')
plt.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
plt.legend()
plt.show()