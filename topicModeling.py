# -*- coding: utf-8 -*-
import os
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
import json

wordFreq = open('../videoTranscripts/transcriptsWordFrequency.json').read()
wordFreqDict = json.loads(wordFreq)
wordFreqList = wordFreqDict.values()


textFilesList = os.listdir(os.getcwd())
textFilesList.pop(0)
commonWords = open('../videoTranscripts/commonWords.txt','r').readlines()
commonWordsList = []
for i in commonWords:
    commonWordsList.append(i.replace('\n',''))


filenames = textFilesList
##
vectorizer = CountVectorizer(input='filename',lowercase=True,)
dtm = vectorizer.fit_transform(filenames)
#vocab = vectorizer.get_feature_names()
#dtm = dtm.toarray() 
#vocab = np.array(vocab)
#
#import lda
#dtm.shape

#vocab = lda.datasets.load_reuters_vocab()
#titles = lda.datasets.load_reuters_titles()
#X.shape
#
#model = lda.LDA(n_topics=20, n_iter=500, random_state=1)
#model.fit(X)
#topic_word = model.topic_word_  # model.components_ also works
#n_top_words = 8
#for i, topic_dist in enumerate(topic_word):
#     topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
#     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
