import numpy as np
import matplotlib.pyplot as plt
from itertools import islice
from scipy.special import wofz

path = 'Rayos_X\\Actividad1\\Datos_1'

def lorentzian(x,A,x0,gamma):
    return A / (1 + ((x-x0)/gamma)**2)

def voigt_profile(x, A, x0, sigma, gamma):
    z = (x - x0 + 1j * gamma) / (sigma * np.sqrt(2))
    return A * np.real(wofz(z))

def read_data(path, skip_rows = 3):
    with open(path, 'r') as file:
        lines = islice(file,skip_rows,None)
        data = [list(map(float,line.replace(',', '.').split())) for line in lines]
    return data

data = read_data(path)

x = [i[0] for i in data]
y = [i[1] for i in data]

xerr = np.full(len(x),0.1)
yerr = np.full(len(y),1)

fig, axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

axs[0].errorbar(x,y,yerr=yerr,xerr=xerr, ecolor='b', label='Datos 1', fmt='None')
axs[0].legend()
axs[0].grid()

plt.show()