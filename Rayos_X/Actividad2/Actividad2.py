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
    
    for name in Names:
        CPath = path + name
        with open(CPath, 'r') as file:
            lines = islice(file, skip_rows, None)
            Data = [list(map(float,line.replace(',', '.').split())) for line in lines]
            
            DataA.append(Data[num_data])
            
            DataA[num_data][1] = DataA[num_data][1] / DataB[num_data][1]
            
    return DataA

DataA45 = read_data(PPath,NamesA)

y = [i[1] for i in DataA45]

plt.scatter(thiknA,y)
plt.show()