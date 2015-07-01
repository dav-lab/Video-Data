import json
import datetime
import collections
from collections import OrderedDict
import ast
import requests
import xmltodict
import bisect
import os
import isodate
from xml.parsers.expat import ExpatError
import pprint #for pretty printing


def wordFreqCounter(newTranscript): 
    '''Takes in a transcript and creates a dictionary with the keys as the words and the values as the frequency'''
    #cleans up the transcript  
    joiner = ' '.join(newTranscript).replace("&#39;","'").replace("\n"," ").replace("."," ").replace("?"," ").replace(","," ").replace("--"," ").replace(":"," ").replace("&quot;"," ").replace("("," ").replace(")"," ").lower()
    
    mylist = []
    mylist.append(joiner) #appending the full transcript (a string) to a list
       
    commonWords = []
    commonWordsFile = open('commonWords.txt','r').readlines()#reading the list of common words
    
    #for loop to get rid of new line character and lowercase the words
    for commonword in commonWordsFile:
        commonword = commonword.replace("\n","").lower()
        commonWords.append(commonword)    
    newDict={}  
    for line in mylist:
        words=line.split() #splits line into individual words
        for word in words:
            if word not in commonWords:
                if word in newDict:
                    newDict[word]+=1 #incrementing a key value pairing
                else:
                    newDict[word]=1 #creating a key value pairing
                                                  
    return OrderedDict(newDict)    
    
APIKEY='AIzaSyDKoeFuf8lF9bO3cQasg5MSf6SDjgBjDgc'
videoReader = open('videos.json').read()
videoLoader = json.loads(videoReader)
videoIDs =[]
videoIDsAndTitles = []
for i in videoLoader: #appends videoIDs to the list videoIDs
    videoIDs.append(i)

for i in videoLoader.values():
    videoIDsAndTitles.append((i,i['title'].split('-')[4]))

transcriptDict = {} #Dictionary for videoIDs and transcript of video
transcriptFreqDict = {} #Dictionary within a dictionary. Video id is first key. Second key is words in transcript, value is number of times it occurs
transcriptTimesDict = {} #tuple within a dictionary. First key is Video ids and the value is a list of tuples with the first index as the time and the second index is a lin of the transcript 
transcriptSubDict = {}
for VIDEOID in videoIDs: #Goes through individual videoIDs in the list
    info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
    try:
        if info['items'][0]['contentDetails']['caption']=='true': #checks if the video has the caption(transcript) info
            subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content
            a=xmltodict.parse(subs)
            listOfSubs=a['transcript']['text']   
            transcriptList = []# list for transcript
            transcriptTimesList=[]# list for the tuple (start time, transcript line)
            i = 1
            while i <  len(listOfSubs)-1: #while loop traverses listOfSubs(not including first and last element because they don't have text)
                transcript = listOfSubs[i].items()[2][1] #listOfSubs[i].items()[2][1] accesses ordered dict
                transcriptList.append(transcript)
                value = (listOfSubs[i].items()[0][1],listOfSubs[i].items()[2][1].replace("&#39;","'").replace("\n"," ").replace("."," ").replace("?"," ").replace(","," ").replace("--"," ").replace(":"," ").replace("("," ").replace("&quot;"," ").lower()) 
                transcriptTimesList.append(value)
                i += 1 
            transcriptSubDict[VIDEOID] =  subs+"\n"       
            transcriptDict[VIDEOID] = transcriptList
            transcriptFreqDict[VIDEOID] = wordFreqCounter(transcriptList)
            transcriptTimesDict[VIDEOID] = transcriptTimesList
    except (IndexError, ExpatError, KeyError), e:
        transcriptDict[VIDEOID] = ['NTA']
        
def printDict():
    pprint.pprint(transcriptDict) #pretty prints the transcriptDict        

def oneTranscript(): #Code for looking at transcript of one video
    newTranscript = []
    VIDEOID = 'zhKN60gDjk8'
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
                newTranscript.append(transcript)
                #print newTranscript
                i += 1
            print ''           
    except (IndexError, ExpatError), e:
        print 'indexError on ',VIDEOID 
    wordFreqCounter(newTranscript)