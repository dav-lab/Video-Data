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

#creating a list of common words removing the new line
commonWords = open('../videoTranscripts/commonWordsReduced.txt','r').readlines()
commonWordsList = []
for i in commonWords:
    commonWordsList.append(i.replace('\n',''))

#Gets the text files from current directory 
textFilesList = os.listdir(os.getcwd())
filenames = textFilesList

vectorizer = CountVectorizer(input='filename',lowercase=True,stop_words=commonWordsList)


dtm = vectorizer.fit_transform(filenames)
vocab = vectorizer.get_feature_names()
dtm = dtm.toarray() 
vocab = np.array(vocab)


dtm.shape


X = dtm # document term matrix
model = lda.LDA(n_topics=20, n_iter=200, random_state=1)
model.fit(X)
topic_word = model.topic_word_  # model.components_ also works
n_top_words = 11
f=open('topicModels2.txt', 'w') # files for topics and files grouped into topics

for i, topic_dist in enumerate(topic_word): #generating the topics
     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
     #print ('Topic {}: {}'.format(i, ' '.join(topic_words)))
     f.write('Topic {}: {}'.format(i, ' '.join(topic_words)))

doc_topic = model.doc_topic_
for i in range(len(filenames)): #grouping transcript in to topics
    #print ("{} (top topic: {})".format(filenames[i], doc_topic[i].argmax())+'\n')
     f.write("{} (top topic: {})".format(filenames[i], doc_topic[i].argmax())+'\n')
f.closed 
