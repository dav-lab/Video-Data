# Amanda and Ella
# Brute Force Algorithm to search for peaks

import json
from collections import OrderedDict


def getPeaksForOneVideo(videoID):
    '''Returns a list of peak points (tuples)
    :param videoID: videoID string'''
    peaks=[] 
    json_data = open("FinishedCourseData/normalize.json").read() 
    videoInfo = json.loads(json_data)
    viewsDict = videoInfo[videoID]
    d = OrderedDict(sorted(viewsDict.items(), key=lambda t: int(t[0]))) 
    x = d.keys()
    y = d.values()
    if len(y) > 1:
        for pt in range(len(y)):
            if pt==0: # is first point a peak?
                if y[pt+1] < y[pt]:
                    peaks.append((x[pt],y[pt]))
            elif pt==len(y)-1: # is last point a peak?
                if y[pt-1] < y[pt]:
                    peaks.append((x[pt],y[pt])) 
            elif y[pt-1] < y[pt] and y[pt+1] < y[pt]:
                peaks.append((x[pt],y[pt]))
    return peaks

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
            #disregard peaks in first 5 seconds
            for pt in range(5,len(y)):
                if pt==len(y)-1: # is last point a peak?
                    if y[pt-1] < y[pt] and y[pt]>=0.25:
                        peaksList.append((x[pt],y[pt])) 
                elif y[pt-1] < y[pt] and y[pt+1] < y[pt]:
                    if y[pt]>=0.25:
                        peaksList.append((x[pt],y[pt]))
            peaks[video]=peaksList
    with open('peaksGreaterThan025.json', 'w') as outfile:
        json.dump(peaks, outfile)

getPeaks('FinishedCourseData/normalize.json')
#print getPeaksForOneVideo('qic9_yRWj5U')