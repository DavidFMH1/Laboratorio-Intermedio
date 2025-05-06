import numpy as np

datos = [4.1, 4.2, 4.3, 4.12]
media = np.mean(datos)
incertidumbre = np.std(datos, ddof=1)
incertidumbre_media = incertidumbre / np.sqrt(len(datos))

print(f"Resultado: {media:.2f} ± {incertidumbre:.2f}")