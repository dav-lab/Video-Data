# -*- coding: utf-8 -*-
# Amanda and Ella
# Plots a histogram of the total time spent watching videos in minutes

import numpy as np
import scipy.special
import json

from bokeh.plotting import figure, show, output_file, vplot

filename=json.load(open('totalTime.json'))

output_file('histogram.html')

p1 = figure(title="Total Time Spent Watching Videos",tools="save", background_fill="#E8DDCB")

measured = filename.values()[:4000] # Bokeh caps the data at 4000, so we are unable to plot all 6000 students


hist, edges = np.histogram(measured, bins=200)


p1.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
     fill_color="#036564", line_color="#033649",\
)

p1.legend.orientation = "top_left"
p1.xaxis.axis_label = 'Time (min)'
p1.yaxis.axis_label = 'Number of Students'

show(p1)