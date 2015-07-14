import numpy as np

from bokeh.plotting import figure, output_file, show, VBox
from bokeh.sampledata.olympics2014 import data
import json

def createHistogram(key):
    data =json.load(open('FinishedCourseData/pausePlayBins.json'))[key]
    
    x=sorted([float(num) for num in data.keys()])
    strX=[str(i) for i in x]
    
    y = np.array([data[i] for i in strX], dtype=np.float)
    
    
    output_file('pausePlay.html')
    
    p2 = figure(title="PausePlay for "+key, tools="",
                x_range=strX, y_range=[0, int(max(y))],
                background_fill='#59636C', plot_width=1600, plot_height=800)
    
    xSize = [c+":0.5" for c in strX]
    
    p2.rect(x=xSize, y=y/2, width=0.2, height=y, color="gold", alpha=0.8)
    
    p2.xgrid.grid_line_color = None
    p2.axis.major_label_text_font_size = "8pt"
    p2.axis.major_label_standoff = 0
    p2.xaxis.major_label_orientation = np.pi/3
    p2.xaxis.major_label_standoff = 5
    p2.xaxis.major_tick_out = 0
    
    # show the plots arrayed in a VBox
    show(VBox(p2))

createHistogram('SVQuLOiHJeE')