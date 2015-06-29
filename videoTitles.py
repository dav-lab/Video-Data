# Amanda and Ella
# Previously called forWhitney.py

import json
import ast
import os
import requests
import csv

APIKEY='API'

listOfFileNames=os.listdir('examtakers')

def videos(listFileName):
    '''Creates a dictionary of dictionaries where the keys are video IDs and values are url and title'''
    code={}
    for k in listFileName:
        filename=json.load(open('examtakers/'+k))
        for i in range(len(filename)):
    	    if filename[i]['event_type']=='pause_video' or filename[i]['event_type']=='play_video':
                d = json.loads(ast.literal_eval(filename[i]['event']))
                videoDict=dict((k,v) for (k,v) in d.items())
                if videoDict['code'] not in code:
                    code[videoDict['code']]={'title':videoDict['id'],'url':'https://www.youtube.com/watch?v='+videoDict['code']}
    with open('videos.json', 'w') as outfile:
        json.dump(code, outfile)

def csvToDict(csvFile):
    reader = csv.reader(open('weekly_videos.csv', 'rU'), dialect=csv.excel_tab)
    d={}
    for line in reader:
        toList = line[0].split(',')
        d[toList[2]]= {'week':toList[0].strip('/'),'topic':toList[1].strip('/')} # key=title, value=week and topic
    return d

def videoTitles(videoInfo):
    '''Creates a dictionary of dictionaries where the keys are titles and 
    values are list of video IDs, week, length, video link, description, transcript link. 
    :param listFileName: directory with a json file for every student that details their actions/events'''
    # create a dictionary of dictionaries where the keys are titles and values are a list of video IDs
    filename=json.load(open(videoInfo))
    counts=json.load(open('lengthsAndViews.json')) 
    code={}
    weekInfo=csvToDict('weekly_videos.csv')
    for videoID in filename:
        title= filename[videoID]['title']
        titleSegment = filename[videoID]['title'][21:]
        print titleSegment
        if title not in code:
            code[title]= {"ID":[videoID]} 
            try: 
                code[title]["week"]=weekInfo[titleSegment]['week']
                code[title]["topic"]=weekInfo[titleSegment]['topic']
            except KeyError:
                pass
        else:
            code[title]['ID'].append(videoID) 
    for name in code:
        for ids in code[name]['ID']:
            info=json.loads(requests.get('https://www.googleapis.com/youtube/v3/videos?part=contentDetails%2Cstatistics&id='+ids+'&key='+APIKEY).content)
            if len(info['items'])>0 and info['items'][0]['contentDetails']['caption']=='true':        
                code[name]['transcripts'] = 'http://video.google.com/timedtext?lang=en&v='+ids
                code[name]['url']='https://www.youtube.com/watch?v='+ids
                code[name]['length']=counts[ids]['length']
                break
            
    with open('videoTitles.json', 'w') as outfile:
        json.dump(code, outfile)
        
    ## go through code dictionary values and remove IDs with lowest view count
    #counts=json.load(open('lengthsAndViews.json')) # Key= ID, Values= length and counts
    #for title in code:
    #    viewCount=[]
    #    for vidID in code[title]:
    #        if vidID in counts:
    #            viewCount.append(counts[vidID]['counts'])
    #            length = counts[vidID]['length']
    #        else:
    #            viewCount.append(0)         
    #    videoID = code[title][viewCount.index(max(viewCount))]
    
        
videoTitles('videos.json')
#print csvToDict('weekly_videos.csv')