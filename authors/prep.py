# -*- coding: cp1252 -*-
import math
import string
import cPickle as pickle
import nltk.data
import nltk
from nltk.collocations import *
import time


hemway = ['Works/hemingway_1.txt','Works/hemingway_2.txt','Works/hemingway_3.txt',
          'Works/hemingway_4.txt','Works/hemingway_5.txt','Works/hemingway_6.txt',
          'Works/hemingway_7.txt','Works/hemingway_8.txt','Works/hemingway_9.txt',
          'Works/hemingway_10.txt','Works/hemingway_11.txt','Works/hemingway_12.txt',
          'Works/hemingway_13.txt','Works/hemingway_14.txt','Works/hemingway_15.txt',
          'Works/hemingway_16.txt','Works/hemingway_17.txt','Works/hemingway_18.txt',
          'Works/hemingway_19.txt','Works/hemingway_20.txt']

meyer = ['Works/meyer_1.txt','Works/meyer_2.txt','Works/meyer_3.txt',
          'Works/meyer_4.txt','Works/meyer_5.txt','Works/meyer_6.txt',
          'Works/meyer_7.txt','Works/meyer_8.txt','Works/meyer_9.txt',
          'Works/meyer_10.txt','Works/meyer_11.txt','Works/meyer_12.txt',
          'Works/meyer_13.txt','Works/meyer_14.txt','Works/meyer_15.txt',
          'Works/meyer_16.txt','Works/meyer_17.txt','Works/meyer_18.txt',
          'Works/meyer_19.txt','Works/meyer_20.txt']


stopwords = ["the", "be", "to", "of",]

def docToDic_stopwords (f):
    f = open(f, 'r')
    dic = {}
    splitList = []
    intab = "“’”"
    outtab = '''"'"'''
    trantab = string.maketrans(intab, outtab)
    for line in f:
        splitList = line.strip().translate(trantab).split()
        for out in splitList:
            if out.lower() not in stopwords:
                var = out
                if var in dic:
                    dic[var] = dic[var] + 1
                else:
                    dic[var] = 1
    pickle.dump(dic, open( "dic_stopwords.p", "wb" ))

def docToDic_clean (f):
    f = open(f, 'r')
    dic = {}
    splitList = []
    par = f.read().translate(None, '?.!/;:()#$%^*"<>{}[]“”…').replace("’","'").replace("—"," ")
    for x in par.split():
        if not x.islower():
            continue
        if x.lower() not in stopwords:
            var = x
            if var in dic:
                dic[var] = dic[var] + 1
            else:
                dic[var] = 1
    pickle.dump(dic, open( "dic_clean.p", "wb" ))    

def num_words(f):
    f = open(f, 'r')
    num = len(f.read().split())
    print num
    return num


def avg_words(f):
    f = open(f, 'r')
    dic = {}
    par = f.read().translate(None, '?.!/;:()#$%^*"<>{}[]“”…').replace("’","'").replace("—"," ")
    i = 0
    for x in par.split():
        count = len(x)
        if count in dic:
            dic[count] = dic[count] + 1
        else:
            dic[count] = 1
        i += 1
    pickle.dump(dic, open( "avg_words.p", "wb" ))


def var_words(f):
    f = open(f, 'r')
    dic = {}
    par = f.read().translate(None, '?.!/;:()#$%^*"<>{}[]“”…').replace("’","'").replace("—"," ")
    i = 0
    for x in par.split():
        if i == 0:
            prev = len(x)
            i = 1
            continue
        count = abs(len(x) - prev)
        prev = len(x)
        if count in dic:
            dic[count] = dic[count] + 1
        else:
            dic[count] = 1
        i += 1
    pickle.dump(dic, open( "var_words.p", "wb" ))
            
def var_sen(f):
    f = open(f, 'r')
    dic = {}
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    x = sent_detector.tokenize(f.read().strip())
    i = 0
    for y in x:
        if i == 0:
            prev = len(y.split())
            i += 1
            continue
        count = abs(len(y.split()) - prev)
        if count in dic:
            dic[count] = dic[count] + 1
        else:
            dic[count] = 1
        i += 1
        prev = len(y.split())
    pickle.dump(dic, open( "var_sen.p", "wb" ))


def bigram_clean(f,num):
    f = open(f, 'r')
    dic = {}
    par = f.read().translate(None, '?.!/;:()#$%^*"<>{}[]“”…').lower().replace("’","'").replace("—"," ")
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(par.split())
    finder.apply_freq_filter(2)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    for x in scored:
        if x[0] in dic: 
            dic[x[0]] += num *x[1]
        else:
            dic[x[0]] = num *x[1]
    pickle.dump(dic, open( "bi_clean.p", "wb" ))

def bigram(f,num):
    f = open(f, 'r')
    dic = {}
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(f.read().split())
    finder.apply_freq_filter(2)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    for x in scored:
        if x[0] in dic: 
            dic[x[0]] += num *x[1]
        else:
            dic[x[0]] = num*x[1]
    pickle.dump(dic, open( "bi.p", "wb" ))


def trigram_clean(f,num):
    f = open(f, 'r')
    dic = {}
    par = f.read().translate(None, '?.!/;:()#$%^*"<>{}[]“”…').lower().replace("’","'").replace("—"," ")
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(par.split())
    finder.apply_freq_filter(2)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    for x in scored:
        if x[0] in dic: 
            dic[x[0]] += num *x[1]
        else:
            dic[x[0]] = num *x[1]
    pickle.dump(dic, open( "tri_clean.p", "wb" ))

docToDic_stopwords('Works/meyer_full.txt')
docToDic_clean('Works/meyer_full.txt')
num = num_words('Works/meyer_full.txt')
avg_words('Works/meyer_full.txt')
var_words('Works/meyer_full.txt')
var_sen('Works/meyer_full.txt')
bigram('Works/meyer_full.txt',num)
bigram_clean('Works/meyer_full.txt',num)
trigram_clean('Works/meyer_full.txt',num)
