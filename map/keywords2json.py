import glob
import re
import json
import os
import pickle
import math

with open("../sentiment_counts.pkl","rb") as f:
    hit_counter,lemma_sent=pickle.load(f)

#hit_counter: (lemma,country) -> count
#lemma_sent: (lemma,sent) -> count

def get_sentiment(lemmas,country):
    """None if unknown, or number between 0-1 neg-pos"""
    global hit_counter, lemma_sent
    w_sum=0
    norm_const=0
    for l in lemmas[:20]:
        #what is the sentiment of this lemma?
        l_pos=lemma_sent.get((l,"pos"),0)
        l_neg=lemma_sent.get((l,"neg"),0)
        if l_pos==0 and l_neg==0:
            continue
        sent=l_pos/(l_pos+l_neg) #How positive is this lemma as such? (0,1)
        c=hit_counter.get((l,country),0)
        if c==0:
            continue
        c=math.log(c)
        w_sum+=sent*c
        norm_const+=c
    if norm_const==0:
        return None
    else:
        return w_sum/norm_const


def brformat(kwords,N=6):
    """Formats keywords into html, N per line"""
    lines=[]
    for i in range(0,len(kwords),N):
        lines.append(", ".join(kwords[i:i+N]))
    return " <br/> ".join(lines)


countries={} #  dataset -> country-code -> list

f_name_re=re.compile("^(s24|pb)_(.*?)_([A-Z]{2})$")
for f_name in glob.glob("/home/jmnybl/git_checkout/maastereotypiat/results3/*"):
    base=os.path.basename(f_name)
    match=f_name_re.match(base)
    if not match:
        continue
    country_dict=countries.setdefault(match.group(1)+"_"+match.group(2),{})
    with open(f_name) as f:
        data=list(map(str.strip,f.readlines()))
        if not data: #empty file, skip
            continue
        ccode=data[0].split()[0]
        for feature_line in data[1:]:
            feature,weight=feature_line.split("\t")
            country_dict.setdefault(ccode,[]).append(feature)

for dataset,country_dict in list(countries.items()):
    done_dict=countries.setdefault(dataset+"-done",{})
    sentiment_dict=countries.setdefault(dataset+"-sentiment",{})
    for ccode in country_dict:
        s=get_sentiment(country_dict[ccode],ccode)
        if s is not None:
            sentiment_dict[ccode]=s
        done_dict[ccode]=1
        country_dict[ccode]=brformat(country_dict[ccode][:21])

with open("features.json","w") as f:
    print("features = '{}';".format(json.dumps(countries)),file=f)


            
        
