# -*- coding: utf-8 -*-
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import json
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from stemming.porter2 import stem
import numpy as np
import lda
import lda.datasets

"""
wordFreq = open('../Video-Data/videoTranscripts/transcriptsWordFrequency.json').read()
wordFreqDict = json.loads(wordFreq)
wordFreqList = wordFreqDict.values()
vocabList=[]
for i in wordFreqList:
    vocabList.append(i[0][0])
    
vocabList = set(vocabList)
"""
class LemmaTokenizer(object):
     def __init__(self):
         self.wnl = WordNetLemmatizer()
     def __call__(self, doc):
         return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]
         
#wordFreqDict = json.load(open('../transcriptNewWordFreq.json'))
#vocabs = []
#for key in wordFreqDict:
#    vocabs.extend(wordFreqDict[key].keys())
#    
#vocabList = list(set(vocabs))
#
#
#    
#

commonWords = open('../videoTranscripts/commonWordsReduced.txt','r').readlines()
commonWordsList = []
for i in commonWords:
    commonWordsList.append(i.replace('\n',''))

#d = Counter()
#for key in wordFreqDict:
#    vD = wordFreqDict[key]
#    d.update(vD)
#
textFilesList = os.listdir(os.getcwd())
filenames = textFilesList
#lemList = []
#for i in vocabList:
#    lemList.append(LemmaTokenizer()(i)[0])
#
#lemList= list(set(lemList))
#stemList = []
#for i in lemList:
#        stemList.append(stem(i))
#stemList = list(set(stemList))

vectorizer = CountVectorizer(input='filename',lowercase=True,stop_words=commonWordsList)


dtm = vectorizer.fit_transform(filenames)
vocab = vectorizer.get_feature_names()
dtm = dtm.toarray() 
vocab = np.array(vocab)
#

dtm.shape

#vocab = lda.datasets.load_reuters_vocab()
#titles = lda.datasets.load_reuters_titles()
#X.shape
#snippetDict = json.load(open('../transcriptsPeakSnippets.json'))
#snippetList = []
#for i in snippetDict.keys():
#     snippetList.append(i + ': ' + snippetDict[i])
#titles = tuple(snippetList)

X = dtm # document term matrix
model = lda.LDA(n_topics=5, n_iter=1000, random_state=1)
model.fit(X)
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 9
#f=open('topicModels.txt', 'w') 

for i, topic_dist in enumerate(topic_word): #generating the topics
     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
     print ('Topic {}: {}'.format(i, ' '.join(topic_words)))
     #f.write('Topic {}: {}'.format(i, ' '.join(topic_words)))

#doc_topic = model.doc_topic_
#for i in range(len(filenames)): #grouping transcript in to topics
#     f.write("{} (top topic: {})".format(filenames[i], doc_topic[i].argmax())+'\n')
#f.closed 
         
#def wordFinder(word):
#    word = stem(word)
#    newList = []
#    for i in snippetDict.keys():
#        if word in snippetDict[i]:
#            newList.append(i +': ' + snippetDict[i])
#    return newList
#        