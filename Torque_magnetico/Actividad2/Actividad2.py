import numpy as np
import matplotlib.pyplot as plt
import csv

from scipy.optimize import curve_fit

path = 'Torque_magnetico\\Actividad2\\Actividad2.csv'

R, M= 2.6875, 141.3

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

c, sigc, m, sigm = Weighted_least_squares(per2, MfieldN, sigBn) 
print(m)

_x = np.linspace(np.min(per2),(np.max(per2)))
_y = linealfunc(_x,m,c)

fig, axs = plt.subplots(2, 1, figsize=(7,5.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0, 'wspace': 0.15})

fig.suptitle('Inverso del campo en función del periodo al cuadrado', fontsize=12)

axs[0].errorbar(per2, MfieldN, yerr=sigBn, fmt='o', label='Datos',color='blue', capsize=5, elinewidth=1.5, markersize=6)
axs[0].plot(_x,_y,color='red')

for row in axs:
    row.grid(visible=True, linestyle="--", linewidth=0.7, alpha=0.7)

'''plt.show()'''