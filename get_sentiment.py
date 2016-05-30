import csv

#        0                   1               2              3                     4                5            6             7                 8                9
#(41, 'Positive'), (42, 'Negative'), (43, 'Anger'), (44, 'Anticipation'), (45, 'Disgust'), (46, 'Fear'), (47, 'Joy'), (48, 'Sadness'), (49, 'Surprise'), (50, 'Trust')

with open("/home/ginter/NRC-Emotion-Lexicon-v0.92-InManyLanguages-web.csv") as f:
    for cols in list(csv.reader(f))[1:]:
        classes=list(map(int,list(cols[41:])))
        if any((classes[0],)):#,classes[6],classes[9])):
            sentiment="pos"
        elif any((classes[1],)):#classes[2],classes[4],classes[5],classes[7])):
            sentiment="neg"
        else:
            sentiment=None
        if sentiment is not None and cols[10]:
            print(cols[10],sentiment,cols[0],sep="\t")

