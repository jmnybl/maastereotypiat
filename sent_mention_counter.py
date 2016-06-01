import conllutil3 as cu
import sys
import json
import pickle

swords={}
with open("sentiment.txt") as f:
    for line in f:
        line=line.strip()
        fi,s,en=line.split("\t")
        swords[fi]=s

hit_counter={} # kwordlemma, nationality -> count
lemma_sent={} #kwordlemma,sent -> count

for comm,sent in cu.read_conllu(sys.stdin):
    nats=set(c.split(": ")[1] for c in comm if c.startswith("# nationality"))
    for line in sent:
        form,lemma=line[cu.FORM],line[cu.LEMMA]
        if form in swords:
            for n in nats:
                hit_counter[(lemma,n)]=hit_counter.get((lemma,n),0)+1
            sent=swords[form]
            lemma_sent[(lemma,sent)]=lemma_sent.get((lemma,sent),0)+1
        elif lemma.replace("#","") in swords:
            for n in nats:
                hit_counter[(lemma,n)]=hit_counter.get((lemma,n),0)+1
            sent=swords[lemma.replace("#","")]
            lemma_sent[(lemma,sent)]=lemma_sent.get((lemma,sent),0)+1

with open("sentiment_counts.pkl","wb") as f:
    pickle.dump([hit_counter,lemma_sent],f)

