import codecs
import sklearn.feature_extraction
from sklearn.svm import LinearSVC
from sklearn.metrics import classification_report
import sys
import conllutil3 as cu
import gzip
import numpy as np
import re
from filter_pb import read_vocabulary

""" One versus all svm classification with heavy regularization to find most significant features. """

dev_labels=[]
dev_texts=[]

labels=[]

def data_iterator(f,country,vocabulary,cpos=None,max_count=500000):
    global labels,dev_labels,dev_texts

    comment_line="# nationality: "+country

    counter=0
    for comm,sent in cu.read_conllu(f):
        
        words=[]
        for line in sent:
            if cpos is not None and line[cu.CPOS] not in cpos:
                continue
            if line[cu.FORM] in vocabulary or line[cu.LEMMA].replace("#","") in vocabulary:
                continue # remove nationality words
            else:
                words.append(line[cu.LEMMA])

        if not words: # no adjectives in this sentence
            continue
        
        if comment_line in comm: # this is positive example
            if counter%1000==0:
                dev_labels.append(1)
            else:
                labels.append(1)
        else:
            if counter%1000==0:
                dev_labels.append(0)
            else:
                labels.append(0)

        stext=" ".join(words)
        if counter%1000==0:
            dev_texts.append(stext)
        else:
            yield stext
        counter+=1
        if max_count!=0 and counter==max_count:
            break

def tokenizer(txt):
    """Simple whitespace tokenizer"""
    return txt.split()


country_code=sys.argv[1]
try:
    cpos=sys.argv[2].split(",")
except:
    cpos=None
if cpos:
    for p in cpos:
        assert p in cu.allowed_pos

print("Country code:", country_code, "CPOS:", cpos, sep=" ", file=sys.stderr)

with open("nations_ready.txt","rt",encoding="utf-8") as f:
    vocab,country_codes=read_vocabulary(f)

iterator=data_iterator(sys.stdin,country_code,vocab,cpos=cpos,max_count=0)

vectorizer=sklearn.feature_extraction.text.TfidfVectorizer(tokenizer=tokenizer,max_df=0.3,sublinear_tf=True,use_idf=False)

d=vectorizer.fit_transform(iterator)



for c in np.arange(0.00001,0.1,0.00005):
    classifier = LinearSVC(penalty="l1",C=c,dual=False,class_weight="balanced")

    classifier.fit(d,labels)

#    print(len(dev_labels),dev_labels.count(0),dev_labels.count(1),sep=" ")
#    print(classification_report(classifier.predict(vectorizer.transform(dev_texts)),dev_labels))

    non_zero=np.count_nonzero(classifier.coef_[classifier.coef_ > 0]) # count only positive features

#    print("Non-zero positive features:",non_zero)
    

    if non_zero>100: # save and die
        print(country_code,"# c value:",c,"# Non-zero positive features:",non_zero)
        f_names=vectorizer.get_feature_names()
        sorted_by_weight=sorted(zip(classifier.coef_[0],f_names), reverse=True)
        for f_weight,f_name in sorted_by_weight[:non_zero]:
            print(f_name, f_weight, sep="\t")
        break



