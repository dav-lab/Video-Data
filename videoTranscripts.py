import json
import datetime
import ast
import requests
import xmltodict
import bisect
import os
import isodate
from xml.parsers.expat import ExpatError
import pprint

APIKEY='AIzaSyDKoeFuf8lF9bO3cQasg5MSf6SDjgBjDgc'
videoReader = open('videos.json').read()
videoLoader = json.loads(videoReader)
videoIDs =[]
for i in videoLoader:
    videoIDs.append(i)

transcriptDict = {}
transcriptList = []
for VIDEOID in videoIDs:
        #print VIDEOID
    #VIDEOID = 'BWBUXxyRILw'
    info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
    #vidLength=info['items'][0]['contentDetails']['duration']
    try:    
        if info['items'][0]['contentDetails']['caption']=='true':
            subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
            a=xmltodict.parse(subs)
            listOfSubs=a['transcript']['text']
            
            #while loop traverses listOfSubs(not including first and last element because they don't have text)
            #listOfSubs[i].items()[2][1] accesses ordered dict (like a tuple)
            i = 1
            while i <  len(listOfSubs)-1:
                transcript = listOfSubs[i].items()[2][1]
                newTranscript = transcript.replace("&#39;","'")
                transcriptList.append(newTranscript)
                i += 1
                
            #print '' 
            transcriptDict[VIDEOID] = [transcriptList]
            
            
    except (IndexError, ExpatError), e:
        #print 'indexError on ',VIDEOID
        transcriptDict[VIDEOID] = ['NTA']


#
#Code for looking at transcript of one video
#
#VIDEOID = 'lhERAjJFcek'
#info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
##vidLength=info['items'][0]['contentDetails']['duration']
#try:    
#    if info['items'][0]['contentDetails']['caption']=='true':
#        subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
#        a=xmltodict.parse(subs)
#        listOfSubs=a['transcript']['text']
#        
#        #while loop traverses listOfSubs(not including first and last element because they don't have text)
#        #listOfSubs[i].items()[2][1] accesses ordered dict (like a tuple)
#        i = 1
#        while i <  len(listOfSubs)-1:
#            transcript = listOfSubs[i].items()[2][1]
#            newTranscript = transcript.replace("&#39;","'")
#            print newTranscript
#            i += 1
#        print ''
#        
#except (IndexError, ExpatError), e:
#    print 'indexError on ',VIDEOID

#def getSub(time,subList):
#    startTimes=[]
#    text=[]
#    for i in subList:
#        startTimes.append(float(i['@start']))
#        try:
#            text.append(i['#text'])
#        except KeyError:
#            text.append('No sub')
#    breakpoints=startTimes[1:]
#    i=bisect.bisect(breakpoints,time)
#    return text[i]