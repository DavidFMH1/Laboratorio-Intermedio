import matplotlib.pyplot as plt
import numpy as np

from itertools import islice
from scipy.optimize import curve_fit

def format_number(num, precision=2):
    if abs(num) < 1e-2 or abs(num) > 1e3: 
        return f'{num:.{precision}e}'
    else:  
        return f'{num:.{precision}f}'

d = 2.014e-10

Aldens = 2.7
Zndens = 7.14

NameB = np.array(['Nofiltro'])
NamesA = np.array(['aluminio002mm','aluminio004mm','aluminio008mm','aluminio01mm'])
NamesB = np.array(['Zinc0025mm','Zinc005mm','Zinc0075mm','Zinc01mm'])
thiknA = np.array([0.02, 0.04, 0.08, 0.1])
thiknB = np.array([0.025, 0.05, 0.075, 0.1])

PPath = 'Rayos_X\\Actividad2\\'

def Lineal_reg(x,A):
    return A*x

def lineal_regb(x,a,b):
    return a*x + b

def cuadratic_reg(x,a,b,c):
    return a*x**2 + b*x + c

def cub_reg(x,a,b,c,d):
    return a*x**3 + b*x**2 + c*x +d

def cuatro_reg(x,a,b,c,d,e):
    return a*x*4 + b*x**3 + c*x**2 + d*x + e

def cinco_reg(x,a,b,c,d,e,f):
    return a*x**5 + b*x**4 + c*x**3 + d*x**2 + e*x + f

def seis_reg(x,a,b,c,d,e,f,g):
    return a*x**6 + b*x**5 + c*x**4 + d*x**3 + e*x**2 + f*x + g
 
def read_data(path, Names, thikn, skip_rows=3, BName = NameB):
    
    DataA = []
    
    with open(path + BName[0], 'r') as fileb:
        lines = islice(fileb, skip_rows, None)
        DataB = [list(map(float,line.replace(',', '.').split())) for line in lines]
    
    i = 0
    
    angles = {}
    
    while i < len(Names):
        CPath = path + Names[i]
        with open(CPath, 'r') as file:
            lines = islice(file, skip_rows, None)
            j = 0
            for line in lines:
                D = list(map(float,line.replace(',','.').split()))
                if not(str(D[0]) in angles):
                    angles[str(D[0])] = np.array([thikn[i], D[1]/DataB[j][1]]),    
                else:
                    angles[str(D[0])] = np.append(angles[str(D[0])],[[thikn[i], D[1]/DataB[j][1]]], axis=0)
                
                j += 1
        i += 1
    
    return angles

Datos1, Datos2 = read_data(PPath,NamesA,thiknA), read_data(PPath,NamesB,thiknB)

fig, axs = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

fig.suptitle('Intensidad noralizada vs Espesor')

colores = np.array(['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta', 'yellow'])
marcadores = np.array(['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'X', 'h'])

j = 0

lambsAl = np.array([])
muAl = np.array([])
sigmuAl = np.array([])

for i in Datos1:
    
    lamb = 2*d*np.sin(np.radians(float(i)))*(10**9)
    lambsAl = np.append(lambsAl,float(lamb))
    lamb = format_number(lamb, 4)
    
    x = [Datos1[i][k][0] for k in range(len(Datos1[i]))]
    y = [np.log(Datos1[i][k][1]) for k in range(len(Datos1[i]))]
    
    param, cov = curve_fit(Lineal_reg, x, y)
    
    muAl = np.append(muAl, float(-param[0]))
    
    covn = np.sqrt(np.diagonal(cov))
    sigmuAl  = np.append(sigmuAl, float(covn[0]))
    covn = format_number(covn[0],0)
    
    _x = np.linspace(x[0],x[-1],200)
    _y = Lineal_reg(_x,param)
    
    res = (y - Lineal_reg(x, param))/np.std(y)
    
    param = format_number(-param[0], 0)
    
    axs[0].scatter(x,y, color=colores[j], marker = marcadores[j], label=f'{lamb:.4}nm ; '+r'$\mu = $' + f'{param} '+ r'$\pm$'+ f' {covn}')
    axs[0].set_ylabel('Intensidad normalizada ' + r'$\ln(\frac{I}{I_{0}})$')
    axs[0].legend(fontsize=7)
    axs[0].plot(_x,_y,color=colores[j])
    
    axs[1].scatter(x, res, color=colores[j], marker = marcadores[j])
    axs[1].axhline(0, color='black', linestyle='--')
    axs[1].set_xlabel('Espesor del material (mm)')
    axs[1].set_ylabel('Residuales\n normalizados')
    
    j += 1

for ax in axs:
    ax.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
        
'''plt.savefig(r'Rayos_X\\Actividad2\\IntensidadEspesorAl.png', format='png', dpi=300)'''

plt.close()

fig, axs = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

fig.suptitle('Intensidad noralizada vs Espesor')

j = 0

lambsZn = np.array([])
muZn = np.array([])
sigmuZn = np.array([])

for i in Datos1:
    
    lamb = 2*d*np.sin(np.radians(float(i)))*(10**9)
    lambsZn = np.append(lambsZn,float(lamb))
    lamb = format_number(lamb, 4)
    
    x = [Datos1[i][k][0] for k in range(len(Datos1[i]))]
    y = [np.log(Datos1[i][k][1]) for k in range(len(Datos1[i]))]
    
    param, cov = curve_fit(Lineal_reg, x, y)
    
    muZn = np.append(muZn, float(-param[0]))
    
    covn = np.sqrt(np.diagonal(cov))
    sigmuZn  = np.append(sigmuZn, float(covn[0]))
    covn = format_number(covn[0],0)
    
    _x = np.linspace(x[0],x[-1],200)
    _y = Lineal_reg(_x,param)
    
    res = (y - Lineal_reg(x, param))/np.std(y)
    
    param = format_number(-param[0], 0)
    
    axs[0].scatter(x,y, color=colores[j], marker = marcadores[j], label=f'{lamb:.4}nm ; '+r'$\mu = $' + f'{param} '+ r'$\pm$'+ f' {covn}')
    axs[0].set_ylabel('Intensidad normalizada ' + r'$\ln(\frac{I}{I_{0}})$')
    axs[0].legend(fontsize=7)
    axs[0].plot(_x,_y,color=colores[j])
    
    axs[1].scatter(x, res, color=colores[j], marker = marcadores[j])
    axs[1].axhline(0, color='black', linestyle='--')
    axs[1].set_xlabel('Espesor del material (mm)')
    axs[1].set_ylabel('Residuales\n normalizados')
    
    j += 1

for ax in axs:
    ax.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
    
'''plt.savefig(r'Rayos_X\\Actividad2\\IntensidadEspesorZn.png', format='png', dpi=300)'''

plt.close()

muAlY = (muAl/Aldens)*10
muZnY = (muZn/Zndens)*10

lambAlX = lambsAl**3
lambZnX = lambsZn**3

sigmuAlN = (1/Aldens)*sigmuAl
sigmuZnN = (1/Zndens)*sigmuZn

fig, axs = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

fig.suptitle('Coeficiente de absorción lineal vs longitud de onda')

axs[0].errorbar(lambAlX,muAlY, yerr = sigmuAl, fmt='o', label='Datos Al', capsize = 3)
axs[0].errorbar(lambZnX,muZnY, yerr = sigmuZn, fmt='o', label='Datos Zn', capsize = 3)
axs[0].set_ylabel(r"$\frac{\mu}{\rho} \quad \frac{\mathrm{cm}^{2}}{\mathrm{g}}$")

param, cov  = curve_fit(cub_reg, lambAlX, muAlY, sigma=sigmuAlN, absolute_sigma=True)
param2, cov2 = curve_fit(cub_reg, lambZnX, muZnY, sigma=sigmuZnN, absolute_sigma=True)

_x = np.linspace(np.min(lambAlX), np.max(lambAlX),200)
_y = cub_reg(_x,*param)

_x2 = np.linspace(np.min(lambZnX), np.max(lambZnX),200)
_y2 = cub_reg(_x, *param2)

axs[0].plot(_x,_y, label='Ajuste cubico', color='red', linestyle='solid')
axs[0].plot(_x2,_y2, label='Ajuste cubico', color='red', linestyle='dashdot')
axs[0].legend()

res = (muAlY - cub_reg(lambAlX, *param))/sigmuAlN
res2 = (muZnY - cub_reg(lambZnX, *param2))/sigmuZnN

axs[1].scatter(lambAlX, res, color='black', marker = 'x', label='residuales Al')
axs[1].scatter(lambZnX, res2, color='black', marker = 'p', label='residuales Zn')
axs[1].axhline(0, color='black', linestyle='--')
axs[1].set_xlabel('longitud de onda al cubo (nm^3)')
axs[1].set_ylabel('Residuales\n normalizados')

axs[1].legend()

'''plt.savefig(r'Rayos_X\\Actividad2\\coeficientedeatenuacni.png', format='png', dpi=300)'''