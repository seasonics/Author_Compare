# -*- coding: cp1252 -*-
import math
import string
import cPickle as pickle
import nltk.data
import nltk
from nltk.collocations import *
import time
import logging
logger = logging.getLogger(__name__)
stopwords = ["the", "be", "to", "of",]

def docToDic_stopwords (f):
    dic = {}
    splitList = []
    f = f.encode('ascii', 'ignore')
    intab = "“’”"
    outtab = '''"'"'''
    trantab = string.maketrans(intab, outtab)
    splitList = f.strip().translate(trantab).split()
    for out in splitList:
        if out.lower() not in stopwords:
            var = out
            if var in dic:
                dic[var] = dic[var] + 1
            else:
                dic[var] = 1
    return dic

def docToDic_clean (f):
    dic = {}
    f = f.encode('ascii', 'ignore')
    splitList = []
    par = f.translate(None, '?.!/;:()#$%^*"<>{}[]“”…').replace("’","'").replace("—"," ")
    for x in par.split():
        if not x.islower():
            continue
        if x.lower() not in stopwords:
            var = x
            if var in dic:
                dic[var] = dic[var] + 1
            else:
                dic[var] = 1
    return dic    

def num_words(f):
    f = f.encode('ascii', 'ignore')
    num = len(f.split())
    return num

def avg_words(f):
    dic = {}
    f = f.encode('ascii', 'ignore')
    par = f.translate(None, '?.!/;:()#$%^*"<>{}[]“”…').replace("’","'").replace("—"," ")
    i = 0
    for x in par.split():
        count = len(x)
        if count in dic:
            dic[count] = dic[count] + 1
        else:
            dic[count] = 1
        i += 1
    return dic


def var_words(f):
    dic = {}
    f = f.encode('ascii', 'ignore')
    par = f.translate(None, '?.!/;:()#$%^*"<>{}[]“”…').replace("’","'").replace("—"," ")
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
    return dic
            
def var_sen(f):
    dic = {}
    f = f.encode('ascii', 'ignore')
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    x = sent_detector.tokenize(f.strip())
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
    return dic


def bigram_clean(f):
    dic = {}
    f = f.encode('ascii', 'ignore')
    par = f.translate(None, '?.!/;:()#$%^*"<>{}[]“”…').lower().replace("’","'").replace("—"," ")
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(par.split())
    finder.apply_freq_filter(2)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    for x in scored:
        if x[0] in dic: 
            dic[x[0]] += num_words(f) *x[1]
        else:
            dic[x[0]] = num_words(f) *x[1]
    return dic

def bigram(f):
    dic = {}
    f = f.encode('ascii', 'ignore')
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(f.split())
    finder.apply_freq_filter(2)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    for x in scored:
        if x[0] in dic: 
            dic[x[0]] += num_words(f) *x[1]
        else:
            dic[x[0]] = num_words(f) *x[1]
    return dic


def trigram_clean(f):
    dic = {}
    f = f.encode('ascii', 'ignore')
    par = f.translate(None, '?.!/;:()#$%^*"<>{}[]“”…').lower().replace("’","'").replace("—"," ")
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(par.split())
    finder.apply_freq_filter(2)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    for x in scored:
        if x[0] in dic: 
            dic[x[0]] += num_words(f) *x[1]
        else:
            dic[x[0]] = num_words(f) *x[1]
    return dic



def docToDic(f, num):
    if num == 0:
        return docToDic_stopwords(f),1.0
    if num == 1:
        return docToDic_clean(f),1.0
    if num == 2:
        return avg_words(f),.92
    if num == 3:
        return var_words(f),.92
    if num == 4:
        return var_sen(f), .80
    if num == 5:
        return bigram(f), .91
    if num == 6:
        return bigram_clean(f), 1.0
    if num == 7:
        return trigram_clean(f), 1.0
    return f

def MLE(dicn, dicp, pcount):
    pcount = float(pcount)
    val = sum(dicn.itervalues())
    for key in dicn:
        dicp[key] = (dicn[key] + pcount)/ ((len (dicn)*pcount) + val)
    return dicp

def MNB(author_1, a1_val, author_2,a2_val, unk, pcount):
    a1val = float(1)
    a2val = float(1)
    pcount = float(pcount)
    for val in unk:
        if val in author_2:
            a2val = a2val + (unk[val]*math.log(author_2[val]))
            if val in author_1:
                a1val = a1val + (unk[val]*math.log(author_1[val]))
            else:
                a1val = a1val + (unk[val]* math.log((pcount/ ((len (author_1)*pcount) + a1_val))))
        else:
            if val in author_1:
                a1val = a1val + (unk[val]*math.log(author_1[val]))
            else:
                a1val = a1val + (unk[val]* math.log((pcount/ ((len (author_1)*pcount) + a1_val))))
            a2val = a2val + (unk[val]* math.log((pcount/ ((len (author_2)*pcount) + a2_val))))
    if a1val < 0 and a2val < 0:
        a = a2val/a1val
    if a1val < 0 and a2val > 0:
        a = ((a1val*2)+a1val)/a2val
    if a1val > 0 and a2val < 0:
        a = a1val/((a2val*2)+a2val)
    if a1val > 0 and a2val > 0:
        a = a1val/a2val
    return a1val > a2val, a


def runUnknown (author_1, author_2, unknown, num):
    pcount = float(.5)
    a1_dic_p = {}
    a2_dic_p ={}
    a1_dic_p = MLE(author_1, a1_dic_p, pcount)
    a2_dic_p = MLE(author_2, a2_dic_p, pcount)
    val = sum(author_1.itervalues())
    val2 = sum(author_2.itervalues())
    unNT = {}
    unNT, per = docToDic(unknown, num)
    a,b = MNB(a1_dic_p,val, a2_dic_p,val2, unNT,pcount )
    if a:
        return float(b - ((b-1)*(1-per)))
    else:
        return float(b + ((1-b) *(1-per)))   
    
    
