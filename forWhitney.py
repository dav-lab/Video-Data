import json
import ast
import os

listOfFileNames=os.listdir('examtakers')

def videos(listFileName):
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