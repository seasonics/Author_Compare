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

def docToDic_stopwords (f,dic):
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
    return dic

def docToDic_clean (f,dic):
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
    return dic    

def num_words(f):
    num = len(f.read().split())
    return num

def num_chars(f):
    num = len(f.read().strip())
    return num

def quotes(f):
    count = 0
    intab = "“’”"
    outtab = '''"'"'''
    trantab = string.maketrans(intab, outtab)
    for x in f.read().translate(trantab):
        if x == '"':
            count += 1
    return count


def avg_words(f,dic):
    par = f.read().translate(None, '?.!/;:()#$%^*"<>{}[]“”…').replace("’","'").replace("—"," ")
    i = 0
    for x in par.split():
        count = len(x)
        if count in dic:
            dic[count] = dic[count] + 1
        else:
            dic[count] = 1
        i += 1
    return dic


def var_words(f,dic):
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
    return dic
            
def var_sen(f,dic):
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
    return dic


def bigram_clean(f,dic):
    par = f.read().translate(None, '?.!/;:()#$%^*"<>{}[]“”…').lower().replace("’","'").replace("—"," ")
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

def bigram(f,dic):
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(f.read().split())
    finder.apply_freq_filter(2)
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    for x in scored:
        if x[0] in dic: 
            dic[x[0]] += num_words(f) *x[1]
        else:
            dic[x[0]] = num_words(f) *x[1]
    return dic


def trigram_clean(f,dic):
    par = f.read().translate(None, '?.!/;:()#$%^*"<>{}[]“”…').lower().replace("’","'").replace("—"," ")
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





def docToDic(f,dic, num):
    f = open(f, 'r')
    if num == 0:
        return docToDic_stopwords(f,dic),1.0
    if num == 1:
        return docToDic_clean(f,dic),1.0
    if num == 2:
        return avg_words(f,dic),.92
    if num == 3:
        return var_words(f,dic),.92
    if num == 4:
        return var_sen(f,dic), .80
    if num == 5:
        return bigram(f,dic), .91
    if num == 6:
        return bigram_clean(f,dic), 1.0
    if num == 7:
        return trigram_clean(f,dic), 1.0
    f.close()
    return dic

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

def process (author_1, author_2):
    tcount = 0
    pcount = .5
    count = 0
    arr = [0] * 20
    c = 0
    while c <8:
        i = 0
        a2_dic_n = {}
        a2_dic_p = {}
        for x in author_2:
            a2_dic_n, per = docToDic(x, a2_dic_n, c)
        a2_dic_p = MLE(a2_dic_n, a2_dic_p, pcount)
        while i<20:
            a1_dic_n = {}
            a1_dic_p = {}
            j = 0
            for x in author_1:
               if j == i:
                   j
               else:
                   a1_dic_n,per = docToDic(x, a1_dic_n,c)
               j = j+1
            a1_dic_p = MLE(a1_dic_n, a1_dic_p, pcount)
            val = sum(a1_dic_n.itervalues())
            val2 = sum(a2_dic_n.itervalues())
            a1_NT = {}
            a1_NT,per = docToDic(author_1[i], a1_NT,c)
            a,b = MNB(a1_dic_p,val, a2_dic_p,val2, a1_NT,pcount)
            if a:
                arr[i] += (b - ((b-1)*(1-per)))
            else:
                arr[i] += (b + ((1-b) *(1-per)))
            i=i+1
        c += 1
    print arr
    return
##        i = 0
##        a1_dic_n = {}
##        a1_dic_p = {}
##        for x in author_1:
##            a1_dic_n = docToDic(x, a1_dic_n,c)
##        a1_dic_p = MLE(a1_dic_n, a1_dic_p,pcount)
##        while i<20:
##            a2_dic_n = {}
##            a2_dic_p = {}
##            j = 0
##            for x in author_2:
##               if j == i:
##                   j
##               else:
##                   a2_dic_n = docToDic(x, a2_dic_n,c)
##               j = j+1
##
##            a2_dic_p = MLE(a2_dic_n, a2_dic_p, pcount)
##            val = sum(a1_dic_n.itervalues())
##            val2 = sum(a2_dic_n.itervalues())
##            a2_NT = {}
##            a2_NT = docToDic(author_2[i], a2_NT,c)
##            a,b = MNB(a2_dic_p,val2, a1_dic_p,val, a2_NT,pcount )
##            if a:
##                print b
##            else:
##                count = count+1
##            i=i+1
##        c += 1
##    print count
    

process(meyer, hemway)    


# def runUnknown (ham, mad, unknown):
    # maddicn = {}
    # maddicp = {}
    # hamdicn = {}
    # hamdicp = {}
    # pcount = float(3)
    # for x in mad:
        # maddicn = docToDic(x, maddicn)
    # maddicp = MLE(maddicn, maddicp, pcount)
    # for x in ham:
        # hamdicn = docToDic(x, hamdicn)
    # hamdicp = MLE(hamdicn, hamdicp,pcount)
    # val = sum(hamdicn.itervalues())
    # val2 = sum(maddicn.itervalues())
    # for x in unknown:
        # unNT = {}
        # unNT = docToDic(x, unNT)
        # if MNB(hamdicp,val, maddicp,val2, unNT,pcount ):
            # print "hamilton"
        # else:
            # print "madison"
    

# runUnknown(hamilton, madison, unknown)
    
