#transcript to corresponding video

import json
import requests
import xmltodict
import bisect

<<<<<<< HEAD
APIKEY= 'AIzaSyCRau8nX4c2rubB_ckdUyODhwakNkjUGGI' #'APIKEY'
=======
APIKEY= 'APIKEY'
>>>>>>> origin/master
VIDEOID='lhERAjJFcek' #'VIDEO_ID'
info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)

if info['items'][0]['contentDetails']['caption']=='true':
    subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
    a=xmltodict.parse(subs)
    listOfSubs=a['transcript']['text']

def getSub(time,subList):
    '''returns the transcript (string) of the video at the given time
        :param time: given time in seconds
        :param subList: list of the entire video's transcript'''
    startTimes=[]
    text=[] # contains entire transcript
    for i in subList:
        startTimes.append(float(i['@start']))
        try:
            text.append(i['#text'])
        except KeyError:
            text.append('No sub')
    breakpoints=startTimes[1:] # list of all the start times of the video
    # bisect returns an insertion point which comes after ane existing entries of time in breakpoints
    i=bisect.bisect(breakpoints,time) 
    return text[i]+text[i+1]

print getSub(15,listOfSubs)