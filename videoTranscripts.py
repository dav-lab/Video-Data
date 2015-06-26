import json
import datetime
import collections
import ast
import requests
import xmltodict
import bisect
import os
import isodate
from xml.parsers.expat import ExpatError
import pprint #for pretty printing

APIKEY='AIzaSyDKoeFuf8lF9bO3cQasg5MSf6SDjgBjDgc'
videoReader = open('videos.json').read()
videoLoader = json.loads(videoReader)
videoIDs =[]

#for i in videoLoader: #appends videoIDs to the list videoIDs
#    videoIDs.append(i)
#
transcriptDict = {} #Dictionary for videoIDs and transcript of video
#
#for VIDEOID in videoIDs: #Goes through individual videoIDs in the list
#    info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
#    try:
#        if info['items'][0]['contentDetails']['caption']=='true': #checks if the video has the caption(transcript) info
#            subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
#            a=xmltodict.parse(subs)
#            listOfSubs=a['transcript']['text']   
#            transcriptList = []
#            i = 1
#            while i <  len(listOfSubs)-1: #while loop traverses listOfSubs(not including first and last element because they don't have text)
#                transcript = listOfSubs[i].items()[2][1] #listOfSubs[i].items()[2][1] accesses ordered dict
#                newTranscript = transcript.replace("&#39;","'")
#                transcriptList.append(newTranscript)
#                i += 1          
#            transcriptDict[VIDEOID] = [transcriptList]
#   
#    except (IndexError, ExpatError), e:
#        #print 'indexError on ',VIDEOID
#        transcriptDict[VIDEOID] = ['NTA']
#        
#def printDict():
#    pprint.pprint(transcriptDict) #pretty prints the transcriptDict   

def wordFreqCounter(mylist):
    newDict={}
    for i in mylist:
        words=i.split()
        for word in words:
            if word in newDict:
                newDict[word]+=1
            else:
                newDict[word]=1
                                      
    #print newDict
    print collections.OrderedDict(sorted(newDict.items()))  


#Code for looking at transcript of one video

mytranscript = []
VIDEOID = 'B03dhB-YmMM'
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
            mytranscript.append(newTranscript)
            #print newTranscript
            i += 1
        print ''
        
except (IndexError, ExpatError), e:
    print 'indexError on ',VIDEOID

joiner = ''.join(mytranscript).replace("\n"," ").replace("."," ").replace("?"," ").replace(","," ").replace("--"," ").lower()
newlist = []
newlist.append(joiner)
#print 'newlist \n',newlist
wordFreqCounter(newlist)

#Code for getting the time in video
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