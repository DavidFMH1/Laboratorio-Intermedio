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

masa1, Dtheta1 = read_data(Datos_1a)
masa2, Dtheta2 = read_data(Datos_1b)

masa1, Dtheta1 = np.array(masa1), np.array(Dtheta1)
masa2, Dtheta2 = np.array(masa2), np.array(Dtheta2)

x = Dtheta1/np.cos(Dtheta1)
y =2*masa1*9.7735*0.0244/1000

param1a ,cov1a = curve_fit(linealfit,x,y)

#actividad 2 

nmasas, periodo = read_data(Datos_2)
nmasas, periodo = np.array(nmasas), np.array(periodo)

periodo2 = (periodo**2)/(4*np.pi**2)

param2 ,cov2 = curve_fit(linealfit,nmasas,periodo2)

print(param2,np.sqrt(np.diagonal(cov2)))

_x = np.linspace(0,8,100)
_y = linealfit(_x,param2[0],param2[1])

fig, (ax1,ax2) = plt.subplots(2,1,sharex=True)
plt.subplots_adjust(hspace=0)
ax1.scatter(nmasas, periodo2, color='r')
ax1.plot(_x,_y,color='black')

ax1.grid(True)

plt.show()

#Actividad 3

I, Dtheta3 = read_data(Datos_3)
I, Dtheta3 = np.array(I), np.array(Dtheta3)


#Actividad 4

t1, V1 = read_data(Datos_4a)
t2, V2 = read_data(Datos_4b)
t3, V3 = read_data(Datos_4c)

t1, V1 = np.array(t1), np.array(V1)
t2, V2 = np.array(t2), np.array(V2)
t3, V3 = np.array(t3), np.array(V3)


#Actividad 5

frecu1, ampl1 = read_data(Datos_5a)
frecu2, ampl2 = read_data(Datos_5b)