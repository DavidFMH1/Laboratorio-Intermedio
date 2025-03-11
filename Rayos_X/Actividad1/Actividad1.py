import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ti

from itertools import islice
from scipy.special import wofz
from scipy.optimize import curve_fit

path = 'Rayos_X\\Actividad1\\Datos_1'

d = 2.014e-10

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

#Este x es en angulo
xv = [i[0] for i in data if 41.7 <= i[0] <= 42.1]
xl = [i[0] for i in data if 41.6 <= i[0] <= 42.2]

#Nuevo x en longitud de onda
xn = [2*d*np.sin(np.radians(k)) for k in xv]
xnl = [2*d*np.sin(np.radians(k)) for k in xl]

y = [i[1] for i in data if 41.7 <= i[0] <= 42.1 ]
yl = [i[1] for i in data if 41.6 <= i[0] <= 42.2]

xerr = np.full(len(xv),0.1)

xerrn = [np.abs(d*np.cos(np.radians(k))*np.radians(0.1)) for k in xv]
xerrnl = [np.abs(d*np.cos(np.radians(k))*np.radians(0.1)) for k in xl]

yerr = np.full(len(y),1)
yerrl = np.full(len(yl),1)

guess = [max(yl),2.68e-10,(max(xnl)-min(xnl))/10]

#lorentzian

param, cov = curve_fit(lorentzian,xnl,yl,p0=guess,sigma=yerrl,absolute_sigma=True)

covn = np.sqrt(np.diagonal(cov))

x_ = np.linspace(xnl[0]-xerrnl[0],xnl[-1]+xerrnl[-1],200)
y_ = lorentzian(x_, param[0], param[1], param[2])

#Voigt profile

guessv = [max(y),2.68e-10,(max(xn)-min(xn))/10,(max(xn)-min(xn))/20]
guessv2 = [param[0], param[1], 1, param[2]]
guessv3 = [max(y),2.68e-10,(max(xn)-min(xn)),(max(xn)-min(xn))/20]

paramv, covv = curve_fit(voigt_profile,xn,y,p0=guessv2, sigma=yerr, absolute_sigma=True)

covvn = np.sqrt(np.diagonal(covv))

xv_ = np.linspace(xn[0]-xerrn[0],xn[-1]+xerrn[-1],200)
yv_ = voigt_profile(x_,*paramv)


fig, axs = plt.subplots(2, 3, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'width_ratios': [1,0.001,1], 'hspace': 0, 'wspace': 0.15})

fig.suptitle('Intensidad vs Longitud de onda', fontsize=20)

axs[0,1].axis('off')
axs[1,1].axis('off')

#axs[0,2].scatter(xn,y)

#Ajuste lorentziano

x0 = param[1]
error = covn[1]

exponente = np.floor(np.log10(x0))  # Encuentra el exponente más grande
x0_mant = x0 / 10**exponente
error_mant = error / 10**exponente

axs[0, 0].errorbar(xnl, yl, xerr=xerrnl, yerr=yerrl, fmt='o', label='Pico #4', capsize=3)
axs[0, 0].axvline(param[1],color='g', linestyle='--', label=f"$x_0 = ({x0_mant:.5f} \\pm {error_mant:.5f}) \\times 10^{{{int(exponente)}}}$")
axs[0, 0].yaxis.set_major_formatter(ti.ScalarFormatter(useMathText=True))
axs[0, 0].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
axs[0, 0].yaxis.get_offset_text().set_fontsize(8) 
axs[0, 0].plot(x_, y_, label='Ajuste Lonrentziano', color='red')
axs[0, 0].set_ylabel('Intensidad (imp/s)')
axs[0, 0].legend(fontsize=8)

res = yl - lorentzian(xnl,*param) / yerrl

axs[1, 0].scatter(xnl, res, color='black', marker='x')
axs[1, 0].axhline(0, color='black', linestyle='--')
axs[1, 0].yaxis.set_major_formatter(ti.ScalarFormatter(useMathText=True))
axs[1, 0].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
axs[1, 0].yaxis.get_offset_text().set_fontsize(8)
axs[1, 0].set_xlabel('Longitud de onda (m)')
axs[1, 0].set_ylabel('Residuales\n normalizados')

#Perfil de Voigt

x0v = paramv[1]
errorv = covvn[1]

exponentev = np.floor(np.log10(x0v)) 
x0v_mant = x0v / 10**exponentev
errorv_mant = errorv / 10**exponentev

axs[0, 2].errorbar(xn, y, xerr=xerrn, yerr=yerr, fmt='o', label='Pico #4', capsize=3)


axs[0, 2].axvline(paramv[1],color='g', linestyle='--', label=f"$x_0 = ({x0v_mant:.6f} \\pm {errorv_mant:.6f}) \\times 10^{{{int(exponentev)}}}$")
axs[0, 2].yaxis.set_major_formatter(ti.ScalarFormatter(useMathText=True))
axs[0, 2].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
axs[0, 2].yaxis.get_offset_text().set_fontsize(8) 
axs[0, 2].plot(xv_, yv_, label='Perfil de Voigt', color='red')
axs[0, 2].set_ylabel('Intensidad (imp/s)')
axs[0, 2].legend(fontsize=8)

resv = y - voigt_profile(xn,*paramv) / yerr

axs[1, 2].scatter(xn, resv, color='black', marker='x')
axs[1, 2].axhline(0, color='black', linestyle='--')
axs[1, 2].yaxis.set_major_formatter(ti.ScalarFormatter(useMathText=True))
axs[1, 2].ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
axs[1, 2].yaxis.get_offset_text().set_fontsize(8) 
axs[1, 2].set_xlabel('Longitud de onda (m)')
axs[1, 2].set_ylabel('Residuales\n normalizados')

for row in axs:
    for ax in row:
        ax.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)

plt.show()

'''plt.savefig(r'Rayos_X\\Actividad1\\GraficaAv1pic4.png', format='png', dpi=300)'''