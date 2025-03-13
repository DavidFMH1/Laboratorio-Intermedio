import numpy as np
import matplotlib.pyplot as plt

from itertools import islice

d = 2.014e-10

pathTc = 'Rayos_X\\Actividad3\\Datos tenscte'

colores = np.array(['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta'])
marcadores = np.array(['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'X'])

def lorentzian(x,A,x0,gamma):
    return A / (1 + ((x-x0)/gamma)**2)

def read_dataTc(path):
    
    with open(path, 'r') as file:
        lineas = islice(file, 3, None)
        Data = np.array([list(map(float, line.replace(',', '.').split())) for line in lineas])
    
    return Data.T

datos = read_dataTc(pathTc)

plt.figure(figsize=(15,7.5))
plt.suptitle('Intensidad vs Longitud de onda')

for i in range(1,11):
    k = 11
    lamb = 2*d*np.sin(np.radians(datos[0]))
    j = datos[i]
    siglam = 2*d*np.cos(np.radians(datos[0]))*np.radians(0.1)
    sigmi = np.full(len(j),1)
    
    plt.errorbar(lamb,j,yerr=sigmi, xerr=siglam, fmt='o', color=colores[i-1], label=f'{k+2.5*(i-1)} V')

plt.legend(fontsize=10)
plt.close()

for i in range(1,11):
    Tpath = f'Rayos_X\\Actividad3\\corrcte{i:02d}ma'
    
    datos = read_dataTc(Tpath)
    