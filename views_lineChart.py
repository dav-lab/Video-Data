#Amanda Foun and Ella Chao 
#views_lineChart.py creates a line chart to show the peaks in video views

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components # generates individual component
from bokeh.models import HoverTool
from bruteforce import getPeaksForOneVideo
import json


videoInfo = json.loads(open("groupPeaks.json").read())

def makeScripts():
    '''Creates a text file that contains all the scripts for the videos'''
    scripts = open('groupRewatchPeaksGraphScripts.txt', 'w')
    for video in videoInfo:
        try: # only get the scripts of the graphs with transcrips
            script, div = withPeaks(video)
            scripts.write(script + '\n')
            scripts.write(div + '\n')
        except KeyError:
            pass
    scripts.close()
    
def noPeaks(videoID):
    '''Plots a Bokeh graph of video views'''
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

    p = figure(title="Peaks in Video Views", x_axis_label='time (sec)', y_axis_label='views', plot_width=300,plot_height=300)

    # add a line and set line thickness
    p.line(x, y, legend=videoID, line_width=2)
    
    # display chart 
    #output_file("views.html", title="Peaks in Video Views")
    #show(p)
    script, div = components(p)
    return script, div

def withPeaks(videoID):
    '''Plots a Bokeh graph of video views with the peaks''' 
    wordfreq = json.loads(open("transcriptsWordFrequency.json").read())
    titles = json.loads(open("videos.json").read())
    
    fiveWords=[wordfreq[videoID][i][0] for i in range(len(wordfreq[videoID])) if i <5]
    stringFiveWords=', '.join(fiveWords)
    viewsDict = videoInfo[videoID]
      
    # x and y contain the points to plot on the graph
    x = []
    y = []
    
    toInt = map(int, viewsDict.keys())
    toInt.sort()
    for k in toInt: # populate x and y
        x.append(int(k))
        y.append(viewsDict[str(k)]) # append the corresponding video views 
    
    # a and b contain the peaks to plot on the graph
    a = []
    b = []
    peaksList = getPeaksForOneVideo(videoID) # list of tuples
    for tup in peaksList:
        a.append(int(tup[0]))
        b.append(tup[1])    

    output_file("peaks.html")

    hover = HoverTool(
        tooltips = [
            ("(a,b)", "(@x, @y)"),
        ]
    )
    
    TOOLS = 'resize,hover, save, pan, box_zoom, wheel_zoom'
    
    p = figure(plot_width=400, plot_height=400,tools=TOOLS, title_text_font_size='12pt',title=titles[videoID]['title'][21:], x_axis_label=stringFiveWords)
    
    p.xaxis.axis_label_text_font_size='12pt'
    # add both a line and circles on the same plot
    p.line(x, y, legend=videoID, line_width=2)
    p.circle(a, b, fill_color="red", size=8)
    
    #show(p)
    script, div = components(p)
    return script, div

makeScripts()
#withPeaks('qic9_yRWj5U')

