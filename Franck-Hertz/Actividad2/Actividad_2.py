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
    Sx = np.sum(x)
    Sy = np.sum(y)
    Sxx = np.sum(x**2)
    Sxy = np.sum(x * y)
    
    m = (n * Sxy - Sx * Sy) / (n * Sxx - Sx**2)
    b = (Sy * Sxx - Sx * Sxy) / (n * Sxx - Sx**2)
    
    y_pred = m * x + b
    residuals = y - y_pred
    Sr = np.sum(residuals**2)
    
    dm = np.sqrt((n * Sr) / ((n - 2) * (n * Sxx - Sx**2)))
    db = np.sqrt((Sr / (n * (n - 2))) * (1 + (Sx**2 / (n * Sxx - Sx**2))))
    
    return m, dm, b, db, residuals

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

marcadores = ['o', 's', 'D', '^']
colores = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 5.5), sharex=True, gridspec_kw={'hspace': 0, 'height_ratios': [3, 1]})
x_fit = np.linspace(0, 10.5, 100)

for i, (label, y) in enumerate(datos.items()):
    m, dm, b, db, residuals = ajuste_minimos_cuadrados(n, y)
    y_fit = linealfunc(x_fit, m, b)

    ax1.plot(x_fit, y_fit, color=colores[i])
    ax1.scatter(n, y, label=rf'{label}: $m={m:.2f} \pm {dm:.2f}$, $b={b:.1f} \pm {db:.1f}$',
                marker=marcadores[i], color=colores[i])
    
    ax2.scatter(n, residuals, color=colores[i], marker=marcadores[i], label=label)

ax1.set_ylabel(rf'$\Delta E_n$ (eV)', fontsize=13)
ax1.set_title('Ajuste lineal de $\Delta E_n$ vs $n$', fontsize=14)
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.legend(fontsize=8)

ax2.axhline(0, color='black', linestyle='--', linewidth=1)
ax2.set_xlabel(r'$n$', fontsize=13)
ax2.set_ylabel('Residuales', fontsize=11)
ax2.grid(True, linestyle='--', alpha=0.6)

plt.savefig('Franck-Hertz/Actividad2/ajusteminimos.png', dpi=300, bbox_inches='tight')