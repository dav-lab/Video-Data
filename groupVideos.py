# Amanda and Ella

import json

def groupVideos():
    '''Aggregates the views of the videos that are the same (but at different speeds).
    Creates a json file where the 147 keys are video IDs with transcripts and values are views
    at each second'''
    groupCounts = {}
    ids = json.load(open('videoTitles.json'))
    length = json.load(open('lengthsAndViews.json'))
    counts = json.load(open('rewatchPeaks.json'))
    for title in ids:
        try:
            videoWithTranscript = ids[title]['url'][32:] # get id of video with transcript
            temp = {}
            vidLen = ids[title]['length'] # length of video with transcript
            for i in ids[title]['ID']: # loop through list of grouped IDs
                vidLen2 = length[i]['length']
                if i != videoWithTranscript:
                    ratio = float(vidLen)/vidLen2
                    for sec in counts[i]:
                        updated = int(round(int(sec)*ratio))
                        if updated not in temp:
                            temp[updated] = counts[i][sec]
                        else:
                            temp[updated] += counts[i][sec]
                else:
                    for sec in counts[i]:
                        if int(sec) not in temp:
                            temp[int(sec)] = counts[i][sec]
                        else:
                            temp[int(sec)] += counts[i][sec]
            groupCounts[videoWithTranscript] = temp
            
        except KeyError: # transcript does not exist
            pass
            
    with open('groupPeaks.json', 'w') as outfile:
            json.dump(groupCounts, outfile)

groupVideos()