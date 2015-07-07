# Amanda and Ella
# July 1st, 2015
# Finding the frequency of bigrams helps with creating video descriptions

import json
import re # allows us to filter words
from collections import Counter

def makeTranscript(transcriptFile):
    '''Updates the transcript file that separates each line by time.
    Creates a json file of the transcript that separates each line by sentence.'''
    transcript=json.load(open(transcriptFile))
    sentences={}
    for vid in transcript:
        fullString = ' '.join(transcript[vid])
        sentences[vid]=fullString.split('.')
    with open('transcriptsSentences.json', 'w') as outfile:
            json.dump(sentences, outfile)
        
def bigram(transcriptFile):
    '''Creates a json file where the keys are video IDs and values are frequency of bigrams
       :param transcriptFile: json file created by makeTranscript(), transcriptsSentences.json'''
    transcript=json.load(open(transcriptFile))
    d={}
    for vid in transcript:
        l=[] # list of all the bigrams
        
        # filter out common words
        remove = re.compile("(of|the)\W", re.I)
        filtered = map(lambda phrase: remove.sub("", phrase),  transcript[vid]) 
        
        for sentence in filtered: # loop through list of sentences
            listTups=zip(sentence.split(),sentence.split()[1:])
            for tup in listTups:
                l.append(' '.join(tup))
        d[vid]=Counter({k:v for k,v in Counter(l).iteritems() if v not in (1,2)}) # filter out bigrams with frequency <=3
    with open('bigrams.json', 'w') as outfile:
            json.dump(d, outfile)
            
#makeTranscript('transcript_JSON/transcriptsParagraph.json')
bigram('transcriptsSentences.json')
    