import numpy as np

datos = [14.5, 14.4, 14.52, 14.23]
media = np.mean(datos)
incertidumbre = np.std(datos, ddof=1)
incertidumbre_media = incertidumbre / np.sqrt(len(datos))

print(f"Resultado: {media:.2f} ± {incertidumbre:.2f}")4

import numpy as np


