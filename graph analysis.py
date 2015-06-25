import json

with open('viewsAll.json') as data_file:    
    data = json.load(data_file)

videoDict = data

testValuesDict = videoDict['JRmOHsNA2eM']

orderedList = []
for key in sorted(sorted(testValuesDict.keys()), key=len):
    orderedList.append((key, testValuesDict[key]))

def extremeViews(dictionary):
    '''Returns the maximum watch with the relevant time stamps, adn the minimum watch with the relevant time stamps'''
    globalMaxWatch = max(testValuesDict.values())
    globalMinWatch = min(testValuesDict.values())

    globalMaxWatchSegmentList = []
    next(globalMaxWatchSegmentList.append(keys) for keys in testValuesDict.keys() if testValuesDict[keys] == globalMaxWatch)
            
    globalMinWatchSegmentList = []
    next(globalMinWatchSegmentList.append(keys) for keys in testValuesDict.keys() if testValuesDict[keys] == globalMinWatch)

    return {globalMaxWatch: globalMaxWatchSegmentList, globalMinWatch: globalMinWatchSegmentList}
        
#print extremeViews(testValuesDict)

def gradients(dictionary):
    # This works second by second. Code might be more effective if we had larger bins. Look into normalizing.
    '''Returns the minimum difference with the relevant time stamps, and the maximum difference with the relevant time stamps'''
    maxDifference = 0
    minDifference = 0
    difference = 0
    
    for tupl in orderedList:
        if orderedList.index(tupl) != 0:
            difference = tupl[1] - orderedList[orderedList.index(tupl) - 1][1]
        if difference > maxDifference:
            maxDifference = difference
            maxValueTime = tupl[0]
            maxValueTimePrev = orderedList[orderedList.index(tupl) - 1][0]
        if difference < minDifference:
            minDifference = difference
            minValueTime = tupl[0]
            minValueTimePrev = orderedList[orderedList.index(tupl) - 1][0]
        else: pass
    
    gradDict = {maxDifference: (maxValueTimePrev, maxValueTime), minDifference: (minValueTimePrev, minValueTime)}
    return gradDict
    
#print gradients(testValuesDict)    