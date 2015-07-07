#Amanda Foun
#uses matplotlib to create a line chart of all the views
#the peaks are marked on the graph

import sys
from numpy import NaN, Inf, arange, isscalar, asarray, array
from matplotlib.pyplot import plot, scatter, show
from pylab import *
import json
import requests
import xmltodict
import bisect

 
def peakdet(v, delta, x = None):
    """Detects peaks in a vector and returns two arrays with min and max values
       [MAXTAB, MINTAB] = PEAKDET(V, DELTA) finds the local maxima and minima. 
        A point is considered a max peak if it has the max value, and was 
        preceded (to the left) by a value lower by DELTA."""
    maxtab = []
    mintab = []
       
    if x is None:
        x = arange(len(v))
    
    v = asarray(v)
    
    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')   
    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')    
    if delta <= 0:
        sys.exit('Input argument delta must be positive')
    
    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN
    
    lookformax = True
    
    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]        
        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True
 
    return array(maxtab), array(mintab)


<<<<<<< HEAD
APIKEY= 'AIzaSyCRau8nX4c2rubB_ckdUyODhwakNkjUGGI' #'APIKEY'
=======
APIKEY= #'APIKEY'
>>>>>>> origin/master
json_data = open("viewsAll.json").read() 
videoInfo = json.loads(json_data) 


def makePeakPlot(VIDEOID):
    # gather data from allViews.json which was created in numViews.py
    viewsDict = videoInfo[VIDEOID]
    
    # populate x and y, which contain the points to plot on the graph
    x = []
    y = []
    toInt = map(int, viewsDict.keys())
    toInt.sort()
    for k in toInt: # populate x and y
        x.append(k) # append time (min)
        y.append(viewsDict[str(k)]) # append the corresponding video views
    
    # display the graph   
    if __name__=="__main__":
        maxtab, mintab = peakdet(y,5)
        xlabel('time (secs)')
        ylabel('views')
        title('Peaks in Video Views')
        xlim(-5,max(x))
        plot(y, label=VIDEOID)
        legend = plt.legend(loc='upper right', shadow=True, fontsize='large')
        scatter(array(maxtab)[:,0], array(maxtab)[:,1], color='blue')
        #scatter(array(mintab)[:,0], array(mintab)[:,1], color='red')
        show()
        return maxtab


def getSubList(VIDEOID):
    '''Helper function for getSub() that 
    Returns a list of all the transcripts for a given video'''
    info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)

    if info['items'][0]['contentDetails']['caption']=='true':
        subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
        a=xmltodict.parse(subs)
        listOfSubs=a['transcript']['text']
        return listOfSubs
    else:
        return '--NO TRANSCRIPT PROVIDED--'
 
def getSub(time,subList):
    '''returns the transcript (string) of the video at the given time
        :param time: given time in seconds
        :param videoID: video ID'''
    startTimes=[]
    text=[]
    if subList == '--NO TRANSCRIPT PROVIDED--':
        return '--NO TRANSCRIPT PROVIDED--'
    else:
        for i in subList:
            startTimes.append(float(i['@start']))
            try:
                text.append(i['#text'])
            except KeyError: # no subtitles there
                text.append('-NONE-')
        breakpoints=startTimes[1:] # list of all the start times of the video
        # bisect returns an insertion point which comes after ane existing entries of time in breakpoints
        i=bisect.bisect(breakpoints,time)
        # try to get the most out of the transcript
        if i<len(text)-2:
            return text[i]+text[i+1]+text[i+2]
        elif i<len(text)-1:
            return text[i]+text[i+1]
        else:
            return text[i]


def peakTranscripts():
    '''Writes a file peakTranscripts.txt that contains all the transcripts at all the video peaks'''
    tran = open('peakTranscripts.txt', 'w')

    for vid in videoInfo: # vid is the video ID
        viewsDict=videoInfo[vid]
        # populate x and y, which contain the points to plot on the graph
        xval = []
        yval = []
        toInt = map(int, viewsDict.keys())
        toInt.sort()
        for k in toInt: # populate x and y
            xval.append(k) # append time (min)
            yval.append(viewsDict[str(k)]) # append the corresponding video views
        maxval, minval = peakdet(yval,5)
        tran.write('*** VIDEOID: ' + vid + ' ***' + '\n')
        for pt in maxval: # add the transcripts at each peak
            tran.write("(" + str(pt[0]) + " SECS): " + getSub(pt[0],getSubList(vid)) + '\n')

    tran.close()

        
#############
## TESTING ##
#############

## create plot using matplotlib
maxtab = makePeakPlot("BWBUXxyRILw")

## print out the corresponding transcript
#subList = getSubList("lhERAjJFcek")
#for pt in maxtab: # loop through the peak coordinates
#    print "(" + str(pt[0]) + " SECS): " + getSub(pt[0],subList) + '\n'
    
#peakTranscripts()