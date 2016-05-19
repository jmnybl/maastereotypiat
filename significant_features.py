# -*- encoding: utf-8 -*-

import codecs
import sklearn.feature_extraction
from sklearn.svm import LinearSVC
import sys
import conllutil
import gzip
import numpy as np
import re

""" One versus all svm classification with heavy regularization to find most significant features. """

def vocabulary(f):

    vocabulary=set()
    country_codes=dict()

    for line in f:
        line=line.strip()
        code,words=line.split(u"\t")
        words=words.split(u",")
        for w in words:
            if w.endswith(u"nen"):
                vocabulary.add(re.sub('nen$', 'set', w))
                country_codes[re.sub('nen$', 'set', w)]=code
            vocabulary.add(w)
            country_codes[w]=code

    return vocabulary,country_codes


def country_or_citizen(line):
    """ return 1 if country and -1 if citizen """
    if line[conllutil.CPOS]==u"ADJ" or line[conllutil.CPOS]==u"PROPN":
        return 1
    if u"Derivation=Lainen" in line[conllutil.FEAT]:
        return -1
    if u"lainen" in line[conllutil.LEMMA] or u"laiset" in line[conllutil.LEMMA] or u"läinen" in line[conllutil.LEMMA] or u"läiset" in line[conllutil.LEMMA]:
        return -1
    return 1

#def decide_label(sent,country):
#    pass


labels=[]

def data_iterator(f,country,vocabulary,max_count=100000):
    global labels

    comment_line=u"# nationality: "+country

    counter=0
    for comm,sent in conllutil.read_conllu(f):
        if comment_line in comm: # this is positive example
            labels.append(1)
        else:
            labels.append(0)
        words=[]
        for line in sent:
            if line[conllutil.FORM] in vocabulary or line[conllutil.LEMMA].replace(u"#",u"") in vocabulary:# or line[conllutil.CPOS]!=u"ADJ":
                continue # remove nationality words
            else:
                words.append(line[conllutil.LEMMA])

        if not words: # no adjectives in this sentence
            words.append(u"EMPTY")
        stext=u" ".join(words)
        yield stext
        counter+=1
        if max_count!=0 and counter==max_count:
            break

def tokenizer(txt):
    """Simple whitespace tokenizer"""
    return txt.split()


country_code=unicode(sys.argv[1])

with codecs.open(u"nations_ready.txt",u"rt",u"utf-8") as f:
    vocab,country_codes=vocabulary(f)

iterator=data_iterator(codecs.getreader(u"utf-8")(sys.stdin),country_code,vocab)

#vectorizer=sklearn.feature_extraction.text.TfidfVectorizer(tokenizer=tokenizer,use_idf=True) #,max_df=0.9

vectorizer=sklearn.feature_extraction.text.CountVectorizer(tokenizer=tokenizer) #,max_df=0.9,min_df=0.01
d=vectorizer.fit_transform(iterator)

classifier=LinearSVC(penalty="l1",C=0.1,dual=False)
classifier.fit(d,labels)


print "Non-zero features:",np.count_nonzero(classifier.coef_)
f_names=vectorizer.get_feature_names()
sorted_by_weight=sorted(zip(classifier.coef_[0],f_names))
for f_weight,f_name in sorted_by_weight[-30:]:
    print f_name, f_weight
print "------------------------"
for f_weight,f_name in sorted_by_weight[:30]:
    print f_name, f_weight



#fnames=vectorizer.get_feature_names()
#print len(fnames),fnames[:10]

#dense = d.todense()
#document = dense[0].tolist()[0]
#scores = [pair for pair in zip(range(0, len(document)), document) if pair[1] > 0]
#print len(scores)
#top_n = sorted(scores, key=lambda t: t[1] * -1)[:5]
#for w,sc in top_n:
#    print fnames[w],sc

#indices = np.argsort(vectorizer.idf_)[::-1]


#top_features = [fnames[i] for i in indices[:50]]
#print top_features


#devel_iterator=data_iterator(codecs.getreader(u"utf-8")(gzip.open(u"nationality_data_pb_old.conllu.gz")))
#for text in devel_iterator:
#    print d.transform(text)
#    sys.exit()

##print d[:10]
##print "documents x features", d.shape
#fnames=tfidf_v.get_feature_names()
##for feature_id in range(1,500,50):
##    print feature_id,fnames[feature_id],d[feature_id]
