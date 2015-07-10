import numpy
import pylab
import json

beta = [32]

videoInfo = json.loads(open("FinishedCourseData/pausePlayBins.json").read())

def smooth(x,beta):
    """ kaiser window smoothing """
    window_len=11
    # extending the data at beginning and at the end
    # to apply the window at the borders
    s = numpy.r_[x[window_len-1:0:-1],x,x[-1:-window_len:-1]]
    w = numpy.kaiser(window_len,beta)
    y = numpy.convolve(w/w.sum(),s,mode='valid')
    return y[5:len(y)-5]
    
 # random data generation
dataX= map(float,videoInfo["SVQuLOiHJeE"].keys())
dataX.sort()
dataY= []
for elt in dataX:
    pt = videoInfo["SVQuLOiHJeE"][str(elt)]
    dataY.append(pt)
    
x = numpy.array(dataX)
y = numpy.array(dataY)

# smoothing the data
pylab.figure(1)
pylab.plot(y,'-k',label="original signal",alpha=.3)
for b in beta:
 yy = smooth(y,b) 
 pylab.plot(yy,label="filtered (beta = "+str(b)+")")
pylab.legend()
pylab.show()

print x
print '*****'
print yy