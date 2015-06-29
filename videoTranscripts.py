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






def wordFreqCounter(newTranscript,VIDEOID):   
    joiner = ' '.join(newTranscript).replace("&#39;","'").replace("\n"," ").replace("."," ").replace("?"," ").replace(","," ").replace("--"," ").replace(":"," ").replace("&quot;"," ").replace("("," ").replace(")"," ").lower()
    mylist = []
    mylist.append(joiner)
    
    commonWords = []
    commonWordsFile = open('commonWords.txt','r').readlines()
    
    for i in commonWordsFile:
        i = i.replace("\n","").lower()
        commonWords.append(i)
    
    newDict={}
    for i in mylist:
        words=i.split()
        for word in words:
            if word not in commonWords:
                if word in newDict:
                    newDict[word]+=1
                else:
                    newDict[word]=1
                newDict[word].(getWordOccurreneceTime(VIDEOID,word))
                                      
    return newDict
    #print collections.OrderedDict(sorted(newDict.items()))  






APIKEY='AIzaSyDKoeFuf8lF9bO3cQasg5MSf6SDjgBjDgc'
videoReader = open('videos.json').read()
videoLoader = json.loads(videoReader)
videoIDs =[]

for i in videoLoader: #appends videoIDs to the list videoIDs
    videoIDs.append(i)

transcriptDict = {} #Dictionary for videoIDs and transcript of video
transcriptFreqDict = {}
transcriptTimesDict = {}

for VIDEOID in videoIDs: #Goes through individual videoIDs in the list
    info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
    try:
        if info['items'][0]['contentDetails']['caption']=='true': #checks if the video has the caption(transcript) info
            subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
            a=xmltodict.parse(subs)
            #print 'a is',a
            #print subs
            listOfSubs=a['transcript']['text']   
            transcriptList = []
            transcriptTimesList=[]
            i = 1
            while i <  len(listOfSubs)-1: #while loop traverses listOfSubs(not including first and last element because they don't have text)
                transcript = listOfSubs[i].items()[2][1] #listOfSubs[i].items()[2][1] accesses ordered dict
                #newTranscript = transcript.replace("&#39;","'")
                transcriptList.append(transcript)
                value = (listOfSubs[i].items()[0][1],listOfSubs[i].items()[2][1].replace("&#39;","'").replace("\n"," ").replace("."," ").replace("?"," ").replace(","," ").replace("--"," ").replace(":"," ").replace("&quot;"," ").replace("("," ").replace("&quot;"," ").lower()) 
                transcriptTimesList.append(value)
                i += 1         
            transcriptDict[VIDEOID] = transcriptList
            transcriptFreqDict[VIDEOID] = wordFreqCounter(transcriptList,VIDEOID).items()
            #transcriptTimesDict[VIDEOID] = value
            transcriptTimesDict[VIDEOID] = transcriptTimesList
    except (IndexError, ExpatError), e:
        #print 'indexError on ',VIDEOID
        transcriptDict[VIDEOID] = ['NTA']
        
def printDict():
    pprint.pprint(transcriptDict) #pretty prints the transcriptDict 
    
    
def getWordOccurreneceTime(ids,word):
    #uniqueIds = transcriptFreqDict.keys()
    #for ids in uniqueIds:     
        #for j in range(len(transcriptFreqDict[ids])): #loops through words
            for i in range(len(transcriptTimesDict[ids])): #loops through lines
                print 'looking at this line: ',transcriptTimesDict[ids][i][1]
                if word in transcriptTimesDict[ids][i][1]: # if word in transcript line 
                    #transcriptFreqDict[ids][j][0] is the word
                    #print 'the word:',transcriptFreqDict[ids][j][0],'occurence at line:',i,'at',transcriptTimesDict[ids][i][0]
                    #print 'the line is',transcriptTimesDict[ids][i][1],'\n'
                    return transcriptTimesDict[ids][i][0]
                #else:
                #    #print transcriptFreqDict[ids][j][0],'is not in line',i
                #    pass

 


##Code for looking at transcript of one video
#newTranscript = []
#VIDEOID = 'zhKN60gDjk8'
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
#            newTranscript.append(transcript)
#            #print newTranscript
#            i += 1
#        print ''
#        
#except (IndexError, ExpatError), e:
#    print 'indexError on ',VIDEOID
#
#wordFreqCounter(newTranscript)


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