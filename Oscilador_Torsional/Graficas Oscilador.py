import matplotlib.pyplot as plt
import matplotlib.gridspec as grd
import csv
import numpy as np

from scipy.optimize import curve_fit

Datos_a = "Oscilador_Torsional\\Datos_Amplitud.csv"
Datos_1a = "Oscilador_Torsional\\Datos_1a.csv"
Datos_1b = "Oscilador_Torsional\\Datos_1b.csv"
Datos_2 = "Oscilador_Torsional\\Datos_2.csv"
Datos_3 = "Oscilador_Torsional\\Datos_3.csv"
Datos_4a = "Oscilador_Torsional\\Datos_4a.csv"
Datos_4b = "Oscilador_Torsional\\Datos_4b.csv"
Datos_4c = "Oscilador_Torsional\\Datos_4c.csv"
Datos_5a = "Oscilador_Torsional\\Datos_5a.csv"
Datos_5b = "Oscilador_Torsional\\Datos_5b.csv"
 
def read_data(path):
    with open(path, 'r') as file:
        data1 = [float(line.split(',')[0]) for line in file]
    with open(path, 'r') as file:
        data2 = [float(line.split(',')[1]) for line in file]
    return data1, data2

Ampl, Vpp = read_data(Datos_a)
Ampl = np.array(Ampl)
Vpp = np.array(Vpp)

def linealfit(x,a,b):
    return a*x + b

#Calibracion del Oscilador

param,cov = curve_fit(linealfit,Ampl,Vpp)

#Actividad 1

def weirdfit(x,A):
    return -A*x

masa1, Dtheta1 = read_data(Datos_1a)

masa1, Dtheta1 = np.array(masa1), np.array(Dtheta1)

x = Dtheta1/np.cos(Dtheta1)
y = masa1*9.7753*0.0244/1000

guess = [0.05]

param1a ,cov1a = curve_fit(weirdfit,x,y,p0=guess)

_x = np.linspace(-2.06,2.06,100)
_y = weirdfit(_x,param1a[0])

yp = weirdfit(x,param1a[0])

res = y - yp

normres = res / np.std(res)

fig, axs1 = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

axs1[0].scatter(x, y, label="Datos", color='blue')
axs1[0].plot(_x, _y, label=f"Ajuste lineal: y = {param1a[0]:.3f}" + r"$\pm$" f"{np.sqrt(np.diagonal(cov1a))[0]:.3f}x", color='red')
axs1[0].set_ylabel("Torque")
axs1[0].set_title("Torque linealizado")
axs1[0].legend()
axs1[0].grid()

axs1[1].scatter(x, normres, label="Residuales Normalizados", color='green', marker='x')
axs1[1].axhline(0, color='black', linestyle='--')
axs1[1].set_ylabel("Residuales Normalizados")
axs1[0].set_xlabel(r"$\frac{\theta}{\cos\theta}$")
axs1[1].legend()
axs1[1].grid()

plt.tight_layout()

plt.savefig(r"C:\\Users\\david\\OneDrive\\Documentos\\Universidad\\Lab intermedio\\Repositorio intermedio\\Laboratorio-Intermedio\\Oscilador_Torsional\\actividad1.png")


#actividad 2 

nmasas, periodo = read_data(Datos_2)
nmasas, periodo = np.array(nmasas), np.array(periodo)

periodo2 = (periodo**2)/(4*np.pi**2)

guess = [0.173,1.34]

param2 ,cov2 = curve_fit(linealfit,nmasas,periodo2,p0=guess)

deviation2 = np.sqrt(np.diagonal(cov2))

_x2 = np.linspace(0,8,100)
_y2 = linealfit(_x2,param2[0],param2[1])

ypre2 = linealfit(nmasas,param2[0],param2[1])

res2 = periodo2 - ypre2

normres2 = res2 / np.std(res2)

fig, axs2 = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

axs2[0].scatter(nmasas, periodo2, label="Datos", color='blue')
axs2[0].plot(_x2, _y2, label=f"Ajuste lineal: y = {param2[0]:.4f}x + {param2[1]:.4f}\n m "+r"$\pm$"+f"{deviation2[0]:.4f}\n b "+r"$\pm$"+f" {deviation2[1]:.4f}", color='red')
axs2[0].set_ylabel(r"$T^{2} (s^{2})$")
axs2[0].set_title("Periodo linealizado")
axs2[0].legend()
axs2[0].grid()

axs2[1].scatter(nmasas, normres2, label="Residuales Normalizados", color='green', marker='x')
axs2[1].axhline(0, color='black', linestyle='--')
axs2[1].set_xlabel("Numero de masas")
axs2[1].set_ylabel("Residuales Normalizados")
axs2[1].legend()
axs2[1].grid()

plt.tight_layout()

plt.savefig(r"C:\\Users\\david\\OneDrive\\Documentos\\Universidad\\Lab intermedio\\Repositorio intermedio\\Laboratorio-Intermedio\\Oscilador_Torsional\\actividad2.png")

#Actividad 3

I, Dtheta3 = read_data(Datos_3)
I, Dtheta3 = np.array(I), np.array(Dtheta3)

Dp = Dtheta3/np.cos(Dtheta3)

guess3 = [0.3,0.003]

param3, cov3 = curve_fit(linealfit,I,Dp,p0=guess3)
deviation3 = np.sqrt(np.diagonal(cov3))

_x3 = np.linspace(-1.6,1.6,100)
_y3 = linealfit(_x3, param3[0], param3[1])

ypre3 = linealfit(I,param3[0],param3[1])

res3 = Dp - ypre3

normres3 = res3 / np.std(res3)

fig, axs3 = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

axs3[0].scatter(I, Dp, label="Datos", color='blue')
axs3[0].plot(_x3, _y3, label=f"Ajuste lineal: y = {param3[0]:.3f}x + {param3[1]:.3f}\n m "+r"$\pm$"+f" {deviation3[0]:.3f}\n b "+r"$\pm$"+f" {deviation3[1]:.3f}", color='red')
axs3[0].set_ylabel("I (A)")
axs3[0].set_title("Corriente normalizada")
axs3[0].legend()
axs3[0].grid()

axs3[1].scatter(I, normres3, label="Residuales Normalizados", color='green', marker='x')
axs3[1].axhline(0, color='black', linestyle='--')
axs3[1].set_xlabel(r"$\frac{\theta}{\cos\theta}$")
axs3[1].set_ylabel("Residuales Normalizados")
axs3[1].legend()
axs3[1].grid()

plt.tight_layout()

plt.savefig(r"C:\\Users\\david\\OneDrive\\Documentos\\Universidad\\Lab intermedio\\Repositorio intermedio\\Laboratorio-Intermedio\\Oscilador_Torsional\\actividad3.png")


#Actividad 4

def exponentialfit(x,A,B,C):
    return A*np.exp(-B*x)+C

t1, V1 = read_data(Datos_4a)
t2, V2 = read_data(Datos_4b)
t3, V3 = read_data(Datos_4c)

t1, V1 = np.array(t1), np.abs(np.array(V1))
t2, V2 = np.array(t2), np.abs(np.array(V2))
t3, V3 = np.array(t3), np.abs(np.array(V3))

guess4a = [13.07,0.13,0.03]
guess4b = [15.2,2.0,0.03]
guess4c = [11.8,2,0.03]

param4a, cov4a = curve_fit(exponentialfit,t1,V1)
param4b, cov4b = curve_fit(exponentialfit,t2,V2)
param4c, cov4c = curve_fit(exponentialfit,t3,V3)

_x4a = np.linspace(0,9,100)
_x4b = np.linspace(0,9,100)
_x4c = np.linspace(0,9,100)

_y4a = exponentialfit(_x4a,param4a[0],param4a[1],param4a[2])
_y4b = exponentialfit(_x4b,param4b[0],param4b[1],param4b[2])
_y4c = exponentialfit(_x4c,param4c[0],param4c[1],param4c[2])

ypre4a = exponentialfit(t1,param4a[0],param4a[1],param4a[2])
ypre4b = exponentialfit(t2,param4b[0],param4b[1],param4b[2])
ypre4c = exponentialfit(t3,param4c[0],param4c[1],param4c[2])

res4a = V1 - ypre4a
res4b = V2 - ypre4b
res4c = V3 - ypre4c

normres4a = res4a / np.std(res4a)
normres4b = res4b / np.std(res4b)
normres4c = res4c / np.std(res4c)

fig, axs4 = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

axs4[0].scatter(t1, V1, color='blue', marker='s')
axs4[0].scatter(t2, V2, color='g', marker='^')
axs4[0].scatter(t3, V3, color='m', marker='v')
axs4[0].plot(_x4a, _y4a, label=f"Ajuste exponencial: y = {param4a[0]:.4f}e^{param4a[1]:.4f} + {param4a[2]:.4f}", color='blue')
axs4[0].plot(_x4b, _y4b, label=f"Ajuste exponencial: y = {param4b[0]:.4f}e^{param4b[1]:.4f} + {param4b[2]:.4f}", color ='g')
axs4[0].plot(_x4c, _y4c, label=f"Ajuste exponencial: y = {param4c[0]:.4f}e^{param4c[1]:.4f} + {param4c[2]:.4f}", color ='m')
axs4[0].set_ylabel("V (v)")
axs4[0].set_title("Amplitud en funcion del tiempo")
axs4[0].legend()
axs4[0].grid()

axs4[1].scatter(t1, normres4a, label="Residuales Normalizados", color='blue', marker='x')
axs4[1].scatter(t2, normres4b, label="Residuales Normalizados", color='g', marker='x')
axs4[1].scatter(t3, normres4c, label="Residuales Normalizados", color='m', marker='x')
axs4[1].axhline(0, color='black', linestyle='--')
axs4[1].set_xlabel("t (s)")
axs4[1].set_ylabel("Residuales Normalizados")
axs4[1].legend()
axs4[1].grid()

plt.tight_layout()

plt.savefig(r"C:\\Users\\david\\OneDrive\\Documentos\\Universidad\\Lab intermedio\\Repositorio intermedio\\Laboratorio-Intermedio\\Oscilador_Torsional\\actividad4.png")


#Actividad 5

def forcedfit(f, A, B, C):
    return A / np.sqrt((B - f**2)**2 + C**2 * f**2)

frecu1, ampl1 = read_data(Datos_5a)
frecu2, ampl2 = read_data(Datos_5b)

frecu1, ampl1 = np.array(frecu1), np.array(ampl1)
frecu2, ampl2 = np.array(frecu2), np.array(ampl2)

guess5a = [1,1,1]
guess5b = [1,1,1]

param5a, cov5a = curve_fit(forcedfit, frecu1, ampl1)
param5b, cov5b = curve_fit(forcedfit, frecu2, ampl2)

_x5 =np.linspace(0.1,1.4,100)

_y5a = forcedfit(_x5,param5a[0],param5a[1],param5a[2])
_y5b = forcedfit(_x5,param5b[0],param5b[1],param5b[2])

ypre5a = forcedfit(frecu1,param5a[0],param5a[1],param5a[2])
ypre5b = forcedfit(frecu2,param5b[0],param5b[1],param5b[2])

res5a = ampl1 - ypre5a
res5b = ampl2 - ypre5b

normres5a = res5a / np.std(res5a)
normres5b = res5b / np.std(res5b)

fig, axs5 = plt.subplots(2, 1, figsize=(15,7.5), gridspec_kw={'height_ratios': [3, 1], 'hspace': 0})

axs5[0].scatter(frecu1, ampl1, label="Datos 1", color='blue', marker='s')
axs5[0].scatter(frecu2, ampl2, label='Datos 2', color='g', marker='^')
axs5[0].plot(_x5, _y5a, color='blue')
axs5[0].plot(_x5, _y5b, color ='g')
axs5[0].set_ylabel("Amplitud (v)")
axs5[0].set_title("amplitud en funcion de la frecuencia")
axs5[0].legend()
axs5[0].grid()

axs5[1].scatter(frecu1, normres5a, label="Residuales Normalizados", color='blue', marker='x')
axs5[1].scatter(frecu2, normres5b, label="Residuales Normalizados", color='g', marker='x')
axs5[1].axhline(0, color='black', linestyle='--')
axs5[1].set_xlabel("Frecuencia (Hz)")
axs5[1].set_ylabel("Residuales Normalizados")
axs5[1].legend()
axs5[1].grid()

plt.tight_layout()
plt.savefig(r"C:\\Users\\david\\OneDrive\\Documentos\\Universidad\\Lab intermedio\\Repositorio intermedio\\Laboratorio-Intermedio\\Oscilador_Torsional\\actividad5.png")
