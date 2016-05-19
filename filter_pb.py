import codecs
import sys
import re
import conllutil


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


with codecs.open(u"nations_ready.txt",u"rt",u"utf-8") as f:
    vocab,country_codes=vocabulary(f)


counter=1
for comm,sent in conllutil.read_conllu(codecs.getreader(u"utf-8")(sys.stdin)):

    hit=False
    for line in sent:

        if line[conllutil.FORM] in vocab or line[conllutil.LEMMA].replace(u"#",u"") in vocab:
            # hit !!!
            if line[conllutil.LEMMA].replace(u"#",u"") in country_codes:
                comm.append(u"# nationality: "+country_codes[line[conllutil.LEMMA].replace(u"#",u"")])
            else:
                comm.append(u"# nationality: "+country_codes[line[conllutil.FORM]])
            hit=True
            

    if hit: # print
        comm.insert(0,u"# sentence: "+unicode(counter))
        conllutil.plain_print(sys.stdout,comm,sent)
        counter+=1
        hit=False


