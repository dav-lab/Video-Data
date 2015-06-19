#Amanda Foun
#numViews.py creates a list of dictionaries which contain info about the number of video views

#NOTES
#round the numbers

import json
from collections import Counter

def findOverlaps(viewList):
    '''Helper function for videoViewDicts() that returns a list
        of lists of interval pairs that overlap.
        :param viewList: sorted list of video view interval (tuples)'''
    overlaps=[] 
    for i in xrange(len(viewList)):
        for j in xrange(i+1,len(viewList)):
            x = viewList[i]
            y = viewList[j]
            if x[0] == y[0]:
                overlaps.append([x, y])
            elif x[1] == y[1]:
                overlaps.append([x, y])
            elif (x[1]>y[0] and x[0]<y[0]):
                overlaps.append([x, y])
    return overlaps

def expandList(viewList):
    '''Helper function for videoViewDicts() that returns a list of ranges (ints)
        :param viewList: sorted list of video view interval (tuples)'''
    fullList = []
    for tup in viewList:
        ran = range(tup[0],tup[1]) # list of the numbers in that range
        for num in ran:
            fullList.append(num) # individually add each number to list
    return fullList

def videoViewDicts(infoFile):
    '''Returns a list of dictionaries where the keys are the videoID and lists of time intervals
       and the values show how many views there were at each interval.
       :param infoFile: dictionary of dictionaries of info about each video'''
    viewsDict ={}
    for video in infoFile: # video is the videoID
        viewList=[]
        segList = infoFile["lhERAjJFcek"]['segments'] # list of lists; play/pause events
        segList.sort() # sorts from smallest start time to largest
        for seg in segList: # seg is a list of 2 floats
            rounded_list = map(int,map(round,seg)) # rounds to nearest integer
            rounded_tuple = tuple(rounded_list) # because lists can't be dictionary keys
            viewList.append(rounded_tuple) # list of tuples of play/pause events
            expanded = expandList(viewList)
            cdict= Counter(expanded) # dictionary of views at every sec
            viewsDict[video] = cdict
        break
    totalViews=dict((k, dict(v)) for k, v in viewsDict.iteritems()) # gets rid of "counter" word
    return totalViews
    
        
     
    ######## FINDS INTESECTIONS
    #for interval in overlaps:
    #    range1 = set(range(interval[0][0],interval[0][1]))
    #    range2 = set(range(interval[1][0],interval[1][1]))
    #    print range1.intersection(range2)
    ########
    
# TESTING
json_data = open("finalData.json").read() 
videoInfo = json.loads(json_data)  
#print videoViewDicts(videoInfo)  
allViews = videoViewDicts(videoInfo)
json.dump(allViews,open('allViews.json','w'))#dump takes object and open file for writing  