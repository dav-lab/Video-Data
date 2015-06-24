#Amanda Foun
#views_lineChart.py creates a line chart to show the peaks in video views

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components # generates individual component
import json

json_data = open("viewsAll.json").read() 
videoInfo = json.loads(json_data)

def makeScripts():
    '''Creates a text file that contains all the scripts for the videos'''
    scripts = open('graphScripts.txt', 'w')
    for video in videoInfo:
        script, div = graphViews(video)
        scripts.write(script + '\n')
        scripts.write(div + '\n')
    scripts.close()
    
def graphViews(videoID):
    viewsDict = videoInfo[videoID]
      
    # x and y contain the points to plot on the graph
    x = []
    y = []
    
    toInt = map(int, viewsDict.keys())
    toInt.sort()
    for k in toInt: # populate x and y
        x.append(k)
        y.append(viewsDict[str(k)]) # append the corresponding video views
        
    # create a new plot with a title and axis labels
    p = figure(title="Peaks in Video Views", x_axis_label='time (sec)', y_axis_label='views')
    
    # add a line and set line thickness
    p.line(x, y, legend=videoID, line_width=2)
    
    # display chart 
    #output_file("views.html", title="Peaks in Video Views")
    #show(p)
    script, div = components(p)
    return script, div

makeScripts()