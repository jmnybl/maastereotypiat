import codecs
import sys
import re
import conllutil3 as cu


def read_vocabulary(f):

    vocabulary=set()
    country_codes=dict()

    for line in f:
        line=line.strip()
        code,words=line.split("\t")
        words=words.split(",")
        for w in words:
            if w.endswith("nen"):
                vocabulary.add(re.sub("nen$", "set", w))
                country_codes[re.sub("nen$", "set", w)]=code
            vocabulary.add(w)
            country_codes[w]=code

    return vocabulary,country_codes


if __name__=="__main__":

    with open("nations_ready.txt","rt",encoding="utf-8") as f:
        vocab,country_codes=read_vocabulary(f)


    counter=1
    for comm,sent in cu.read_conllu(sys.stdin):

        hit=False
        for line in sent:

            if line[cu.FORM] in vocab or line[cu.LEMMA].replace("#","") in vocab:
                # hit !!!
                if line[cu.LEMMA].replace("#","") in country_codes:
                    comm.append("# nationality: "+country_codes[line[cu.LEMMA].replace("#","")])
                else:
                    comm.append("# nationality: "+country_codes[line[cu.FORM]])
                hit=True
            

        if hit: # print
            comm.insert(0,"# sentence: "+str(counter))
            cu.plain_print(sys.stdout,comm,sent)
            counter+=1
            hit=False


