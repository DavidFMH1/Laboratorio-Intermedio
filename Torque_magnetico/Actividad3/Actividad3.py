import numpy as np
import matplotlib.pyplot as plt
import csv

from scipy.optimize import curve_fit

path = 'Torque_magnetico\\Actividad3\\Actividad3.csv'

R, M= 2.6875/100, 141.3/1000
sR, sM = 0.00005, 0.0001

NF = (5/(32*(np.pi**2)*(R**2)*M))

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

curr, freq = read_data(path)

tfreq = freq.copy()
tfreq[-2:] *= 2

mfield = convert_curr_to_Mfield(curr)

sigfreq = (tfreq**2)*0.16
sigB = np.full(len(mfield),6.8e-5)

c, sc, m, sm = Weighted_least_squares(mfield,tfreq,sigfreq)

_x = np.linspace(np.min(mfield)-6.8e-5,np.max(mfield)+6.8e-5)
_y = linealfunc(_x,m,c)

mu = m/NF

sigmu = np.sqrt(((32/5)*(np.pi**2)*(R**2)*m*sM)**2 + ((64/5)*(np.pi**2)*R*m*sR)**2 + ((32/5)*(np.pi**2)*(R**2)*M*sm)**2)

print(f'De esta actividad se puede deducir un valor de mu {mu:.2f} mas o menos {sigmu:.2f}')

#residuales

res = (tfreq - linealfunc(mfield,m,c))/sigfreq

fig, axs = plt.subplots(2, 1, figsize=(7,5.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0, 'wspace': 0.15})

mt = fr'$m = {m:.0f} \pm {sm:.0f}$'
ct = fr'$b = {c:.3f} \pm {sc:.3f}$'


fig.suptitle('Torque mecánico en función del campo magnético', fontsize=12)

axs[0].errorbar(mfield, freq, yerr=sigfreq, xerr=sigB, fmt='o', label='Datos',color='black', capsize=3, elinewidth=1.5, markersize=6)
axs[0].plot([mfield[-1],mfield[-1]],[np.min(tfreq),freq[-1]*2],'--',color='red', linewidth=1.5)
axs[0].scatter(mfield[-1],2*freq[-1],marker='x',color='red')
axs[0].plot([mfield[-2],mfield[-2]],[np.min(tfreq),freq[-2]*2],'--',color='red', linewidth=1.5)
axs[0].scatter(mfield[-2],2*freq[-2],marker='x',color='red')
axs[0].plot(_x,_y,color='red', label=f'Regresión Lineal \n {mt} \n {ct}')
axs[0].set_ylabel(r'$\Omega$ (Hz)')
axs[0].legend()

axs[1].scatter(mfield,res,color='black',marker='x')
axs[1].axhline(0, color='black', linestyle='--')
axs[1].set_ylabel('Residuales\n normalizados', fontsize = 12)
axs[1].set_xlabel('B (mT)', fontsize=12)

for row in axs:
    row.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)

plt.savefig(r'Torque_magnetico\\Actividad3\\campovsfrecuencialarm.png', format='png', dpi=300)