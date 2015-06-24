import json
import datetime
import ast
import requests
import xmltodict
import bisect
import os
import isodate
from math import floor, ceil
from collections import Counter


APIKEY='Key'

def getLengths(codeFile):
    code=json.load(open(codeFile))
    v={}
    for i in code.keys():
        information=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+i+'&key='+APIKEY).content)
        if len(information['items'])!=0:
            length=information['items'][0]['contentDetails']['duration']
    	    parsedT=isodate.parse_duration(length)
            secs=parsedT.total_seconds()
            v[i]=secs
    return v



def generateVideoDict(fileName):
    filename=json.load(open(fileName))
    video={}
    code=''
    found=False
    current=0
    for i in range(len(filename)):
        if filename[i]['event_type']=='pause_video' or filename[i]['event_type']=='play_video':
            d = json.loads(ast.literal_eval(filename[i]['event']))
            videoDict=dict((k,v) for (k,v) in d.items())
            if code!='' and code!=videoDict['code']:
                video[code].append(('watched another video',datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0)))            
            code=videoDict['code']
            found=True
            try:
                current=float(videoDict['currentTime'])
            #when currentTime is not there
            except (KeyError, TypeError):
                if filename[i]['event_type']=='pause_video' and filename[i-1]['event_type']=='play_video':
                    diff=datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0)-datetime.datetime.utcfromtimestamp(filename[i-1]['timestamp']/1000.0)
                    current+=diff.total_seconds()
                elif filename[i]['event_type']=='play_video' and filename[i-1]['event_type']=='pause_video':
                    current=current
                elif filename[i]['event_type']=='play_video' and filename[i-1]['event_type']=='play_video':
                    diff=datetime.datetime.utcfromtimestamp(filename[i+1]['timestamp']/1000.0)-datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0)
                    current=diff.total_seconds()
                else:
                    continue
            if code not in video:
                video[code]=[(filename[i]['event_type'],datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0),current)]
            else:
                video[code].append((filename[i]['event_type'],datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0),current))
        else:
            if found:
                video[code].append((filename[i]['event_type'],datetime.datetime.utcfromtimestamp(filename[i]['timestamp']/1000.0)))
                found=False
                code=''
    return video

def parseTimes(listTuples):
    intervals=[]
    type1='play_video'
    type2='pause_video'
    length=len(listTuples)
    i=0
    while i<length-1:
        if listTuples[i][0]==type1:
            start=listTuples[i][2]
            if listTuples[i+1][0]==type2:
                end=listTuples[i+1][2]
            else:
                diff=listTuples[i+1][1]-listTuples[i][1]
                end=start+diff.total_seconds()
            intervals.append([start,end])
            i+=1
        else:
            i+=1
    return intervals
    
length=json.load(open('Video-Data/length.json'))

def parseAllVid(videoDict):
    all={}
    for key in videoDict:
        vidLength=length[key]
        intervals=parseTimes(videoDict[key])
        for i in intervals:
            if i[1]>vidLength:
                i[1]=vidLength
        all[key]=intervals
    return all

listOfFileNames=os.listdir('examtakers')

def allUsers(listOfFiles):
    for i in listOfFiles:
        d=generateVideoDict('examtakers/'+i)
        combinedD=parseAllVid(d)
        with open('newData/'+i, 'w') as outfile:
            json.dump(combinedD, outfile)
            
def countViews(filename):
    data = json.load(open(filename))            
    peaksDct = {}
    for key in data.keys():
        values = data[key]
        counterSeg = Counter()
        for seg in values:
            print seg
            seg = [int(floor(seg[0])), int(ceil(seg[1]))]
            end = seg[1]
            for el in range(seg[0], end+1):
                counterSeg[el] += 1
        peaksDct[key] = counterSeg
    return peaksDct

# After running countViews(), loop through the dictionary that it creates
# and only count the seconds with more than 1 view (aka the re-swatches)
