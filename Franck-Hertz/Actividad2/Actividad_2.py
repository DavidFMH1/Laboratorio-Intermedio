import numpy as np
import matplotlib.pyplot as plt
import csv

from itertools import islice
from scipy.signal import find_peaks
from scipy.optimize import curve_fit
from matplotlib.lines import Line2D

Spath = 'Franck-Hertz\\Actividad2\\Datos\\Tconstante_'

def ajuste_minimos_cuadrados(x, y):
    n = len(x)
    
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_x2 = np.sum(x**2)
    sum_xy = np.sum(x * y)
    
    m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x**2)
    
    b = (sum_y * sum_x2 - sum_x * sum_xy) / (n * sum_x2 - sum_x**2)
    
    y_est = m * x + b
    residuals = y - y_est
    sum_res2 = np.sum(residuals**2)
    
    delta_m = np.sqrt((n * sum_res2) / ((n - 2) * (n * sum_x2 - sum_x**2)))
    
    delta_b = np.sqrt((1 + (sum_x**2) / (n * sum_x2 - sum_x**2)) * sum_res2 / (n * (n - 2)))
    
    return m, delta_m, b, delta_b

def linealfunc(x,a,b):
    return a*x + b

def read_data(path, skip_rows = 3):
    with open(path, 'r') as file:
        lines = islice(file,skip_rows,None)
        data = [list(map(float,line.replace(',', '.').split())) for line in lines]
        
    col1, col2 = zip(*[(row[0], row[1]) for row in data])
    return np.array(list(col1)), np.array(list(col2))

plt.figure(figsize=(7,5.5))

han = []

Sm = []

for i in range(0,4):
    Path = Spath + f'{180+i*5}'
    x, y = read_data(Path)
    xfil, yfil = zip(*[(xi, yi) for xi,yi in zip(x,y) if yi < 47])
    xfil, yfil = np.array(list(xfil)), np.array(list(yfil))
    mind, _ = find_peaks(-yfil, distance=10, prominence=0.2)
    mind = np.array(mind)
    mins = xfil[mind]
    Sm.append(mins)
    for min in mins:
        plt.vlines(x=min, ymin=0, ymax=yfil[xfil == min], color='black', linestyle='--', linewidth=0.6)
    scatter = plt.scatter(xfil,yfil, label=f'Datos {180+i*5}',s = 5)
    han.append(scatter)

linea_punteada = Line2D([0], [0], color='black', linestyle='--', linewidth=1, label='Mínimos locales')

han.insert(0, linea_punteada)

plt.legend(handles=han, scatterpoints=1, markerscale=5)

plt.title('Corriente en función del potencial')
plt.xlabel(r'$U_{1}$  $(V)$', fontsize=15)
plt.ylabel(r'$I_{A}$  $(nA)$', fontsize=15)
plt.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
plt.savefig('Franck-Hertz/Actividad2/Datos_T_variable.png', dpi=300, bbox_inches='tight')

plt.close()

n = np.array([5, 6, 7, 8, 9, 10])
datos = {
    '195°C': np.array([5.06, 4.35, 4.90, 4.91, 4.81, 5.11]),
    '190°C': np.array([4.60, 4.81, 4.95, 5.01, 5.10, 5.03]),
    '185°C': np.array([4.67, 4.91, 4.93, 5.00, 5.16, 5.00]),
    '180°C': np.array([4.67, 4.91, 4.95, 4.96, 5.02, 5.06])
}

plt.figure(figsize=(7, 5.5))

for label, y in datos.items():
    m, sigm, b, sifgb = ajuste_minimos_cuadrados(n,y)
    _x = np.linspace(0,11,3)
    _y = linealfunc(_x,m,b)
    plt.plot(_x,_y)
    plt.scatter(n, y, marker='o', label=f'T = {label}')
    print(m,b)

plt.xlabel(r'$n$', fontsize=14)
plt.ylabel(r'$\Delta E_n$ (eV)', fontsize=14)
plt.title('Energía vs número cuántico n', fontsize=15)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.show()