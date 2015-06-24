import json
import datetime
import ast
import requests
import xmltodict
import bisect
import os
import isodate

<<<<<<< HEAD
APIKEY= 'AIzaSyCRau8nX4c2rubB_ckdUyODhwakNkjUGGI' #'APIKEY'
VIDEOID='lhERAjJFcek' #'VIDEO_ID'
=======
APIKEY='KEY'
VIDEOID='ID'
>>>>>>> origin/master
info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
vidLength=info['items'][0]['contentDetails']['duration']

if info['items'][0]['contentDetails']['caption']=='true':
    subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
    a=xmltodict.parse(subs)
    listOfSubs=a['transcript']['text']

def getSub(time,subList):
    startTimes=[]
    text=[]
    for i in subList:
        startTimes.append(float(i['@start']))
        try:
            text.append(i['#text'])
        except KeyError:
            text.append('No sub')
    breakpoints=startTimes[1:]
    i=bisect.bisect(breakpoints,time)
    return text[i]

code=json.load(open('code.json'))

def getLengths():
    v={}
    for i in code:
        information=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+i+'&key='+APIKEY).content)
        if len(information['items'])!=0:
            length=information['items'][0]['contentDetails']['duration']
    	    parsedT=isodate.parse_duration(length)
            secs=parsedT.total_seconds()
            v[i]=secs
    return v

length=getLengths()

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

def parseAllVid(videoDict):
    all={}
    for key in videoDict:
        all[key]=parseTimes(videoDict[key])
    return all

listOfFileNames=os.listdir('random1000')

def combineAllUsers(listOfFiles):
    largeList=[]
    for i in listOfFiles:
        d=generateVideoDict('random1000/'+i)
        largeList.append(parseAllVid(d))
    return largeList

def final(listDict):
    merged={}
    count={}
    for d in listDict:
        for k in d:
            if k not in merged:
                merged[k]=d[k]
                count[k]=1
            else:
                merged[k]+=d[k]
                count[k]+=1
    return count,merged


def countAndLength((count,merged),length):
    everything={}
    for k in count:
        d={}
        d['viewCount']=count[k]
        d['segments']=merged[k]
        try:
            d['length']=length[k]
        except KeyError:
            d['length']='not available'
        everything[k]=d
    return everything


def clean(all):
    for key in all:
        for i in all[key]['segments']:
            if i[1]>all[key]['length']:
                i[1]=all[key]['length']
    with open('finalData.json', 'w') as outfile:
        json.dump(all, outfile)
                