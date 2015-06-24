import json

with open('viewsAll.json') as data_file:    
    data = json.load(data_file)

videoDict = data

testValuesDict = videoDict['JRmOHsNA2eM']

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
    '''Returns the minimum difference with the relevant time stamps, and the maximum difference with the relevant time stamps'''
    maxDifference = 0
    minDifference = 0
    difference = 0

    # Using values    
    for value in testValuesDict.values():
        if (testValuesDict.values()).index(value) != 0:
            difference = value - testValuesDict.values()[((testValuesDict.values()).index(value))-1]
            print difference
            #print ((testValuesDict.values()).index(value), testValuesDict.values()[((testValuesDict.values()).index(value))-1])
        if difference > maxDifference:
            maxDifference = difference
            maxValueTime = next(k for k, v in testValuesDict.iteritems() if v == value)
            maxValueTimePrev = next(k for k, v in testValuesDict.iteritems() if v == testValuesDict.values()[((testValuesDict.values()).index(value))-1])
            #print (testValuesDict.values()).index(value)
        if difference < minDifference:
            minDifference = difference
            minValueTime = next(k for k, v in testValuesDict.iteritems() if v == value)
            minValueTimePrev = next(k for k, v in testValuesDict.iteritems() if v == testValuesDict.values()[((testValuesDict.values()).index(value))-1])
            
    # Using keys
    for key in testValuesDict.keys():
        #print key
        if testValuesDict.keys().index(key) != 0:
            # Difference in views
            difference = testValuesDict[key] - testValuesDict[testValuesDict.keys()[testValuesDict.keys().index(key) - 1]]
            print difference
        if difference > maxDifference:
            maxDifference = difference
            maxValueTime = int(key)
            maxValueTimePrev = int(key) - 1
        if difference < minDifference:
            minDifference = difference
            minValueTime = int(key)
            minValueTimePrev = int(key) - 1
            
    gradDict = {maxDifference: (maxValueTimePrev, maxValueTime), minDifference: (minValueTimePrev, minValueTime)}
    return gradDict
    
print gradients(testValuesDict)    