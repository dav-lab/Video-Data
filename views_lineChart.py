#Amanda Foun
#numViews_lineChart.py creates a line chart to show the peaks in video views

#open allViews.json
#grab the values of the inner dictionary

from bokeh.plotting import figure, output_file, show
import json

# gather data from allViews.json which was created in numViews.py
json_data = open("viewsAll.json").read() 
videoInfo = json.loads(json_data) 
viewsDict = videoInfo['lhERAjJFcek']

# x and y contain the points to plot on the graph
x = []
y = []

toInt = map(int, viewsDict.keys())
toInt.sort()
for k in toInt: # populate x and y
    x.append(k)
    y.append(viewsDict[str(k)]) # append the corresponding video views
print y

# create a new plot with a title and axis labels
p = figure(title="Peaks in Video Views", x_axis_label='time (sec)', y_axis_label='views')

# add a line and set line thickness
p.line(x, y, legend="lhERAjJFcek.", line_width=2)

# display chart 
output_file("views.html", title="Peaks in Video Views")
show(p)