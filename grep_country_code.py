import codecs
import sys
import re
import conllutil3 as cu

code=sys.argv[1]
comment="# nationality: "+code
print(comment, file=sys.stderr)

counter=1
for comm,sent in cu.read_conllu(sys.stdin):

    if comment in comm:

        cu.plain_print(sys.stdout,comm,sent)
        counter+=1

print("sentences=",counter,sep="",file=sys.stderr)
