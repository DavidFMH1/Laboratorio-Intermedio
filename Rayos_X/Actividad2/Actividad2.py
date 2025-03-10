import matplotlib.pyplot as plt
import numpy as np
from itertools import islice

NameB = np.array(['Nofiltro'])
NamesA = np.array(['aluminio002mm','aluminio004mm','aluminio008mm','aluminio01mm'])
NamesB = np.array(['Zinc0025mm','Zinc005mm','Zinc0075mm','Zinc01mm'])
thiknA = np.array([0.02, 0.04, 0.08, 0.1])
thiknB = np.array([0.025, 0.075, 0.5, 0.1])

PPath = 'Rayos_X\\Actividad2\\'
 
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

while i < len(NamesA):
    
    data, sigy = read_data(PPath,NamesA,num_data=i)
    
    y = [i[1] for i in data]
    x = thiknA
    axs[0].errorbar(x,y,yerr=sigy, fmt='None')
    
    i += 1
    
plt.show()