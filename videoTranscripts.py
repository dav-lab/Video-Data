# Whitney and Diana
#Last Updated: 7/1/2015

import re
import HTMLParser
import json
import datetime
import collections
from collections import OrderedDict
from collections import Counter
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
            print type(word)
            if word not in commonWords:
                if word in newDict:
                    newDict[word]+=1 #incrementing a key value pairing
                else:
                    newDict[word]=1 #creating a key value pairing
    #OrderedDict(sorted(newDict.items())) makes the newDict alphabetized
    d = Counter(newDict)                                              
    return d.most_common()   
    
APIKEY='AIzaSyDKoeFuf8lF9bO3cQasg5MSf6SDjgBjDgc'
videoReader = open('videos.json').read()
videoLoader = json.loads(videoReader)
#videoIDs =[]
videoIDsAndTitles = []
#for i in videoLoader: #appends videoIDs to the list videoIDs
#    videoIDs.append(i)

for i in videoLoader.values():
    videoIDsAndTitles.append((i,i['title'].split('-')[4]))
    
json_data = open('transcript_JSON/transcriptsXML.json').read()
info=json.loads(json_data)

#for i in info:
videoIDs = info.keys()

transcriptDict = {} #Dictionary for videoIDs and transcript of video
transcriptFreqDict = {} #Dictionary within a dictionary. Video id is first key. Second key is words in transcript, value is number of times it occurs
transcriptTimesDict = {} #tuple within a dictionary. First key is Video ids and the value is a list of tuples with the first index as the time and the second index is a lin of the transcript 
transcriptSubDict = {}
for VIDEOID in videoIDs: #Goes through individual videoIDs in the list
    #info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+VIDEOID+'&key='+APIKEY).content)
    #try:
        #if info['items'][0]['contentDetails']['caption']=='true': #checks if the video has the caption(transcript) info
            json_data = open('transcript_JSON/transcriptsXML.json').read()
            info=json.loads(json_data)
            subs = info[VIDEOID]
            #subs=requests.get('http://video.google.com/timedtext?lang=en&v='+VIDEOID).content 
            a=xmltodict.parse(subs)
            listOfSubs=a['transcript']['text']   
            transcriptList = []# list for transcript
            transcriptTimesList=[]# list for the tuple (start time, transcript line)
            i = 1
            while i <  len(listOfSubs)-1: #while loop traverses listOfSubs(not including first and last element because they don't have text)
                #transcript = listOfSubs[i].items()[2][1] #listOfSubs[i].items()[2][1] accesses ordered dict
                #transcriptList.append(transcript)
                #value = (listOfSubs[i].items()[0][1],listOfSubs[i].items()[2][1].replace("&#39;","'").replace("\n"," ").replace("."," ").replace("?"," ").replace(","," ").replace("--"," ").replace(":"," ").replace("("," ").replace("&quot;"," ").lower()) 
                #transcriptTimesList.append(value)
                html_parser = HTMLParser.HTMLParser()            
                transcript = html_parser.unescape(listOfSubs[i].items()[2][1])
                transcript = re.compile("[^\w']|_").sub(" ",transcript).strip()
                transcript = re.compile("[0-9]+").sub(" ",transcript).strip()
                transcriptList.append(transcript)
                value = (listOfSubs[i].items()[0][1],listOfSubs[i].items()[1][1],transcript)
                transcriptTimesList.append(value)
                i += 1 
            transcriptSubDict[VIDEOID] =  subs+"\n"       
            transcriptDict[VIDEOID] = transcriptList
            transcriptFreqDict[VIDEOID] = wordFreqCounter(transcriptList)
            transcriptTimesDict[VIDEOID] = transcriptTimesList
    #except (IndexError, ExpatError, KeyError), e:
    #    transcriptDict[VIDEOID] = ['NTA']
        
#json.dump(transcriptSubDict,open('transcriptsXML.json','w'))
<<<<<<< Updated upstream
#json.dump(transcriptFreqDict,open('transcriptsWordFrequency.json','w'))
json.dump(transcriptTimesDict,open('transcriptsTime.json','w'))
=======
json.dump(transcriptFreqDict,open('transcriptsWordFrequency.json','w'))
#json.dump(transcriptTimesDict,open('transcriptsTime.json','w'))
>>>>>>> Stashed changes
#json.dump(transcriptDict,open('transcriptsParagraph.json','w'))
#json.dump(transcriptFreqDict,open('transcriptsOrderedWords.json','w'))
        
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