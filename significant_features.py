# -*- encoding: utf-8 -*-

import codecs
import sklearn.feature_extraction
from sklearn.svm import LinearSVC
import sys
import conllutil3 as cu
import gzip
import numpy as np
import re
from filter_pb import read_vocabulary

""" One versus all svm classification with heavy regularization to find most significant features. """



labels=[]

def data_iterator(f,country,vocabulary,max_count=500000):
    global labels

    comment_line="# nationality: "+country

    counter=0
    for comm,sent in cu.read_conllu(f):
        if comment_line in comm: # this is positive example
            labels.append(1)
        else:
            labels.append(0)
        words=[]
        for line in sent:
            if line[cu.FORM] in vocabulary or line[cu.LEMMA].replace("#","") in vocabulary or line[cu.CPOS]!="ADJ":
                continue # remove nationality words
            else:
                words.append(line[cu.LEMMA])

        if not words: # no adjectives in this sentence
            words.append("EMPTY")
        stext=" ".join(words)
        yield stext
        counter+=1
        if max_count!=0 and counter==max_count:
            break

def tokenizer(txt):
    """Simple whitespace tokenizer"""
    return txt.split()


country_code=sys.argv[1]

with open("nations_ready.txt","rt",encoding="utf-8") as f:
    vocab,country_codes=read_vocabulary(f)

iterator=data_iterator(sys.stdin,country_code,vocab)

#vectorizer=sklearn.feature_extraction.text.TfidfVectorizer(tokenizer=tokenizer,use_idf=True) #,max_df=0.9

vectorizer=sklearn.feature_extraction.text.CountVectorizer(tokenizer=tokenizer) #,max_df=0.9,min_df=0.01
d=vectorizer.fit_transform(iterator)

classifier=LinearSVC(penalty="l1",C=0.1,dual=False)
classifier.fit(d,labels)


print("Non-zero features:",np.count_nonzero(classifier.coef_),sep=" ")
f_names=vectorizer.get_feature_names()
sorted_by_weight=sorted(zip(classifier.coef_[0],f_names))
for f_weight,f_name in sorted_by_weight[-30:]:
    print(f_name, f_weight, sep="\t")
print("------------------------")
for f_weight,f_name in sorted_by_weight[:30]:
    print(f_name, f_weight, sep="\t")



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
