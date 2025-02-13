import matplotlib.pyplot as plt
import matplotlib.gridspec as grd
import csv
import numpy as np

from scipy.optimize import curve_fit
archivo = "Fisica de muones\\25-01-31-19-36.data"
archivo2 = "Fisica de muones\\25-02-07-18-03.data"

def exponentialfit(x, A, T):
    return A * np.exp(-x / T)  

def read_data(path):
    with open(path, 'r') as file:
        data = [int(line.split(' ')[0]) for line in file]
    return data
  
datos = read_data(archivo)
datos2 = read_data(archivo2)

datosn = [d for d in datos if 80 <= d <= 20000]
datosn2 =[d for d in datos2 if 80 <= d <= 20000]

valores_unicos, ocurrencias = np.unique(datosn, return_counts=True)
valores_unicos2 , ocurrencias2 = np.unique(datosn2, return_counts=True)

num_bins = 20
bins = np.linspace(0, 20000, num_bins + 1)
bin_indices = np.digitize(datosn, bins) - 1
bin_indices = np.clip(bin_indices, 0, num_bins - 1)
bin_indices2 = np.digitize(datosn2, bins) - 1
bin_indices2 = np.clip(bin_indices2, 0, num_bins - 1)

conteo_por_bin = np.bincount(bin_indices, minlength=num_bins)
suma_por_bin = np.bincount(bin_indices, weights=datosn, minlength=num_bins)
promedio_por_bin = np.divide(suma_por_bin, conteo_por_bin, where=conteo_por_bin > 0)

conteo_por_bin2 = np.bincount(bin_indices2, minlength=num_bins)
suma_por_bin2 = np.bincount(bin_indices2, weights=datosn2, minlength=num_bins)
promedio_por_bin2 = np.divide(suma_por_bin2,conteo_por_bin2, where=conteo_por_bin2 > 0)

y = (bins[:-1] + bins[1:]) / 2
error_x = np.full(num_bins, (bins[1] - bins[0]) / 2)

mask = conteo_por_bin > 0
mask2 = conteo_por_bin2 > 0
guess = [10, 2000]
param, cov = curve_fit(exponentialfit, y[mask], conteo_por_bin[mask], p0=guess)
param2 , cov2 = curve_fit(exponentialfit,y[mask2], conteo_por_bin2[mask2], p0=guess)

cov1 = np.sqrt(np.diagonal(cov))/1000
cov_2 = np.sqrt(np.diagonal(cov2))/1000

residuales_1 = (conteo_por_bin - exponentialfit(y, param[0], param[1])) / np.sqrt(conteo_por_bin)
residuales_2 = (conteo_por_bin2 - exponentialfit(y, param2[0], param2[1])) / np.sqrt(conteo_por_bin2)

print(param, cov)

x_ = np.linspace(0, 20000, 100)
y_ = exponentialfit(x_, param[0], param[1])
y_2 = exponentialfit(x_, param2[0], param2[1])

fig = plt.figure(figsize=(15,7.5))
gs = grd.GridSpec(5, 3, height_ratios=[1, 0.5, 0.2, 1, 0.5], width_ratios=[1, 0.001, 1.8], hspace=0, wspace=0.2)

ax1 = plt.subplot(gs[:2, 0])
ax2 = plt.subplot(gs[-2:,0])

ax3 = plt.subplot(gs[0,2])
ax4 = plt.subplot(gs[1,2])
ax5 = plt.subplot(gs[3,2])
ax6 = plt.subplot(gs[4,2])

ax1.scatter(valores_unicos, ocurrencias,alpha=0.5,color='b', label='Raw Data,\nToma de datos 1')
ax1.set_ylabel("Numero\nde eventos", color='b')
ax1.set_title("Tiempo vs Numero de decaimientos")

ax1.grid(True)

ax1.legend(loc='upper right')

ax2.scatter(valores_unicos2, ocurrencias2,alpha=0.5,color='b', label='Raw Data,\ntoma de datos 2')
ax2.set_ylabel("Numero\nde eventos", color='b')
ax2.set_xlabel("Tiempo (ns)")

ax2.grid(True)

ax2.legend(loc='upper right')

param_text = r'$N_{0}$' + f" = {param[0]:.2f} " + r'$\pm$' + f" {cov1[0]:.2f}, " + r'$\tau$' + f" = {param[1]/1000:.2f}" + r'$\pm$' + f" {cov1[1]:.2f}"
ax3.plot(x_, y_, label=f"Toma de datos 1\nAjuste exponencial,\n{param_text}", color="black")
ax3.errorbar(y, conteo_por_bin, xerr=error_x, fmt='o', color='r', capsize=5, label="Valor promedio con error en X")

ax3.set_ylabel("Eventos\npor bin", color='r')
ax3.set_title("Tiempo vs Decaiminetos por bin")

ax3.grid(True)

ax3.legend(loc="upper right", fontsize=9)

ax4.scatter(y, residuales_1, color='g', marker='x')
ax4.axhline(0, color='gray', linestyle='--')  
ax4.set_ylabel("Residuales\nNormalizados")

ax4.grid(True)

param_text2 = r'$N_{0}$' + f" = {param2[0]:.2f} "+r'$\pm$' + f" {cov_2[0]:.2f}, " + r'$\tau$' + f" = {param2[1]/1000:.2f} " + r'$\pm$' + f" {cov_2[1]:.2f}"
ax5.plot(x_, y_2 , label=f"Toma de datos 2\nAjuste exponencial 2,\n{param_text2}", color='black')
ax5.errorbar(y, conteo_por_bin2, xerr=error_x, fmt="o", color="r", capsize=5, label="Valor promedio con error en X 2")

ax5.set_xlabel("Tiempo (ns)")
ax5.set_ylabel("Eventos\npor bin", color='r')

ax5.grid(True)

ax5.legend(loc="upper right", fontsize=9)

ax6.scatter(y, residuales_2, color='g', marker='x')
ax6.axhline(0, color='gray', linestyle='--')  
ax6.set_ylabel("Residuales\nNormalizados")
ax6.set_xlabel("Tiempo (ns)")

ax6.grid(True)

plt.savefig(r"Fisica de muones\\deteccion de muones.png", format="png", dpi=300)

