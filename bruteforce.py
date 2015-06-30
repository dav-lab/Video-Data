# Amanda and Ella
# Brute Force Algorithm to search for peaks

import json
from collections import OrderedDict


def getPeaks(filename):
    '''Returns a dictionary where keys are video IDs and values are a list of peak points (tuples)
    :param filename: file of a dictionary of dictionaries where keys are video IDs and values are 
    a dictionary where keys are time in video and values are number of views'''
    data=json.load(open(filename))
    peaks={}
    for video in data:
        peaksList=[]      
        d = OrderedDict(sorted(data[video].items(), key=lambda t: int(t[0]))) 
        x = d.keys()
        y = d.values()
        if len(y) > 1:
            for pt in range(len(y)):
                if pt==0: # is first point a peak?
                    if y[pt+1] < y[pt]:
                        peaksList.append((x[pt],y[pt]))
                elif pt==len(y)-1: # is last point a peak?
                    if y[pt-1] < y[pt]:
                        peaksList.append((x[pt],y[pt])) 
                elif y[pt-1] < y[pt] and y[pt+1] < y[pt]:
                    peaksList.append((x[pt],y[pt]))
            peaks[video]=peaksList
    return peaks
                
print getPeaks('rewatchPeaks.json')