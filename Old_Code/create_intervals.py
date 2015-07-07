#create_intervals.py creates a json file with the number of views of all videos

import json
data = json.load(open('finalData.json'))
from math import floor, ceil
from collections import Counter
import time

t1 = time.time()
peaksDct = {}
for key in data.keys():
    values = data[key]
    segments = values['segments']
    if values['length'] == 'not available':
        print("missing length for: " + key)
        continue
    counterSeg = Counter()
    for seg in segments:
        seg = [int(floor(seg[0])), int(ceil(seg[1]))]
        end = min(seg[1], int(ceil(values['length'])))
        for el in range(seg[0], end+1):
            counterSeg[el] += 1
    peaksDct[key] = counterSeg
    
t2 = time.time()
print (t2-t1)

json.dump(peaksDct, open("viewsAll.json", 'w'))

