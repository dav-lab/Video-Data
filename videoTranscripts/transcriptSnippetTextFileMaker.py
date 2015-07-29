import json
from stemming.porter2 import stem
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer
import itertools

peaksDict=json.load(open('pausePlaySmoothPeaks.json'))
transcriptDict=json.load(open('videoTranscripts/transcriptsTime.json'))

class LemmaTokenizer(object):
     def __init__(self):
         self.wnl = WordNetLemmatizer()
     def __call__(self, doc):
         return [self.wnl.lemmatize(t) for t in word_tokenize(doc)] 

'''The following code is created the text files for all the snippets at peaks
in the graph. It writes the line of transcript at the peak plus a couple lines
before and after'''
for videoId in peaksDict:
    for sec in peaksDict[videoId]:
        listOfTranscripts=transcriptDict[videoId]
        if len(listOfTranscripts)!=0:
            try:
                index=[i for i, t in enumerate(listOfTranscripts) if sec[0]==t[0]][0]
                if index-5<0:
                    start=0
                else:
                    start=index-6
                if index+6>=len(listOfTranscripts):
                    end=len(listOfTranscripts)-1
                else:
                    end=index+7
                words=[listOfTranscripts[i][2].split() for i in range(start,end)]
                wordList=list(itertools.chain.from_iterable(words))
                textList=[stem(LemmaTokenizer()(x)[0]) for x in wordList]
                with open('text2/'+videoId+'('+sec[0]+').txt', 'w') as outfile:
                    outfile.write(' '.join(textList))
            except IndexError:
                 pass
