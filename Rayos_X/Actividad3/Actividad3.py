import numpy as np
import matplotlib.pyplot as plt

from itertools import islice
from scipy.optimize import curve_fit

d = 2.014e-10
pk = 9.979

pathTc = 'Rayos_X\\Actividad3\\Datos tenscte'

colores = np.array(['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta'])
marcadores = np.array(['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'X'])

def lorentzian(x,A,x0,gamma):
    return A / (1 + ((x-x0)/gamma)**2)

def lineal_reg(x,a):
    return a*x

def weird_reg(x,A):
    return A*(x-pk)**(3/2)

def read_dataTc(path):
    
    with open(path, 'r') as file:
        lineas = islice(file, 3, None)
        Data = np.array([list(map(float, line.replace(',', '.').split())) for line in lineas])
    
    return Data.T

datos = read_dataTc(pathTc)

plt.figure(figsize=(15,7.5))
plt.suptitle('Intensidad vs Longitud de onda con corriente cte')

IKb = np.array([])
sigIkb = np.array([])
potencialb = np.array([])

for i in range(1,11):
    k = 11
    mask = (datos[0] <= 18.8) & (datos[0] >= 18.3)
    lamb = 2*d*np.sin(np.radians(datos[0][mask]))
    j = datos[i][mask]
    siglam = 2*d*np.cos(np.radians(datos[0][mask]))*np.radians(0.1)
    sigmi = np.full(len(j),1)
    
    guess = [max(j),1.28e-10,(max(lamb)-min(lamb))/10]
    
    param, cov = curve_fit(lorentzian, lamb, j, p0=guess, sigma=sigmi, absolute_sigma=True)
    
    cov = np.sqrt(np.diagonal(cov))
    
    _x = np.linspace(np.min(lamb), np.max(lamb), 200)
    _y = lorentzian(_x, *param)
    
    IKb = np.append(IKb, param[0])
    sigIkb = np.append(sigIkb, cov[0])
    potencialb = np.append(potencialb, k+2.5*(i-1))
    
    plt.errorbar(lamb,j,yerr=sigmi, xerr=siglam, fmt='o', color=colores[i-1], label=f'{k+2.5*(i-1)} V')
    plt.plot(_x, _y, color=colores[i-1])

plt.legend(fontsize=10)
plt.close()

IKa = np.array([])
sigIka = np.array([])
potenciala = np.array([])

for i in range(1,11):
    k = 11
    mask = (datos[0] <= 21.2) & (datos[0] >= 20.5)
    lamb = 2*d*np.sin(np.radians(datos[0][mask]))
    j = datos[i][mask]
    siglam = 2*d*np.cos(np.radians(datos[0][mask]))*np.radians(0.1)
    sigmi = np.full(len(j),1)
    
    guess = [max(j),1.42e-10,(max(lamb)-min(lamb))/10]
    
    param, cov = curve_fit(lorentzian, lamb, j, p0=guess, sigma=sigmi, absolute_sigma=True)
    
    cov = np.sqrt(np.diagonal(cov))
    
    _x = np.linspace(np.min(lamb), np.max(lamb), 200)
    _y = lorentzian(_x, *param)
    
    IKa = np.append(IKa, param[0])
    sigIka = np.append(sigIka, cov[0])
    potenciala = np.append(potenciala, k+2.5*(i-1))
    
    plt.errorbar(lamb,j,yerr=sigmi, xerr=siglam, fmt='o', color=colores[i-1], label=f'{k+2.5*(i-1)} V')
    plt.plot(_x, _y, color=colores[i-1])
    
plt.legend(fontsize=10)
plt.close()


fig, axs = plt.subplots(2, 2, figsize=(15, 10), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

Urarob = np.power((potencialb - pk), 3/2)
Uraroa = np.power((potenciala - pk), 3/2)

param1, cov1 = curve_fit(weird_reg, potenciala, IKa, sigma= sigIka, absolute_sigma=True)
param2, cov2 = curve_fit(weird_reg, potencialb, IKb, sigma= sigIkb, absolute_sigma=True)
param3, cov3 = curve_fit(lineal_reg, Uraroa, IKa, sigma= sigIka, absolute_sigma=True)
param4, cov4 = curve_fit(lineal_reg, Urarob, IKb, sigma= sigIkb, absolute_sigma=True)

_x1 = np.linspace(np.min(potenciala), np.max(potenciala), 200)
_x2 = np.linspace(np.min(potencialb), np.max(potencialb), 200)
_x3 = np.linspace(np.min(Uraroa), np.max(Uraroa), 200)
_x4 = np.linspace(np.min(Urarob), np.max(Urarob), 200)

_y1 = weird_reg(_x1,*param1)
_y2 = weird_reg(_x2,*param2)
_y3 = lineal_reg(_x3,*param3)
_y4 = lineal_reg(_x4,*param4)

res1 = (IKa - weird_reg(potenciala,param1[0]))
res2 = (IKb - weird_reg(potencialb,param2[0]))
res3 = (IKa - lineal_reg(Uraroa,param3[0]))
res4 = (IKb - lineal_reg(Urarob,param4[0]))

axs[0, 0].errorbar(potencialb, IKb, yerr=sigIkb, fmt='o', label=r'$K_{\beta} \quad en \quad función \quad de \quad U_{K}$')
axs[0, 0].plot(_x2,_y2, color='red')
axs[0, 0].errorbar(potenciala, IKa, yerr=sigIka, fmt='o', label=r'$K_{\alpha} \quad en \quad función \quad de \quad U_{K}$')
axs[0, 0].plot(_x1,_y1, color='red')

axs[0, 0].set_ylabel('K (m)')
axs[0, 0].set_title(r'Gráfico en función de $U_K$')
axs[0, 0].legend(fontsize=12)
axs[0, 0].grid()

axs[0, 1].errorbar(Urarob, IKb, yerr=100*sigIkb, ecolor=colores[1], fmt='None', label=r'$K_{\beta} \quad en \quad función \quad de \quad (U_{A} - U_{K})^{\frac{3}{2}}$', capsize=10e10, capthick=0)
axs[0, 1].plot(_x4,_y4, color='black')
axs[0, 1].errorbar(Uraroa, IKa, yerr=100*sigIkb, ecolor=colores[2], fmt='None', label=r'$K_{\alpha} \quad en \quad función \quad de \quad (U_{A} - U_{K})^{\frac{3}{2}}$', capsize=10, capthick = 0)
axs[0, 1].plot(_x3,_y3, color='black')

axs[0, 1].set_title(r'Gráfico en función de $(U_A - U_K)^{3/2}$')
axs[0, 1].legend(fontsize=12)
axs[0, 1].grid()

axs[1, 0].scatter(potencialb, res2, label=r'Residuales $K_{\beta}$')
axs[1, 0].scatter(potenciala, res1, label=r'Residuales $K_{\alpha}$')
axs[1, 0].axhline(0, color='black', linestyle='--', linewidth=1)
axs[1, 0].set_xlabel('Potencial (mA)')
axs[1, 0].set_ylabel('Residuales\nnormalizados')
axs[1, 0].legend()
axs[1, 0].grid()

axs[1, 1].scatter(Urarob, res4, label=r'Residuales $K_{\beta}$')
axs[1, 1].scatter(Uraroa, res3, label=r'Residuales $K_{\alpha}$')
axs[1, 1].axhline(0, color='black', linestyle='--', linewidth=1)
axs[1, 1].set_xlabel(r'$(U_A - U_K)^{3/2}$')
axs[1, 1].set_ylabel('Residuales\nnormalizados')
axs[1, 1].legend()
axs[1, 1].grid()

plt.show()

'''plt.figure(figsize=(15,7.5))
plt.suptitle('Intensidad vs Longitud de onda, con tension cte')

corriente = np.array([])
x0 = np.array([])
xosig = np.array([])

for i in range(1,11):
    
    k = 0.1
    
    Tpath = f'Rayos_X\\Actividad3\\corrcte{i:02d}ma'
    
    datos = read_dataTc(Tpath)
    mask = (datos[0] <= 42) & (datos[0] >= 41.2)
    datosx = datos[0][mask]
    j = datos[1][mask]
    
    lamb = 2*d*np.sin(np.radians(datosx))
    siglam = 2*d*np.cos(np.radians(datosx))*np.radians(0.1)
    sigmi = np.full(len(j),1)
    
    guess = [max(j),2.67e-10,(max(lamb)-min(lamb))/10]
    
    param, cov = curve_fit(lorentzian, lamb, j, p0=guess, sigma=sigmi, absolute_sigma=True)
    
    cov = np.sqrt(np.diagonal(cov))
    
    _x = np.linspace(np.min(lamb), np.max(lamb), 200)
    _y = lorentzian(_x, *param)
    
    plt.errorbar(lamb,j,yerr=sigmi, xerr=siglam, fmt=marcadores[i-1], color=colores[i-1], label=f'{k+0.1*(i-1):.1f} ma' + ' y ajuste lorentziano')
    plt.plot(_x, _y, color=colores[i-1])
    
    corriente = np.append(corriente, k+0.1*(i-1))
    x0 = np.append(x0, param[1])
    xosig = np.append(xosig, cov[1])
    
    #print(f'valor de corriente {k+0.1*(i-1):.1f} ma, x0 = {param[1]:.5}' + r'$\pm$' + f'{cov[1]:.5}')

plt.close()

corrientea = np.array([])
x0a = np.array([])
xoasig = np.array([])

for i in range(1,11):
    
    k = 0.1
    
    Tpath = f'Rayos_X\\Actividad3\\corrcte{i:02d}ma'
    
    datos = read_dataTc(Tpath)
    mask = (datos[0] <= 37.5) & (datos[0] >= 36.4)
    datosx = datos[0][mask]
    j = datos[1][mask]
    
    lamb = 2*d*np.sin(np.radians(datosx))
    siglam = 2*d*np.cos(np.radians(datosx))*np.radians(0.1)
    sigmi = np.full(len(j),1)
    
    guess = [max(j),1.42e-10,(max(lamb)-min(lamb))/10]
    
    param, cov = curve_fit(lorentzian, lamb, j, p0=guess, sigma=sigmi, absolute_sigma=True)
    
    cov = np.sqrt(np.diagonal(cov))
    
    _x = np.linspace(np.min(lamb), np.max(lamb), 200)
    _y = lorentzian(_x, *param)
    
    plt.errorbar(lamb,j,yerr=sigmi, xerr=siglam, fmt=marcadores[i-1], color=colores[i-1], label=f'{k+0.1*(i-1):.1f} ma' + ' y ajuste lorentziano')
    plt.plot(_x, _y, color=colores[i-1])
    
    corrientea = np.append(corrientea, k+0.1*(i-1))
    x0a = np.append(x0a, param[1])
    xoasig = np.append(xoasig, cov[1])

plt.legend(fontsize=10)
plt.close()

plt.figure(figsize=(15,7.5))
plt.suptitle(f'K en función de la corriente')

plt.errorbar(corrientea,x0a,yerr=xoasig, fmt='o', label=r'$K_{\beta}$')
plt.errorbar(corriente, x0, yerr=xosig, fmt='o', label=r'$K_{\alpha}$')
plt.ylim(min(x0a) * 0.93, max(x0) * 1.07)
plt.ylabel('K (m)')
plt.xlabel('Corriente (mA)')
plt.grid()
plt.legend(fontsize=15)'''

'''plt.savefig(r'Rayos_X\\Actividad3\\GraficaKvsIVcte.png', format='png', dpi=300)'''