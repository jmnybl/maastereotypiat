import codecs
import sys
import re

#from "/home/jmnybl/git_checkout/conllutil3" import conllutil3 as conllutil
from filter_pb import read_vocabulary

import conllutil3 as cu

""" Pass only sentences with either country words or person words """



def country_or_citizen(line):
    """ return country or citizen """
    if line[cu.CPOS]=="ADJ" or line[cu.CPOS]=="PROPN":
        return "country"
    if "Derivation=Lainen" in line[cu.FEAT]:
        return "citizen"
    if "lainen" in line[cu.LEMMA] or "laiset" in line[cu.LEMMA] or "läinen" in line[cu.LEMMA] or "läiset" in line[cu.LEMMA]:
        return "citizen"
    return "country"


ntype=sys.argv[1]
if ntype!="country" and ntype!="citizen":
    print("Error: Argument must be country or citizen",file=sys.stderr)
    sys.exit(1)

with open("nations_ready.txt","rt",encoding="utf-8") as f:
    vocab,country_codes=read_vocabulary(f)


counter=1
for comm,sent in cu.read_conllu(sys.stdin):

    remove=[]

    for line in sent:
        if line[cu.FORM] in vocab or line[cu.LEMMA].replace("#","") in vocab:
            if country_or_citizen(line)!=ntype:
                if line[cu.LEMMA].replace(u"#",u"") in country_codes:
                    remove.append(country_codes[line[cu.LEMMA].replace("#","")])
                else:
                    remove.append(country_codes[line[cu.FORM]])

    for code in remove:
        comm.remove("# nationality: "+code)
    for c in comm:
        if c.startswith("# nationality:"):
            cu.plain_print(sys.stdout,comm,sent)
            counter+=1
            break

print("sentences=",counter,sep="",file=sys.stderr)
