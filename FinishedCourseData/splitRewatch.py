from finalData import generateVideoDict, parseTimes
import os
import json
from collections import Counter
from math import floor, ceil

def firstAndLater(filename):
    '''splits up dictionary returned by generateVideoDict(filename) into first-time 
    watches and later watches'''
    new={}
    d=generateVideoDict(filename)
    for k in d:
        found=False
        temp={'firstTime':[],'later':[]}
        for i in d[k]:
            if found==False:
                if i[0]=='play_video' or i[0]=='pause_video':
                    temp['firstTime'].append(i)
                else:
                    found=True
                    temp['firstTime'].append(i)
            else:
                temp['later'].append(i)
        new[k]=temp
    return new

def intervalsForEacStudent(filename):
    d=firstAndLater(filename)
    new={}
    for k in d:
        new[k]={'firstTime':parseTimes(d[k]['firstTime']),'later':parseTimes(d[k]['later'])}
    return new

def allStudents(dirName):
    d={}
    listOfFileNames=os.listdir(dirName)
    for f in listOfFileNames:
        intervalsDict=intervalsForEacStudent(dirName+'/'+f)
        counts=countViews(intervalsDict)
        for k in counts:
            if k in d:
                try:
                    d[k]['firstTime']+=counts[k]['firstTime']
                except KeyError:
                    pass
                try:
                    d[k]['later']+=counts[k]['later']
                except KeyError:
                    pass
            else:
                d[k]={}
                try:
                    d[k]['firstTime']=counts[k]['firstTime']
                except KeyError:
                    pass
                try:
                    d[k]['later']=counts[k]['later']
                except KeyError:
                    pass
    with open('splitRewatches.json', 'w') as outfile:
            json.dump(d, outfile)


def countViews(dictionary):  
    peaksDct = {}
    for key in dictionary:
        temp={}
        for i in dictionary[key].keys():
            values = dictionary[key][i]      
            counterSeg = Counter()
            for seg in values:
                seg = [int(floor(seg[0])), int(ceil(seg[1]))] # rounds the intervals
                end = seg[1]
                for el in range(seg[0], end+1):
                    counterSeg[el] += 1
            newC=Counter({ k: v-1 for k, v in counterSeg.iteritems() if v not in (0, 1)}) # ignore seconds with 0 or 1 views
            if len(newC) != 0:
                temp[i] = newC
        peaksDct[key]=temp
    return peaksDct   

    