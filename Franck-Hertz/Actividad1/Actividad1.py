import numpy as np
import matplotlib.pyplot as plt
import csv

from itertools import islice
from scipy.optimize import curve_fit

Spath = 'Franck-Hertz\\Actividad1\\Datos\\T_constante175'

def read_data(path, skip_rows = 3):
    with open(path, 'r') as file:
        lines = islice(file,skip_rows,None)
        data = [list(map(float,line.replace(',', '.').split())) for line in lines]
        
    col1, col2 = zip(*data)
    return list(col1), list(col2)

for i in range(2,6):
    Path = Spath + f'({i})'
    x, y = read_data(Path)
    xfil, yfil = zip(*[(xi, yi) for xi,yi in zip(x,y) if xi < 46])
    xfil, yfil = list(xfil), list(yfil)
    plt.scatter(xfil,yfil, label=f'Datos {i}',s = 5)


plt.ylabel('')
plt.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
plt.legend()
plt.show()