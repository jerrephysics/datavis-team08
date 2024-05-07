import pandas as pd
import numpy as np
import os
import json
import time
import matplotlib.pyplot as plt
import string
import random

from itertools import product

from tqdm import tqdm

def get_random_string_of_length(n):
    letters = string.ascii_lowercase
    ret_str = ''.join([random.choice(letters) for i in range(n)])
    print(ret_str)
    return ret_str

with open('DEAD/data/regions.csv','r') as f:
    regions = pd.read_csv(f)
    
def levenshtein(a,b,level = 0,max_length=0):
    if a in b or b in a:
        return 0    
    elif len(a) == 0:
        return len(b)
    elif len(b) == 0:
        return len(a)
    elif a[0] == b[0]:
        return levenshtein(a[1:],b[1:],level + 1)
    else:
        return 1 + min(levenshtein(a[1:],b,level+1),levenshtein(a,b[1:],level+1),levenshtein(a[1:],b[1:],level+1))

def stringdist(a,b):
    letters_a = set(a)
    letters_b = set(b)
    letters_a.union(letters_b)
    all_letters = sorted(list(letters_a))
    del letters_a
    del letters_b
    
    vec_a = [a.count(l) for l in all_letters]
    vec_b = [b.count(l) for l in all_letters]
    
    d = 0
    for i in range(len(vec_a)):
        d = d + (vec_a[i] - vec_b[i])**2
    
    if d < 2:
        return levenshtein(a,b)
    return d

def get_ports():
    ports = []
    JSON_FILES = [f for f in os.listdir('./') if f.endswith('.json')]

    for file_name in JSON_FILES:
        with open(file_name,'r',encoding='utf-8-sig') as f:
            cities = json.load(f)
        ports = ports + cities['features']
        del cities

    ports_name_coords = []
    for p in ports:
        ports_name_coords.append((p['properties']['name'],p['geometry']['coordinates']))

    ports = dict(ports_name_coords)
    del ports_name_coords
    return ports

ports = get_ports()

with open('ports_in_json.txt','w') as f:
    f.writelines('\n'.join(sorted(list(ports.keys()))))

matched = []

terr = ''

best_matches = {}
for _,r in regions.iterrows():
    terr = r['Territory']
    #terr_words = terr.split(' ')
    print(' - '.join([terr,r['Area'],r['Region']]))
    dist = np.inf
    best_match = ''
    for p in tqdm(ports):
        #port_words = p.split(' ')
        #new_dist = levenshtein(terr.lower(),p.lower(),max_length=100)
        new_dist = stringdist(terr.lower(),p.lower())
        if new_dist < dist:
            best_match = p
        dist = min(dist,new_dist)
        if dist == 0:
            print('\t possible substring match')
            matched.append(p)
            break
    print(f"\t -> best match for {terr} is {best_match} with distance {dist}")
    best_matches[terr] = best_match

unmatched = [r['Territory'] for _,r in regions.iterrows() if r['Territory'] not in matched and not r['Area'] == 'Underdark']

print(f"{len(matched)} out of {len(list(regions.iterrows()))} were matched")

with open('places_to_find.txt','w') as f:
    f.writelines('\n'.join(unmatched))


