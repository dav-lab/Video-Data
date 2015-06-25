import json
import datetime
import ast
import requests
import xmltodict
import bisect
import os
import isodate


APIKEY='AIzaSyDKoeFuf8lF9bO3cQasg5MSf6SDjgBjDgc'
VIDEOID='lhERAjJFcek'
info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
vidLength=info['items'][0]['contentDetails']['duration']

videoIDs = open('videos.json').read()
#videoIds2 = json.loads(videoIDs)

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