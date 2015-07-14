# Amanda and Ella
# Brute Force Algorithm to search for peaks

import json
from collections import OrderedDict


def getPeaksForOneVideo(videoID):
    '''Returns a list of peak points (tuples)
    :param videoID: videoID string'''
    peaks=[] 
    json_data = open("FinishedCourseData/pausePlayBinsSmooth.json").read() 
    videoInfo = json.loads(json_data)
    viewsDict = videoInfo[videoID]
    d = OrderedDict(sorted(viewsDict.items(), key=lambda t: float(t[0]))) # the points of the peaks
    x = d.keys()
    y = d.values()
    if len(y) > 1:
        for pt in range(5,len(y)-1): # ignore peaks in first 5 seconds and the last second
            #if pt==len(y)-1: # is last point a peak?
            #    if y[pt-1] < y[pt] and y[pt]>=0.25:
            #        peaks.append((x[pt],y[pt])) 
            if y[pt-1] < y[pt] and y[pt+1] < y[pt]:
                if y[pt]>=0.25:
                    peaks.append((x[pt],y[pt]))
    #only return top 5 peaks
    sortedPeaks=sorted(peaks, key=lambda i:i[1], reverse=True)
    return sortedPeaks[:5]

#print getPeaksForOneVideo("SVQuLOiHJeE")

def getPeaks(filename):
    '''Returns a dictionary where keys are video IDs and values are a list of peak points (tuples)
    :param filename: file of a dictionary of dictionaries where keys are video IDs and values are 
    a dictionary where keys are time in video and values are number of views'''
    data=json.load(open(filename))
    peaks={}
    for video in data:
        peaksList=[]     
        d = OrderedDict(sorted(data[video].items(), key=lambda t: float(t[0]))) 
        x = d.keys()
        y = d.values()
        if len(y) > 1:
            for pt in range(5,len(y)-1): # ignore peaks in first 5 seconds and the last second
                if y[pt-1] < y[pt] and y[pt+1] < y[pt]:
                    if y[pt]>=0.25:
                        peaksList.append((x[pt],y[pt]))
            sortedPeaks=sorted(peaksList, key=lambda i:i[1], reverse=True)
        peaks[video]=sortedPeaks[:5]
    with open('pausePlaySmoothPeaks.json', 'w') as outfile:
        json.dump(peaks, outfile)

#getPeaks('FinishedCourseData/pausePlayBinsSmooth.json')

def groupPeaksByWeek():
    '''Returns a dictionary where keys are week number and values are dictionaries where
    keys are video IDs and values are lists of peaks'''
    d={}
    peaks=json.load(open('FinishedCourseData/peaksGreaterThan025.json'))
    weeks=json.load(open('videoTranscripts/videoTitles.json'))
    for video in weeks:
        try:
            if weeks[video]['week'] not in d:
                i=weeks[video]['url'][32:] # video id of video with transcript
                d[weeks[video]['week']]={i:peaks[i]}
            else:
                d[weeks[video]['week']][i]=peaks[i]
        except KeyError: # if video does not have url or transcript
            pass
    return d
        
#print getPeaksForOneVideo('qic9_yRWj5U')