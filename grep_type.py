# -*- encoding: utf-8 -*-

import codecs
import sys
import re
import conllutil

""" Pass only sentences with either country words or person words """


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
    """ return country or citizen """
    if line[conllutil.CPOS]==u"ADJ" or line[conllutil.CPOS]==u"PROPN":
        return u"country"
    if u"Derivation=Lainen" in line[conllutil.FEAT]:
        return u"citizen"
    if u"lainen" in line[conllutil.LEMMA] or u"laiset" in line[conllutil.LEMMA] or u"läinen" in line[conllutil.LEMMA] or u"läiset" in line[conllutil.LEMMA]:
        return u"citizen"
    return u"country"


ntype=unicode(sys.argv[1])
if ntype!=u"country" and ntype!=u"citizen":
    print >> sys.stderr, "Error: Argument must be country or citizen"
    sys.exit(1)

with codecs.open(u"nations_ready.txt",u"rt",u"utf-8") as f:
    vocab,country_codes=vocabulary(f)


counter=1
for comm,sent in conllutil.read_conllu(codecs.getreader(u"utf-8")(sys.stdin)):

    remove=[]

    for line in sent:
        if line[conllutil.FORM] in vocab or line[conllutil.LEMMA].replace(u"#",u"") in vocab:
            if country_or_citizen(line)!=ntype:
                if line[conllutil.LEMMA].replace(u"#",u"") in country_codes:
                    remove.append(country_codes[line[conllutil.LEMMA].replace(u"#",u"")])
                else:
                    remove.append(country_codes[line[conllutil.FORM]])

    for code in remove:
        comm.remove(u"# nationality: "+code)
    for c in comm:
        if c.startswith(u"# nationality:"):
            conllutil.plain_print(sys.stdout,comm,sent)
            counter+=1
            break

print >> sys.stderr,counter
