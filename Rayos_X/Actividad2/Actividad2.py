import matplotlib.pyplot as plt
import numpy as np

from itertools import islice
from scipy.optimize import curve_fit

d = 2.014e-10

NameB = np.array(['Nofiltro'])
NamesA = np.array(['aluminio002mm','aluminio004mm','aluminio008mm','aluminio01mm'])
NamesB = np.array(['Zinc0025mm','Zinc005mm','Zinc0075mm','Zinc01mm'])
thiknA = np.array([0.02, 0.04, 0.08, 0.1])
thiknB = np.array([0.025, 0.05, 0.075, 0.1])

PPath = 'Rayos_X\\Actividad2\\'

def Lineal_reg(x,A):
    return A*x
 
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

Datos = read_data(PPath,NamesA,thiknA)

fig, axs = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

fig.suptitle('Intensidad noralizada vs Espesor')

colores = np.array(['blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan', 'magenta', 'yellow'])
marcadores = np.array(['o', 's', 'D', '^', 'v', '<', '>', 'p', '*', 'X', 'h'])

j = 0

for i in Datos:
    
    lamb = 2*d*np.sin(np.radians(float(i)))*(10**9)
    
    x = [Datos[i][k][0] for k in range(len(Datos[i]))]
    y = [np.log(Datos[i][k][1]) for k in range(len(Datos[i]))]
    
    param, cov = curve_fit(Lineal_reg, x, y)
    
    _x = np.linspace(x[0],x[-1],200)
    _y = Lineal_reg(_x,param)
    
    res = (y - Lineal_reg(x, param))/np.std(y)
    
    axs[0].scatter(x,y, color=colores[j], marker = marcadores[j], label=f'{lamb:.3}nm ; '+r'$\mu = $' + f'{-param[0]:.3}')
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
        
plt.savefig(r'Rayos_X\\Actividad2\\IntensidadEspesorAl.png', format='png', dpi=300)