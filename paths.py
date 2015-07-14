import json
import ast
import collections 

def getPath(filename):
    '''Takes in a student file of a list of dictionaries that specify their actions. 
    Returns a list of tuples, (event_type,event), that maps the student's path'''
    oneFile=json.load(open(filename))
    paths=[]
    for i in oneFile:
        if i['event_type']=='pause_video' or i['event_type']=='play_video':
            d = json.loads(ast.literal_eval(i['event']))
            videoDict=dict((k,v) for (k,v) in d.items())
            paths.append((i['event_type'],videoDict['code']))
        elif 'goto_position' in i['event_type']:
            d2 = json.loads(ast.literal_eval(i['event']))
            videoDict2=dict((k,v) for (k,v) in d2.items())
            paths.append((i['event_type'],'position: ' + str(videoDict2['POST']['position']))) # position refers to the tab the user clicked on
        else:
            paths.append((i['event_type'],'N/A'))
    return paths
    
def count(listOfTuples):
    '''Returns a dictionary where the keys are event types and
    values are the number of times that event has occurred for one student'''
    return collections.Counter(listOfTuples)