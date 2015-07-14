#Whitney and Diana

import csv
import natsort
import json

#Reads in json and csv files
jsonReader = open('/Users/emustafa-local/Video-Data/videoTranscripts/videoTitles.json').read()
csvReader = csv.reader(open('/Users/emustafa-local/Video-Data/videoTranscripts/weeks.csv'))

#creates a dictionary with weeks and lectures from csv file
weekDict = {}
for row in csvReader:
    key = row[0]
    if key in weekDict:
        pass
    weekDict[key] = row[1:]
   
videoDict=json.loads(jsonReader) #makes dictionary from the json
videoTitles = videoDict.keys() #makes list for titles from videoDict

for i in weekDict:
     for j in range(len(weekDict[i])):
         lectName = weekDict[i][j]
         newDict = {lectName: []}
         weekDict[i][j] = newDict

for title in videoTitles:
    try:
        weekNum = videoDict[title]['week'] #gets week
        lectNum = videoDict[title]['topic'] #gets lecture
        transID = videoDict[title]['transcripts'][-11:]
        for index in range(len(weekDict[weekNum])):
            try:
                lectureKey = weekDict[weekNum][index].keys()[0]
                if lectureKey == lectNum:
                    weekDict[weekNum][index][lectureKey].append((title,{transID: ''})) #stores title in corresponding week/lecture in weekDict
            except (AttributeError), e:
                pass
    except (KeyError), e:
        pass

wordFreqDict = json.loads(open('/Users/emustafa-local/Video-Data/videoTranscripts/transcriptsWordFrequency.json').read()) 

for week in weekDict.keys(): #How to access keys in dict: weekDict['Week_1'][0]['Lecture_1'][1][1]['f3TskgnL_3U']
    for i in range(len(weekDict[week])):
        for lect in weekDict[week][i].keys():
            for j in range(len(weekDict[week][i][lect])):
                for ids in weekDict[week][i][lect][j][1]:
                    #print weekDict[week][i][lect][j][1].keys()[0]
                    for videoID in wordFreqDict:
                        if weekDict[week][i][lect][j][1].keys()[0] == videoID:
                            weekDict[week][i][lect][j][1][videoID] = wordFreqDict[videoID]
                    
sorted_result = natsort.natsorted(weekDict.items(), key=lambda y: y)
json.dump(sorted_result,open('/Users/emustafa-local/Video-Data/videoTranscripts/transcriptSorted.json','w'))
#print sorted_result