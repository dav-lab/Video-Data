import json
import pandas as pd
import csv
from collections import OrderedDict


#json_data = open('videoTitles.json').read()
#info=json.loads(json_data)
#weekDict = {}

#try: 
#    for i in info.values():
#        print i
#        if not i[1]['week'] in weekDict:
#            weekDict[i[1]['week']] = {}
#except KeyError:
#   pass
#            


csv_data = open('weekly_videos1.csv').read()
df= pd.read_csv('weekly_videos1.csv')
weekDict = {}

listOfNum = []
for i in range(1,24):
    listOfNum.append('Lecture_' + str(i))
    
def csvToDict():
    reader = csv.reader(open('weekly_videos1.csv', 'rU'), dialect=csv.excel_tab)
    d={}
    for line in reader:
        #print line
        toList = line[0].split(',')
        #d[toList[2]]= {'week':toList[0].strip('/'),'topic':toList[1].strip('/')} # key=title, value=week and topic
        d[toList[0].strip('/')]= toList[1].strip('/')# key=title, value=week and topic
        #d=OrderedDict(d)
            
    return d
    
json_data = open('Transcripts_JSON/transcriptsWordFreq.json').read()
info=json.loads(json_data)


    