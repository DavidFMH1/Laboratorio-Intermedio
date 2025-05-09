import numpy as np
import matplotlib.pyplot as plt
import csv

from scipy.optimize import curve_fit

path = 'Torque_magnetico\\Actividad1\\actividad_1.csv'

def Weighted_least_squares(x,y,dy):
    
    W = 1/dy**2
    
    s1 = np.sum(W)
    s2 = np.sum(W*x)
    s3 = np.sum(W*y)
    s4 = np.sum(W*x**2)
    s5 = np.sum(W*x*y)
    
    Delt = s1*s4 - s2**2
    
    c = (s4*s3-s2*s5)/Delt
    m = (s1*s5-s2*s3)/Delt
    
    sigc = np.sqrt(s4/Delt)
    sigm = np.sqrt(s1/Delt)
    
    return c, sigc, m, sigm

def linealfunc(x,a,b):
    return a*x + b

def read_data(path):
    
    col1 = np.array([])
    col2 = np.array([])
    
    with open(path, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for line in reader:
            if len(line) >= 2:
                col1 = np.append(col1,float(line[0]))
                col2 = np.append(col2,float(line[1]))
        
    return col1, col2

def convert_curr_to_Mfield(currlist):
    return 1.36e-3*currlist

Rad, Curr = read_data(path)
MField = convert_curr_to_Mfield(Curr)

Rm = Rad/100

rmg = Rm*0.0015*9.78

sigrmg = np.sqrt(5.38e-13+(Rm*0.0015*0.0001)**2)
sigB = np.full(len(MField),6.8e-5)

c, sc, m, sm = Weighted_least_squares(MField,rmg,sigrmg)

_x = np.linspace(np.min(MField)-6.8e-5,np.max(MField)+6.8e-5,2)
_y = linealfunc(_x,m,c)

#residuales

res = (rmg-linealfunc(MField,m,c))/(sigrmg*20)

fig, axs = plt.subplots(2, 1, figsize=(7,5.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0, 'wspace': 0.15})

fig.suptitle('Torque mecánico en función del campo magnético', fontsize=12)

mt = fr'$m = {m:.4f} \pm {sm:.4f}$'
ct = fr'$b = ({c*10e5:.0f} \pm {sc*10e5:.0f})\times 10^{{-5}}$'

axs[0].errorbar(MField*1000, rmg*1000, yerr=20000*sigrmg, xerr=sigB*1000, fmt='o', label='Datos',color='black', capsize=3, elinewidth=1.5, markersize=6)
axs[0].plot(_x*1000,_y*1000,color='red', label=f'Regresión Lineal \n {mt} \n {ct}')
axs[0].set_ylabel(r'Rmg $10^{-3} (Nm)$', fontsize =14)
axs[0].legend()

axs[1].scatter(MField*1000, res, color='black', marker='x')
axs[1].axhline(0, color='black', linestyle='--')
axs[1].set_ylabel('Residuales\n normalizados', fontsize = 12)
axs[1].set_xlabel('B (mT)', fontsize=12)

for row in axs:
    row.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)

plt.savefig(r'Torque_magnetico\\Actividad1\\rmgvscampomagnetic.png', format='png', dpi=300)