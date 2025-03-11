import matplotlib.pyplot as plt
import numpy as np

from itertools import islice
from scipy.optimize import curve_fit

NameB = np.array(['Nofiltro'])
NamesA = np.array(['aluminio002mm','aluminio004mm','aluminio008mm','aluminio01mm'])
NamesB = np.array(['Zinc0025mm','Zinc005mm','Zinc0075mm','Zinc01mm'])
thiknA = np.array([0.02, 0.04, 0.08, 0.1])
thiknB = np.array([0.025, 0.075, 0.5, 0.1])

PPath = 'Rayos_X\\Actividad2\\'

def Lineal_reg(x,A,B):
    return A*x + B
 
def read_data(path, Names, skip_rows=3, num_data=0, BName = NameB):
    
    DataA = []
    
    with open(path + BName[0], 'r') as fileb:
        lines = islice(fileb, skip_rows, None)
        DataB = [list(map(float,line.replace(',', '.').split())) for line in lines]
    
    j = 0
    
    sigI = np.array([])
    
    for name in Names:
        CPath = path + name
        with open(CPath, 'r') as file:
            lines = islice(file, skip_rows, None)
            Data = [list(map(float,line.replace(',', '.').split())) for line in lines]
            
            DataA.append(Data[num_data])
            
            DataA[j][1] = DataA[j][1] / DataB[num_data][1]
            
            sigI = np.append(sigI, np.sqrt((1/DataB[num_data][1])**2 + (DataA[j][1]/DataB[num_data][1])**2))
            
        j+=1
    
    return DataA, sigI

i = 0

fig, axs = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

fig.suptitle('Intensidad noralizada vs Espesor')

colores = np.array(["red", "blue", "green", "purple"])


while i < len(NamesA):
    
    data, sigy = read_data(PPath,NamesA,num_data=i)
    
    y = [np.log(i[1]) for i in data]
    x = thiknA
    axs[0].errorbar(x,y,yerr=sigy, fmt='s', color=colores[i], label = NamesA[i])
    axs[0].set_ylabel('Intensidad normalizada '+r'$\frac{I}{I_{0}}$')
    
    param, cov = curve_fit(Lineal_reg,x,y,sigma=sigy, absolute_sigma=True)
    
    _x = np.linspace(x[0],x[-1],200)
    _y = Lineal_reg(_x, *param)
    
    res = (y - Lineal_reg(x, *param)) / sigy
    
    axs[0].plot(_x,_y, color=colores[i])
    axs[0].legend()
    
    axs[1].scatter(x,res, color=colores[i], marker='x')
    axs[1].axhline(0, color='black', linestyle = '--')
    axs[1].set_ylabel('Residuales normalizados')
    axs[1].set_xlabel('Espesor material (mm)')
    
    for ax in axs:
        ax.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)
    i += 1
    
plt.savefig(r'Rayos_X\\Actividad2\\IntensidadEspesor.png', format='png', dpi=300)