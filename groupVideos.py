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
            temp = {}
            vidLen = ids[title]['length']
            for i in ids[title]['ID']: 
                vidLen2 = length[i]['length']
                if vidLen != vidLen2:
                    ratio = float(vidLen)/vidLen2
                    for sec in counts[i]:
                        updated = int(round(int(sec)*ratio))
                        if updated not in temp:
                            temp[updated] = counts[i][sec]
                        else:
                            temp[updated] += counts[i][sec]
                else:
                    key=i # video ID with the transcript
                    for sec in counts[i]:
                        if int(sec) not in temp:
                            temp[int(sec)] = counts[i][sec]
                        else:
                            temp[int(sec)] += counts[i][sec]
            groupCounts[key] = temp
            
        except KeyError: # transcript does not exist
            pass
            
    with open('groupPeaks.json', 'w') as outfile:
            json.dump(groupCounts, outfile)

groupVideos()