import numpy as np
import matplotlib.pyplot as plt
import csv

from scipy.optimize import curve_fit

path = 'Torque_magnetico\\Actividad2\\Actividad2.csv'

R, M= 2.6875/100, 141.3/1000
sR, sM = 0.00005, 0.0001

NF = (5/(8*((np.pi)**2)*(R**2)*M))

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

curr, per = read_data(path)
Mfield = convert_curr_to_Mfield(curr) 
MfieldN = 1/Mfield

per2 = (per/5)**2

sigBn = (1/Mfield**2)*6.8e-5
sigper2 = 2*(per/5)*0.02

c, sigc, m, sigm = Weighted_least_squares(per2, MfieldN, sigBn) 

mu = m/NF
sigmu = np.sqrt(((8/5)*(np.pi**2)*(R**2)*m*sM)**2 + ((16/5)*(np.pi**2)*R*m*sR)**2 + ((8/5)*(np.pi**2)*(R**2)*M*sigm)**2)

print(f'De esta actividad se puede deducir un valor de mu {mu:.2f} mas o menos {sigmu:.2f}')

_x = np.linspace(np.min(per2)-sigper2[0],(np.max(per2))+3*sigper2[0])
_y = linealfunc(_x,m,c)

#residuales

res = (MfieldN - linealfunc(per2,m,c))/sigBn

fig, axs = plt.subplots(2, 1, figsize=(7,5.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0, 'wspace': 0.15})

mt = fr'$m = {m:.0f} \pm {sigm:.0f}$'
ct = fr'$b = {c:.0f} \pm {sigc:.0f}$'

fig.suptitle('Inverso del campo en función del periodo al cuadrado', fontsize=12)

axs[0].errorbar(per2, MfieldN, yerr=sigBn, xerr=sigper2, fmt='o', label='Datos',color='black', capsize=3, elinewidth=1.5, markersize=6)
axs[0].plot(_x,_y,color='red', label=f'Regresión Lineal \n {mt} \n {ct}')
axs[0].set_ylabel(r'$\frac{1}{B}$ $(T^{-1})$', fontsize=14)
axs[0].legend()

axs[1].scatter(per2, res, color='black', marker='x')
axs[1].axhline(0, color='black', linestyle='--')
axs[1].set_ylabel('Residuales \n normalizados', fontsize=12)
axs[1].set_xlabel(r'$T^{2}$ $(s^{2})$', fontsize=12)

for row in axs:
    row.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)

plt.savefig(r'Torque_magnetico\\Actividad2\\campontvsperiodo22.png', format='png', dpi=300)