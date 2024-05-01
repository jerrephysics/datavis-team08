import imageio
import os
from pathlib import Path
import numpy as np
from itertools import product
import matplotlib.pyplot as plt
import json

from datavis1 import *
from datavis_add_coords_to_regions import get_ports

print(32*'-')
print(orders)

TILES_FOLDER = Path('./Tiles/6/')

coord_to_file = lambda x,y : f'./Tiles/6/{x}/{y}.png'

files = [str(f) for f in TILES_FOLDER.rglob('*.png')]
#print(files)


array_dim = [0,0]

for f in files:
    f_split = f.split('/')
    f_split.pop(0)
    f_split.pop(0)
    f_split[-1] = int(f_split[-1].split('.')[0])
    f_split[0] = int(f_split[0])
    array_dim[0] = max(array_dim[0],f_split[0])
    array_dim[1] = max(array_dim[1],f_split[1])



file_ranges = np.array(array_dim)+1
array_dim = 256*(np.array(array_dim)+1)
combined_image = np.zeros([array_dim[1],array_dim[0],3])
#print(combined_image.shape)

for coord in product(*[range(d) for d in file_ranges]):
    x,y = coord
    start_x = 256*x
    end_x = 256*(x+1)
    start_y = 256*y
    end_y = 256*(y+1)
    
    image = imageio.imread(coord_to_file(x,y))
    
    combined_image[start_y:end_y,start_x:end_x,:] = image

combined_image = combined_image.astype('int')


ports = get_ports()

places = sorted(list(ports.keys()))
matches = 0

for _,r in regions.iterrows():
    if r['Territory'] not in places:
        #print(r['Territory'])
        for p in places:
            if r['Territory'].lower() in p.lower():
                print(f'\t row < place {r["Territory"]} < {p}')
            elif p.lower() in r['Territory'].lower():
                print(f'\t row > place {r["Territory"]} > {p}')
            else:
                continue
            matches = matches + 1
        else:
            print(f'No match found for {r["Territory"]}')
        places.append(r['Territory'])
    else:
        matches = matches + 1

rows = len(list(regions.iterrows()))
print(sorted(places))
print(matches/rows)






















plt.imshow(combined_image)

for p in ports:
    #print(p,ports[p])
    plt.scatter(2*ports[p][0],2*ports[p][1],s=40,marker='x',c='red')
    #plt.text(2*ports[p][0],2*ports[p][1],s=p)



if __name__ == '__main__':
    plt.show()

